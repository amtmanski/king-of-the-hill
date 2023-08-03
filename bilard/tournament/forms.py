from django import forms
from .models import Player, Event
from django.forms import SelectDateWidget
from datetime import date


class MatchForm(forms.Form):
    winner = forms.ModelChoiceField(queryset=Player.objects.all())
    loser = forms.ModelChoiceField(queryset=Player.objects.all())
    event = forms.ModelChoiceField(queryset=Event.objects.all())

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget(), initial=date.today())
    player_1 = forms.ModelChoiceField(queryset=Player.objects.all())
    player_2 = forms.ModelChoiceField(queryset=Player.objects.all())
    class Meta:
        model = Event
        fields = ['date', 'arena', 'player_1', 'player_2']
        widgets = {
            'arena': forms.Select(
                choices=[
                    ("plaza", "Lucky Star"), 
                    ("tutu", "TuTu"),
                    ("enigma", "Enigma")
                    ], 
                attrs={'class': 'form-control'}
            ),
        }
