
from django.urls import include, path

from main import api

main_api_urls = [
  path('competition/<competition_id>', api.competition),
  path('competitions', api.list_open_competitions),
  path('competitions/register/<competition_id>', api.register_for_competition),
  path('settings', api.get_site_settings)
]
