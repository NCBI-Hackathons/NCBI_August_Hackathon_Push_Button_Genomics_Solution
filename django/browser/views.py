from django.views import generic
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Gene


class IndexView(generic.TemplateView):
    template_name = 'browser/index.html'


    '''
    def post(self, request):
        email = request.POST.get("email", "")
        uploadID = request.POST.get("uploadID", "")
	fileFormat = request.POST.get("format", "")
        print "email:"
        print email
        print ""
        print "uploadID:"
        print uploadID
        print ""
        print "format:"
        print fileFormat
    '''

class UploadView(generic.TemplateView):
    template_name = "browser/upload.html"

    def get(self, request):
        return render(request, self.template_name, {"foo": "asdfasdf"})


class UploadFormView(generic.TemplateView):
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

	kwargs["uploadID"]

        context['genes_all'] = Gene.objects.all()[:5]

        context["filters"] = [
            ["Clinical significance", "Pathogenic"],
            ["Molecular consequence", "Missense"]
        ]

        context["genes"] = [
            {
                "symbol": "BRCA",
                "id": "672",
                "length": "81,189",
                "pathogenic_variants": "4",
                "benign_variants": "50",
                "missense_variants": "3",
                "synonymous_variants": "130"
            },
            {
                "symbol": "APOE",
                "id": "348",
                "length": "3,647",
                "pathogenic_variants": "0",
                "benign_variants": "2",
                "missense_variants": "0",
                "synonymous_variants": "11"
            },
            {
                "symbol": "MLH1",
                "id": "4292",
                "length": "2,662",
                "pathogenic_variants": "13",
                "benign_variants": "2",
                "missense_variants": "10",
                "synonymous_variants": "0"
            }
        ]

        return context
