from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import os

# Folder containing the audio files
folder_path = 'sentences'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to process an audio file


def process_audio_file(audio_path):
    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)

    # Split the audio file into chunks at silence (or pause)
    chunks = split_on_silence(audio, min_silence_len=200, silence_thresh=-40)

    # Extract original filename without extension
    original_filename = os.path.splitext(os.path.basename(audio_path))[0]

    # Process each chunk with speech recognition
    words = []
    for i, chunk in enumerate(chunks):
        # Export chunk to wav
        chunk_path = f'{folder_path}/{original_filename}_chunk{i}.wav'
        chunk.export(chunk_path, format="wav")

        # Recognize the chunk
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            try:
                # Attempt to recognize speech in the chunk
                text = recognizer.recognize_google(audio_data)
                words.append(text)
            except sr.UnknownValueError:
                # Speech was not understood
                words.append("[Unintelligible]")
            except sr.RequestError as e:
                # Could not request results from the service
                words.append(f"[Error: {e}]")

    return words


# Process all WAV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):
        audio_path = os.path.join(folder_path, filename)
        words = process_audio_file(audio_path)
        print(f"Words from {filename}: {words}")
