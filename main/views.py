
from django.shortcuts import render

from main.models import SiteSettings

# Create your views here.

def site_home(request):

  site_settings = SiteSettings.load()

  data = {
    'settings': site_settings,
    'site_title': site_settings.site_branding,
    'title': site_settings.site_branding
  }
  return render(request, 'main.html', data)

def main_app(request):
  
  site_settings = SiteSettings.load()

  data = {
    'settings': site_settings,
    'site_title': site_settings.site_branding,
    'title': site_settings.site_branding
  }
  return render(request, 'app.html', data)
