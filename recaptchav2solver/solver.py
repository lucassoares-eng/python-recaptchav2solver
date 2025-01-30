import os
import random
import shutil
import time
import requests
import zipfile
import speech_recognition as sr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
# Suprimir o aviso específico emitido pelo pydub
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", category=RuntimeWarning)
from pydub import AudioSegment

class ReCAPTCHASolver:
    """A class to solve reCAPTCHA challenges using audio transcription."""

    FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    FFMPEG_DIR = "ffmpeg"

    def __init__(self):
        """Initialize the ReCAPTCHASolver and set up FFmpeg."""
        self._setup_ffmpeg()

    def _setup_ffmpeg(self):
        """Download and configure FFmpeg if not already installed."""
        ffmpeg_exe = os.path.join(self.FFMPEG_DIR, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_exe):
            print("Downloading FFmpeg...")
            zip_path = os.path.join(self.FFMPEG_DIR, "ffmpeg.zip")
            os.makedirs(self.FFMPEG_DIR, exist_ok=True)
            
            # Baixar o arquivo ZIP
            response = requests.get(self.FFMPEG_URL)
            with open(zip_path, "wb") as file:
                file.write(response.content)

            # Extrair o conteúdo para uma pasta temporária
            temp_extract_dir = os.path.join(self.FFMPEG_DIR, "temp_ffmpeg")
            os.makedirs(temp_extract_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_extract_dir)

            # Identificar a pasta extraída (de nome variável, tipo "ffmpeg-7.1-essentials_build")
            extracted_folders = [f for f in os.listdir(temp_extract_dir) if os.path.isdir(os.path.join(temp_extract_dir, f))]
            if extracted_folders:
                extracted_path = os.path.join(temp_extract_dir, extracted_folders[0])
                
                # Mover todo o conteúdo da pasta extraída para FFMPEG_DIR
                for item in os.listdir(extracted_path):
                    shutil.move(os.path.join(extracted_path, item), self.FFMPEG_DIR)

            # Limpar arquivos temporários
            shutil.rmtree(temp_extract_dir)
            os.remove(zip_path)

        if not os.path.exists(ffmpeg_exe):
            raise FileNotFoundError("FFmpeg setup failed.")
        
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_exe)
        AudioSegment.converter = ffmpeg_exe
        print('FFmpeg successfully configured!')

    def _convert_to_wav(self, input_path, output_path="converted_audio.wav"):
        """Convert audio to WAV format."""
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        return output_path

    def _download_audio(self, audio_url, save_path):
        """Download audio from a given URL."""
        response = requests.get(audio_url)
        with open(save_path, "wb") as file:
            file.write(response.content)
        return save_path

    def _transcribe_audio(self, audio_path):
        """Transcribe audio using Google's Speech Recognition."""
        recognizer = sr.Recognizer()
        if not audio_path.endswith(".wav"):
            audio_path = self._convert_to_wav(audio_path)
        with sr.AudioFile(audio_path) as source:
            return recognizer.recognize_google(recognizer.record(source))

    def solve_recaptcha(self, driver):
        """
        Solve a reCAPTCHA challenge on the given Selenium WebDriver instance.

        Args:
            driver: A Selenium WebDriver instance.

        Raises:
            RuntimeError: If an error occurs during the reCAPTCHA solving process.
        """
        try:
            wait = WebDriverWait(driver, 5)

            # Switch to the reCAPTCHA iframe
            iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://www.google.com/recaptcha/api2/bframe')]")))
            driver.switch_to.frame(iframe)

            # Click the audio challenge button
            audio_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button")))
            audio_button.click()

            # Download and transcribe the audio
            audio_source = wait.until(EC.presence_of_element_located((By.ID, "audio-source"))).get_attribute("src")
            audio_path = self._download_audio(audio_source, "recaptcha_audio.mp3")
            response = self._transcribe_audio(audio_path)

            # Enter the transcribed text into the response input
            audio_response_input = wait.until(EC.presence_of_element_located((By.ID, "audio-response")))
            for char in response:
                audio_response_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.5))

            # Click the verify button
            verify_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button")))
            verify_button.click()

            driver.switch_to.default_content()

        except Exception as e:
            driver.switch_to.default_content()
            raise RuntimeError(f"Error solving reCAPTCHA: {str(e)}")