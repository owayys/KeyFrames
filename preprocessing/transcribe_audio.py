import assemblyai as aai
import time
import os
from dotenv import load_dotenv
load_dotenv()
print("ASSEMBLYAI_API_KEY", os.environ["ASSEMBLYAI_API_KEY"])
aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]


def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    print("Transcribing Video...")
    start_time = time.time()
    transcript = transcriber.transcribe(file_path)
    print("Transcription Complete. Took --- %s seconds ---" %
          (time.time() - start_time))
    return transcript.text
