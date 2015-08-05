from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'browser/index.html'

class UploadView(generic.TemplateView):
    template_name = "browser/upload.html"

