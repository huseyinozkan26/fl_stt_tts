from django import forms

class SpeechRecognitionForm(forms.Form):
    audio_file = forms.FileField()
