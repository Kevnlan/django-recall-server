from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from recall_server.config import settings

# from recall_server.county.models import County


class VoteChoices(models.TextChoices):
    YES = 'yes', 'Yes'
    NO = 'no', 'No'
    ABSTAIN = 'abstain', 'Abstain'


class Legislator(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    @property
    def voting_history(self):
        content_type = ContentType.objects.get_for_model(self)
        return OfficialVote.objects.filter(
                legislator_content_type=content_type,
                legislator_object_id=self.id
                )


class PublicVote(models.Model):
    bill = models.ForeignKey(
            'laws.Bill',
            on_delete=models.CASCADE
            )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.CharField(
            max_length=10,
            choices=VoteChoices.choices
            )
    comment = models.TextField()
    region = models.ForeignKey(
            'county.County', 
            on_delete=models.CASCADE
            )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.user}: {self.bill} {self.vote}"


class OfficialVote(models.Model):
    bill = models.ForeignKey(
            'laws.Bill',
            on_delete=models.CASCADE
            )
    legislator_content_type = models.ForeignKey(
            ContentType,
            on_delete=models.CASCADE
            )
    legislator_object_id = models.PositiveIntegerField()
    legislator = GenericForeignKey(
            'legislator_content_type',
            'legislator_object_id'
            )
    vote = models.CharField(
            max_length=10,
            choices=VoteChoices.choices
            )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.bill}: {self.vote}"
