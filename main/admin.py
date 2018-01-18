from django.contrib import admin
# Register your models here.

from main.models import Challenge, ChallengeGroup, CompetitionSchema
from main.models import Competition, SiteSettings, UserParticipationRecord

admin.site.register(SiteSettings)
admin.site.register(Challenge)
admin.site.register(ChallengeGroup)
admin.site.register(CompetitionSchema)
admin.site.register(Competition)
admin.site.register(UserParticipationRecord)
