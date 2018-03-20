
import datetime, json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import Challenge, Competition, SiteSettings
from main.models import UserParticipationRecord

from main.utils import get_user_participation_record, get_visible_challenge_list

@csrf_exempt
@login_required
def get_challenge(request, competition_id, challenge_id):

  competition = Competition.objects.get(pk=competition_id)
  upr = get_user_participation_record(request.user, competition)

  if not upr:
    return HttpResponse("Unauthorized", status=401)

  challenge = Challenge.objects.get(pk=challenge_id)
  if competition.schema.has_challenge(challenge) and challenge.is_visible_to_user(upr):

    data = {}
    data['name'] = challenge.name
    data['status'] = challenge.status
    data['question'] = challenge.html_question
    data['hint'] = ''
    data['hasHint'] = False

    if challenge.hint:
      data['hasHint'] = True
    data['questionType'] = challenge.string_question_type
    if data['questionType'] == 'MultipleChoice':
      data['choices'] = challenge.list_multiple_choice_options
    data['points'] = challenge.points
    data['hintCost'] = challenge.hint_cost
    data['wrongAnswerCost'] = challenge.wrong_answer_cost
    data['hintPurchased'] = False
    data['solved'] = False

    if challenge in upr.challenges_solved.all():
      data['solved'] = True
    if challenge in upr.hints_purchased.all():
      data['hintPurchased'] = True
      data['hint'] = challenge.html_hint
    if challenge.data_file:
      data['dataFileRef'] = challenge.data_file.url

    data['wrongAnswerHistory'] = upr.get_wrong_answers(challenge)

    return HttpResponse(json.dumps(data))
  else:
    return HttpResponse("Challenge Not Found", status=401)

@csrf_exempt
@login_required
def get_competition_leaderboard(request, competition_id):

  competition = Competition.objects.get(pk=competition_id)

  if competition.status == 'NOT_STARTED':
    return HttpResponse("Competition not started", status=401)

  upr = get_user_participation_record(request.user, competition)

  if not upr:
    return HttpResponse("UPR Not Found", status=401)

  data = {}
  data['maxScore'] = competition.schema.get_max_score()
  data['scores'] = []

  for upr in list(UserParticipationRecord.objects.filter(competition=competition).order_by('-score')):
    data['scores'].append({
      'username': upr.user.username,
      'score': upr.score
    })

  return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def purchase_challenge_hint(request, competition_id, challenge_id):

  competition = Competition.objects.get(pk=competition_id)
  upr = get_user_participation_record(request.user, competition)

  if not upr:
    return HttpResponse("UPR Not Found", status=401)

  challenge = Challenge.objects.get(pk=challenge_id)

  upr.purchase_hint(challenge)
  upr.save()

  return get_challenge(request, competition_id, challenge_id)

@csrf_exempt
@login_required
def submit_challenge_answer(request, competition_id, challenge_id):

  competition = Competition.objects.get(pk=competition_id)
  upr = get_user_participation_record(request.user, competition)

  if not upr:
    return HttpResponse("UPR Not Found", status=401)

  challenge = Challenge.objects.get(pk=challenge_id)
  if competition.schema.has_challenge(challenge) and challenge.is_visible_to_user(upr):
    print(request.body)
    post_data = json.loads(request.body.decode('utf-8'))
    if 'answer' in post_data and competition.status == 'ACTIVE':
      is_correct = challenge.check_answer(post_data['answer'])
      if is_correct:

        upr.mark_solved(challenge)
        upr.save()

        return get_challenge(request, competition_id, challenge_id)
      else:

        upr.mark_incorrect(challenge, post_data['answer'])
        upr.save()

        return get_challenge(request, competition_id, challenge_id)
    else:
      return HttpResponse("Condition not met.", status=400)
  else:
    return HttpResponse("Challenge Not Found", status=400)

@csrf_exempt
@login_required
def competition(request, competition_id):

  competition = Competition.objects.get(pk=competition_id)
  upr = get_user_participation_record(request.user, competition)
  if not upr:
    return HttpResponse("Unauthorized", status_code=401)

  status = competition.status

  data = {}
  data['score'] = upr.score
  data['status'] = status
  data['competition'] = { 'id': competition.pk }
  data['competition']['status'] = status
  data['competition']['name'] = competition.name
  data['competition']['description'] = competition.html_description
  data['competition']['welcome'] = competition.html_welcome_message
  data['competition']['startTime'] = competition.start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
  data['competition']['endTime'] = competition.end_time.strftime('%Y-%m-%dT%H:%M:%S%z')

  if status == 'ACTIVE' or status == 'OVER':
    data['challenges'] = get_visible_challenge_list(upr)

  return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def list_open_competitions(request):

  all_competitions = Competition.objects.filter(is_open=True) | Competition.objects.filter(users__id=request.user.pk)

  print(all_competitions)
  
  data = [{
    'id': c.pk,
    'name': c.name,
    'description': c.html_description,
    'startTime': c.start_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'endTime': c.end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
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
