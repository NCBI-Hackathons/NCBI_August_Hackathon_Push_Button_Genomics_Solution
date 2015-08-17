import json
import requests

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import Gene


class IndexView(generic.TemplateView):
    template_name = 'browser/index.html'


class UploadView(generic.TemplateView):
    template_name = "browser/upload.html"

    def get(self, request):
        return render(request, self.template_name, {"foo": "asdfasdf"})


class UploadFormView(generic.TemplateView):

    def post(self, request):
        email = request.POST.get("email")
        uploadID = request.POST.get("uploadID")
        fileFormat = request.POST.get("format")
        file = request.FILES['file']

        file_path = "browser/userdata/" + uploadID + "/" + file.name

        # TODO: file.read() may not handle files larger than 2.5 MB
        # Test and develop a more robust solution if needed
        default_storage.save(file_path, ContentFile(file.read()))

        return redirect(reverse('results', args=[uploadID]), foo='bar')

    def get(self, request): 
        email = request.GET.get("email")
        uploadID = request.GET.get("uploadID")
        fileFormat = request.GET.get("format")
        fileUrl = request.GET.get("fileUrl")
        print "email:"
        print email
        print ""
        print "uploadID:"
        print uploadID
        print ""
        print "format:"
        print fileFormat
        print ""
        print "fileUrl:"
        print fileUrl

        # Call SnakeMake
        # snakemake -s ABSOLUTE_PATH_TO_FILE

        # Upon return, data is in Solr and user can be redirected
        # to /results/<uploadID>

        #
        return redirect('ResultsView', uploadID=uploadID)


class ResultsView(generic.TemplateView):
    template_name = "browser/results.html"

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data()

        # call to solr
        url = '{solr_host}/select?' \
              'q=*%3A*&' \
              'rows=0&' \
              'wt=json&' \
              'indent=true&' \
              'facet=true&' \
              'facet.pivot=gene_name_hgnc_s,putative_impact_s&' \
              'facet.pivot=gene_name_hgnc_s,annotation_s'.format(solr_host=settings.SOLR_HOST)
        response = requests.request('GET', url)

        context['url'] = url

        solr_data = json.loads(response.content)

        context['solr_data'] = {}
        for g_data in solr_data['facet_counts']['facet_pivot']['gene_name_hgnc_s,annotation_s']:
            gene = g_data['value']
            count = g_data['count']
            annotations = {a['value']: a['count'] for a in g_data['pivot']}
            context['solr_data'][gene] = {'count': count, 'annotations': annotations}


        for g_data in solr_data['facet_counts']['facet_pivot']['gene_name_hgnc_s,putative_impact_s']:
            gene = g_data['value']
            impacts = {'HIGH': 0, 'MODERATE': 0, 'LOW': 0, 'MODIFIER': 0}
            for impact in g_data["pivot"]:
                impacts[impact['value']] += impact['count']
            impact_cols = {
                'high_impact': impacts['HIGH'],
                'moderate_impact': impacts['MODERATE'],
                'low_impact': impacts['LOW'],
                'modifier_impact': impacts['MODIFIER'],
            }
            context['solr_data'][gene].update(impact_cols)

        genes_paginator = Paginator(Gene.objects.filter(gene_name__in=context['solr_data'].keys()), 10)
        page = self.request.GET.get('page')
        try:
            genes = genes_paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            genes = genes_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            genes = genes_paginator.page(genes_paginator.num_pages)

        context['genes_all'] = genes

        return context
