
import datetime, re

from django.contrib.auth.models import User
from django.db import models

import markdown

from jfmario_django.model_fields import JsonField
from jfmario_django.models import SingletonModel

from jfmario_python3.markdown.extensions import SpectreCssExtension

DEFAULT_MARKDOWN_EXTENSIONS = [
  'markdown.extensions.abbr',
  'markdown.extensions.extra',
  'markdown.extensions.fenced_code',
  'markdown.extensions.tables',
  SpectreCssExtension()
]

class SiteSettings(SingletonModel):

  SITE_BRANDING_DEFAULT = 'Scoreboard'
  WELCOME_TITLE_DEFAULT = 'Welcome to the Scoreboard'
  WELCOME_MESSAGE_DEFAULT = "Please come on in and register for a competition."

  site_branding = models.CharField(max_length=32, default=SITE_BRANDING_DEFAULT)
  welcome_title = models.CharField(max_length=64, default=WELCOME_TITLE_DEFAULT)
  welcome_message = models.TextField(
    default=WELCOME_MESSAGE_DEFAULT,
    help_text="Markdown Field"
  )

  class Meta:
    verbose_name_plural = "Site Settings"

  def __str__(self):
    return "Site Settings"

  @property
  def welcome_message_html(self):
    return markdown.markdown(self.welcome_message,
      extensions=DEFAULT_MARKDOWN_EXTENSIONS)


class Challenge(models.Model):

  STATUS_DRAFT = 0
  STATUS_EXPERIMENTAL = 1
  STATUS_PUBLISHED = 2

  STATUS_CHOICES = [
    (STATUS_DRAFT, "Draft"),
    (STATUS_EXPERIMENTAL, "Experimental"),
    (STATUS_PUBLISHED, "Published")
  ]

  QUESTION_TYPE_SHORT_ANSWER = 0
  QUESTION_TYPE_MULTIPLE_CHOICE = 1
  QUESTION_TYPE_REGEX = 2

  QUESTION_TYPE_CHOICES = [
    (QUESTION_TYPE_SHORT_ANSWER, "Short Answer"),
    (QUESTION_TYPE_MULTIPLE_CHOICE, "Multiple Choice"),
    (QUESTION_TYPE_REGEX, "Regular Expression")
  ]

  REGEX_INPUT_TYPE_TEXT = 0
  REGEX_INPUT_TYPE_TEXT_AREA = 1

  REGEX_INPUT_TYPE_CHOICES = [
    (REGEX_INPUT_TYPE_TEXT, "Text"),
    (REGEX_INPUT_TYPE_TEXT_AREA, "Textarea")
  ]

  MULTIPLE_CHOICE_OPTIONS_DEFAULT = "Option 1\nOption 2\nOption3\nOption4"

  backend_name = models.CharField(
    max_length=64,
    help_text="Verbose name for admin use."
  )
  name = models.CharField(max_length=64)
  status = models.IntegerField(choices=STATUS_CHOICES, default=0)
  question = models.TextField(help_text="Markdown Field")
  hint = models.TextField(blank=True, help_text="Markdown Field", null=True)
  question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES, default=0)
  short_answer = models.CharField(
    blank=True,
    max_length=128,
    null=True,
    help_text="Use for 'Short Answer' and 'Multiple Choice' questions."
  )
  multiple_choice_options = models.TextField(
    blank=True,
    default=MULTIPLE_CHOICE_OPTIONS_DEFAULT,
    help_text="Put one choice per line.",
    null=True
  )
  regex_input_type = models.IntegerField(
    choices=REGEX_INPUT_TYPE_CHOICES,
    default=0,
    help_text="How should users input their answers for 'Regular Expression' questions?"
  )
  regex_answer = models.CharField(
    blank=True,
    max_length=128,
    null=True,
    help_text="Regular expression to test answer against for 'Regular Expression' questions."
  )
  points = models.IntegerField(default=10)
  hint_cost = models.IntegerField(default=2)
  wrong_answer_cost = models.IntegerField(default=1)
  challenge_unlock_min_points = models.IntegerField(default=0)
  challenge_unlock_dependencies = models.ManyToManyField(
    'self',
    blank=True,
    symmetrical=False
  )
  data_file = models.FileField(
    blank=True,
    help_text="If the challenges needs multiple files, zip them up.",
    null=True,
    upload_to='uploads/%Y/%m/%d/'
  )

  def __str__(self):
    return self.backend_name

  @property
  def html_question(self):
    return markdown.markdown(self.question,
      extensions=DEFAULT_MARKDOWN_EXTENSIONS)
  @property
  def html_hint(self):
    if self.hint:
      return markdown.markdown(self.hint,
        extensions=DEFAULT_MARKDOWN_EXTENSIONS)
    return None
  @property
  def string_question_type(self):
    if (self.question_type == 0):
      return 'ShortAnswer'
    if (self.question_type == 1):
      return 'MultipleChoice'
    if (self.question_type == 2):
      if (self.regex_input_type == 0):
        return 'ShortAnswer'
      else:
        return 'TextAnswer'
  @property
  def list_multiple_choice_options(self):
    return [o.strip() for o in self.multiple_choice_options.split('\n')]

  def is_visible_to_user(self, upr):

    if upr.competition.status == 'NOT_STARTED':
      return False
    if self.status < 1:
      return False
    if self.challenge_unlock_min_points > 0 and self.challenge_unlock_min_points > upr.score:
      return False
    elif len(list(self.challenge_unlock_dependencies.all())) == 0:
      return True
    else:
      for c in self.challenge_unlock_dependencies.all():
        if c not in upr.challenges_solved.all():
          return False
    return True

  def check_answer(self, answer):
    if self.question_type <= 1:
      return (answer == self.short_answer)
    else:
      return (re.match(self.regex_answer, answer))

