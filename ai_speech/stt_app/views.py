import subprocess
import tempfile
import os
import difflib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views import View
import shutil
import uuid
from django.conf import settings

class SpeechRecognitionView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        audio_file = request.FILES['audio']
        submitted_text = request.POST.get('correct_text', '')  # Formdan gelen doğru metin
        
        audio_data = audio_file.read()

         # Ses verisini geçici bir dosyaya kaydet
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name
            
        print("Dosya Başarıyla Kaydedildi:", temp_audio_file_path)

        # Rastgele bir isim oluştur
        random_filename = f"{str(uuid.uuid4())}.wav"

        # Ses dosyasını STATIC_ROOT'a taşı
        static_audio_file_path = os.path.join(settings.STATIC_ROOT, random_filename)
        shutil.move(temp_audio_file_path, static_audio_file_path)

        transcribed_text = self.transcribe(static_audio_file_path)

        accuracy = self.calculate_accuracy(transcribed_text, submitted_text)

        print(temp_audio_file_path)
        #os.remove(temp_audio_file_path)

        response = Response({'text': transcribed_text, 'accuracy': accuracy}, status=status.HTTP_200_OK)
         # CORS başlıklarını elle ekleyin
        response["Access-Control-Allow-Origin"] = "https://etfo.tfo.k12.tr"
        response["Access-Control-Allow-Methods"] = "GET, POST"
        response["Access-Control-Allow-Headers"] = "Content-Type"

        return response

    def transcribe(self, audio_file_path):
        # DeepSpeech komutunu oluşturun
        command = [
            "deepspeech",
            "--model", "../dsmodel/deepspeech-0.9.3-models.pbmm",
            "--scorer", "../dsmodel/deepspeech-0.9.3-models.scorer",
            "--audio", audio_file_path
        ]
        print(command)
        # deepspeech komutunu çalıştırın
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()

        # Çıktıyı UTF-8'e çevirin
        text = output.decode('utf-8')
        print(f"Okunan: {text}")
        return text

    def calculate_accuracy(self, transcribed_text, submitted_text):
        # Doğru metin ve transkript metin arasındaki benzerlik oranını hesapla
        seq = difflib.SequenceMatcher(None, transcribed_text, submitted_text)
        similarity_ratio = seq.ratio()

        # Yüzde doğruluk oranını yuvarla ve yüzde olarak döndür
        accuracy = round(similarity_ratio * 100, 2)
        print(accuracy)
        #%30 altında gelen değer durumunda 0 dönsün
        if(accuracy < 30):
            accuracy = 0
        else:
            accuracy = accuracy + 10
            if(accuracy > 100):
                accuracy = 100
        return accuracy

        
class TestSpeechRecognitionFormView(View):
    template_name = 'test_speech_recognition.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Burada işlemleri gerçekleştirin (API'ye istek gönderme, sonuçları işleme, vs.)
        # Şu an sadece basit bir JSON yanıt döndürüyoruz
        return JsonResponse({'message': 'Form gönderimi başarılı!'})
    

class TestMicSpeechForm(View):
    template_name = 'test_mic_speech.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class TestMaterial(View):
    template_name = 'test_material/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(csrf_exempt, name='dispatch')
class PostMaterial(View):
    template_name = 'test_material/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Gelen POST verilerini al
        post_data = request.POST

        # Gelen POST verilerini ekrana yazdır
        for key, value in post_data.items():
            # Eğer dosya mevcutsa içeriğini al ve ekrana yazdır
            if key == "Filename":
                print(post_data)
                file_path = os.path.join('static', 'xml', value)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as xml_file:
                        xml_content = xml_file.read()
                        print(f'XML File Content:\n{xml_content}')

                    # XML içeriğini bir dosyaya yaz
                    output_file_path = os.path.join('static', 'xml', 'output.xml')
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(xml_content)

                    print(f'XML Content has been saved to: {output_file_path}')
            else:
                print(f'{key}: {value}')

        return render(request, self.template_name, {'post_data': post_data})