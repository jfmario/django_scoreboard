
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

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
  hint = models.TextField(help_text="Markdown Field")
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
    help_text="Put one choice per line."
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

class Competition(models.Model):

  backend_name = models.CharField(
    max_length=64,
    help_text="Verbose name for admin use."
  )
  name = models.CharField(max_length=64)
  use_custom_description = models.BooleanField(
    help_text="If unchecked, description from the competition schema will be used."
  )
  custom_description = models.TextField(help_text="Markdown Field")
  use_custom_welcome_message = models.BooleanField(
    help_text="If unchecked, welcome message from the competition schema will be used."
  )
  custom_welcome_message = models.TextField(help_text="Markdown Field")
  schema = models.ManyToManyField(CompetitionSchema)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  is_open = models.BooleanField(
    default=True,
    help_text="If unchecked, users will be unable to register for this or access this unless they are already assigned to this."
  )
  users = models.ManyToManyField(User)

  def __str__(self):
    return self.backend_name

class UserParticipationRecord(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
  challenges_solved = models.ManyToManyField(Challenge)
  score = models.IntegerField(default=0)

  def __str__(self):
    return "{} in {}".format(self.user, self.competition)
