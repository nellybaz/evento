from django import forms
from .models import Jobs



class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['invite_file', 'invitees']
        # exclude = ['invitees']