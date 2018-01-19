
import datetime, json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import Competition, SiteSettings
from main.utils import get_user_participation_record, get_visible_challenge_list

@csrf_exempt
@login_required
def competition(request, competition_id):

  competition = Competition.objects.get(pk=competition_id)
  upr = get_user_participation_record(request.user, competition)
  if not upr:
    return HttpResponse("Unauthorized", status_code=401)

  status = competition.status

  data = {}
  data['status'] = status
  data['competition'] = { 'id': competition.pk }
  data['competition']['status'] = status
  data['competition']['name'] = competition.name
  data['competition']['description'] = competition.html_description
  data['competition']['welcome'] = competition.html_welcome_message
  data['competition']['startTime'] = competition.start_time.strftime('%Y-%m-%dT%H:%M:%S')
  data['competition']['endTime'] = competition.end_time.strftime('%Y-%m-%dT%H:%M:%S')

  if status == 'ACTIVE' or status == 'OVER':
    data['challenges'] = get_visible_challenge_list(upr)

  return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def list_open_competitions(request):

  open_competitions = Competition.objects.filter(is_open=True)
  user_competitions = Competition.objects.filter(users__id=request.user.pk)
  all_competitions = list(user_competitions) + list(open_competitions)

  data = [{
    'id': c.pk,
    'name': c.name,
    'description': c.html_description,
    'startTime': c.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
    'endTime': c.end_time.strftime('%Y-%m-%dT%H:%M:%S')
  } for c in all_competitions]
  return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def register_for_competition(request, competition_id):

  competition = Competition.objects.get(pk=competition_id)
  if request.user in competition.users.all():
    return HttpResponse(json.dumps({ 'success': True }))
  elif competition.is_open:

    competition.users.add(request.user)
    competition.save()

    return HttpResponse(json.dumps({ 'success': True }))
  else:
    return HttpResponse(json.dumps({ 'success': False }))

@csrf_exempt
@login_required
def get_site_settings(request):

  site_settings = SiteSettings.load()
  data = {
    'siteBranding': site_settings.site_branding,
    'username': request.user.username
  }

  return HttpResponse(json.dumps(data))
