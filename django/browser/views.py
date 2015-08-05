from django.views import generic
from django.shortcuts import render

class IndexView(generic.TemplateView):
    template_name = 'browser/index.html'

class UploadView(generic.TemplateView):

    template_name = "browser/upload.html"

    def get(self, request):
        return render(request, self.template_name, {"foo": "asdfasdf"})

class ResultsView(generic.TemplateView):

    template_name = "browser/results.html"

    mock_results = {
        "filters": [
            ["Clinical significance", "Pathogenic"], 
            ["Molecular consequence", "Missense"]
        ],
        "genes": [
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
    }

    def get(self, request):
        return render(request, self.template_name, self.mock_results)
