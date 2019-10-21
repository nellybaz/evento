from django.db import models
from uuid import uuid4
# from multiselectfield import MultiSelectField
from django.utils import timezone
from django.contrib.auth.models import User

class Jobs(models.Model):
    invite_file = models.FileField(upload_to="invite_files")
    invitees = models.FileField(upload_to="invitees")