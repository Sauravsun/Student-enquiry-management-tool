# forms.py

from django import forms
from .models import knrregistraion

class knrregistraionForm(forms.ModelForm):
    class Meta:
        model = knrregistraion
        fields = ['fname', 'lname', 'place', 'qualification', 'fathername', 'mothername', 'course', 'coursefee', 'amountpaid', 'dop', 'mod']
