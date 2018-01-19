
from main.models import UserParticipationRecord

def get_user_participation_record(user, competition):

  try:
    upr = UserParticipationRecord.objects.get(user=user, competition=competition)
    return upr
  except:
    if user in competition.users.all():
      upr = UserParticipationRecord(user=user, competition=competition)
      upr.save()
      return upr
    else:
      return None

def get_visible_challenge_list(upr):

  lst = []

  for challenge_group in upr.competition.schema.challenge_groups.all():

    challenges = []

    for challenge in challenge_group.challenges.all():

      if challenge.is_visible_to_user(upr):
        challenge_dict = {
          'id': challenge.pk,
          'name': challenge.name,
          'status': challenge.status,
          'points': challenge.points
        }
        challenges.append(challenge_dict)

    if len(challenges):
      obj = { 'group': challenge_group.name }
      obj['challenges'] = challenges
      lst.append(obj)

  return lst
