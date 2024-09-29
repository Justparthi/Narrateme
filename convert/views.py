from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import fitz  
from gtts import gTTS
import os

def pdf_to_text(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype='pdf')
    text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()

    return text

def text_to_speech(text, audio_path):
    tts = gTTS(text, lang='en')
    tts.save(audio_path)

def upload_pdf(request):
    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            
            if pdf_file.name.endswith('.pdf'):
                try:
                    # Convert PDF to text
                    text = pdf_to_text(pdf_file)
                    
                    # Generate audio from text
                    audio_file_name = 'output.mp3'
                    audio_file_path = os.path.join('static/audio', audio_file_name)
                    text_to_speech(text, audio_file_path)
                    
                    with open(audio_file_path, 'rb') as audio_file:
                        audio_file_content = ContentFile(audio_file.read(), audio_file_name)
                        default_storage.save(audio_file_name, audio_file_content)

                    return render(request, 'index.html', {'text': text, 'audio_file': audio_file_path})

                except Exception as e:
                    return render(request, 'index.html', {'error': f'Error processing PDF file: {e}'})
            else:
                return render(request, 'index.html', {'error': 'Please upload a valid PDF file.'})
        else:
            return render(request, 'index.html', {'error': 'No file uploaded.'})

    return render(request, 'index.html')
