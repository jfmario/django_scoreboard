
from django.urls import include, path

from main import api

main_api_urls = [
  path('competition/<competition_id>', api.competition),
  path('competition/<competition_id>/challenge/<challenge_id>', api.get_challenge),
  path('competition/<competition_id>/challenge/<challenge_id>/hint', api.purchase_challenge_hint),
  path('competition/<competition_id>/challenge/<challenge_id>/submit', api.submit_challenge_answer),
  path('competition/<competition_id>/leaderboard', api.get_competition_leaderboard),
  path('competitions', api.list_open_competitions),
  path('competitions/register/<competition_id>', api.register_for_competition),
  path('settings', api.get_site_settings)
]
