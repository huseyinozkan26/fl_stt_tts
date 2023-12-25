from django.urls import path
from .views import SpeechRecognitionView, TestSpeechRecognitionFormView, TestMicSpeechForm,TestMaterial, PostMaterial

urlpatterns = [
    path('api/speech-recognition/', SpeechRecognitionView.as_view(), name='speech-recognition-api'),
    path('test-speech-recognition/', TestSpeechRecognitionFormView.as_view(), name='test-speech-recognition'),
    path('test-mic-speech/', TestMicSpeechForm.as_view(), name='Test-mic-speech'),
    path('test-material/', TestMaterial.as_view(), name='Test-material'),
    path('post-material/', PostMaterial.as_view(), name='Test-material'),
]