class ChallengeGroup(models.Model):

  backend_name = models.CharField(
    max_length=64,
    help_text="Verbose name for admin use."
  )
  name = models.CharField(max_length=64)
  description = models.TextField(help_text="Markdown Field")
  challenges = models.ManyToManyField(Challenge)

  def __str__(self):
    return self.backend_name

  def has_challenge(self, challenge):
    if challenge in self.challenges.all():
      return True
    return False

  def get_max_score(self):
    return sum([c.points for c in self.challenges.all()])

class CompetitionSchema(models.Model):

  backend_name = models.CharField(
    max_length=64,
    help_text="Verbose name for admin use."
  )
  name = models.CharField(max_length=64)
  default_description = models.TextField(help_text="Markdown Field")
  default_welcome_message = models.TextField(help_text="Markdown Field")
  challenge_groups = models.ManyToManyField(ChallengeGroup)

  def __str__(self):
    return self.backend_name

  def has_challenge(self, challenge):
    for group in self.challenge_groups.all():
      if group.has_challenge(challenge):
        return True
    return False

  def get_max_score(self):
    return sum([cg.get_max_score() for cg in self.challenge_groups.all()])

class Competition(models.Model):

  backend_name = models.CharField(
    max_length=64,
    help_text="Verbose name for admin use."
  )
  name = models.CharField(max_length=64)
  use_custom_description = models.BooleanField(
    default=False,
    help_text="If unchecked, description from the competition schema will be used."
  )
  custom_description = models.TextField(blank=True, help_text="Markdown Field", null=True)
  use_custom_welcome_message = models.BooleanField(
    default=False,
    help_text="If unchecked, welcome message from the competition schema will be used."
  )
  custom_welcome_message = models.TextField(blank=True, help_text="Markdown Field", null=True)
  schema = models.ForeignKey(CompetitionSchema, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  is_open = models.BooleanField(
    default=True,
    help_text="If unchecked, users will be unable to register for this or access this unless they are already assigned to this."
  )
  users = models.ManyToManyField(User, blank=True)

  def __str__(self):
    return self.backend_name

  @property
  def description(self):
    if (self.use_custom_description):
      return self.custom_description
    else:
      return self.schema.default_description
  @property
  def welcome_message(self):
    if (self.use_custom_welcome_message):
      return self.custom_welcome_message
    else:
      return self.schema.default_welcome_message
  @property
  def html_description(self):
    return markdown.markdown(self.description,
      extensions=DEFAULT_MARKDOWN_EXTENSIONS)
  @property
  def html_welcome_message(self):
    return markdown.markdown(self.welcome_message,
      extensions=DEFAULT_MARKDOWN_EXTENSIONS)

  @property
  def status(self):
    now = datetime.datetime.now(datetime.timezone.utc)
    if self.start_time > now:
      return 'NOT_STARTED'
    if self.end_time < now:
      return 'OVER'
    else:
      return 'ACTIVE'

class UserParticipationRecord(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
  challenges_solved = models.ManyToManyField(Challenge, blank=True, null=True)
  hints_purchased = models.ManyToManyField(Challenge, blank=True, related_name='hint_purchasers')
  score = models.IntegerField(default=0)
  wrong_answers = JsonField(blank=True, null=True)

  def __str__(self):
    return "{} in {}".format(self.user, self.competition)

  def purchase_hint(self, challenge):
    if self.competition.schema.has_challenge(challenge) and challenge.hint:
      self.score -= challenge.hint_cost
      self.hints_purchased.add(challenge)
      return True
    else:
      return False

  def mark_solved(self, challenge):
    if self.competition.schema.has_challenge(challenge):
      self.score += challenge.points
      self.challenges_solved.add(challenge)

  def mark_incorrect(self, challenge, answer):
    if self.competition.schema.has_challenge(challenge):
      self.score -= challenge.wrong_answer_cost
      if not self.wrong_answers:
        self.wrong_answers = {}
      if str(challenge.pk) not in self.wrong_answers:
        self.wrong_answers[str(challenge.pk)] = []
      self.wrong_answers[str(challenge.pk)].append(answer)

  def get_wrong_answers(self, challenge):
    if not self.wrong_answers:
      self.wrong_answers = {}
    if str(challenge.pk) not in self.wrong_answers:
      self.wrong_answers[str(challenge.pk)] = []
    return self.wrong_answers[str(challenge.pk)]
