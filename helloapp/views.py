from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name =  "index.html"
    def post(self,request,**kwargs):
        return render(request,'index.html',context=None)
    
class AboutPageView(TemplateView):
    template_name =  "about.html"

class PlotPageView(TemplateView):
    template_name = "plotly.html"
    
    
class SamplePageView(TemplateView):
    template_name = "PageExample.html"
    
class TemplatePageView(TemplateView):
    template_name = "template.html"    