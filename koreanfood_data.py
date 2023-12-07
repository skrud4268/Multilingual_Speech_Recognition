import subprocess
import os
import csv
from pydub import AudioSegment


def text_to_aiff_to_wav(text, wav_filename, voice, folder='wav_files', pause_duration=0.5):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Convert text to speech and save as AIFF
    aiff_filename = os.path.join(folder, wav_filename.replace('.wav', '.aiff'))
    command = ['say', '-v', voice, '-o', aiff_filename, text]
    subprocess.run(command)

    # Convert AIFF to WAV
    wav_filepath = os.path.join(folder, wav_filename)
    subprocess.run(['ffmpeg', '-i', aiff_filename, wav_filepath])

    # Remove AIFF file
    os.remove(aiff_filename)

    # Add pause
    if pause_duration > 0:
        add_pause_to_wav(wav_filepath, pause_duration)


def add_pause_to_wav(wav_file, duration_seconds):
    silence = AudioSegment.silent(duration=duration_seconds * 400)
    sound = AudioSegment.from_wav(wav_file)
    combined = sound + silence
    combined.export(wav_file, format='wav')


def combine_wav_files(files, output_file, folder='wav_files'):
    combined = AudioSegment.empty()
    for file in files:
        wav_path = os.path.join(folder, file)
        combined += AudioSegment.from_wav(wav_path)

    combined.export(os.path.join(folder, output_file), format='wav')


# English words
english_words = ["i", "like", "to", "eat"]
for word in english_words:
    text_to_aiff_to_wav(word, f"{word}.wav", "Samantha")

# Korean foods
korean_foods = [
    "김치찌개", "불고기", "비빔밥", "삼겹살", "갈비", "된장찌개", "순두부찌개", "감자탕", "닭갈비", "제육볶음",
    "김밥", "떡볶이", "순대", "오뎅", "피자떡볶이", "치즈떡볶이", "해물파전", "김치전", "계란말이", "감자전",
    "잡채", "부대찌개", "닭도리탕", "고등어구이", "삼계탕", "김치볶음밥", "새우볶음밥", "오징어볶음", "돼지불백", "고추장불고기",
    "콩나물국밥", "갈비탕", "설렁탕", "육개장", "해장국", "북엇국", "만두국", "갈비찜", "약식", "녹두전",
    "김치부침개", "호박전", "곱창구이", "불닭", "안동찜닭", "칼국수", "잔치국수", "비빔국수", "콩국수", "냉면",
    "돼지국밥", "두부김치", "백김치", "열무김치", "오이소박이", "콩나물무침", "시금치나물", "오징어순대", "명태회무침", "고추잡채",
    "해물탕", "삼치구이", "꽁치구이", "매운탕", "멸치볶음", "볶음우동", "잡탕밥", "쭈꾸미볶음", "낙지볶음", "해물순두부",
    "찜닭", "족발", "보쌈", "막걸리", "소주", "매실주", "동동주", "인삼주", "배추김치", "갓김치",
    "깻잎김치", "총각김치", "갈치구이", "갈치조림", "고등어조림", "아귀찜", "아귀탕", "대구탕", "황태구이", "홍어삼합", "배추된장국", "두부조림", "마늘종볶음", "멸치국수", "오징어볶음밥", "양념치킨", "간장게장", "양배추김치", "떡만두국", "김치만두"
]
for index, food in enumerate(korean_foods, start=1):
    text_to_aiff_to_wav(food, f"korean_food_{index}.wav", "Yuna")

# Generate combined sentences and CSV entries
csv_entries = []

# Add entries for English words
for word in english_words:
    csv_entries.append([f"{word}.wav", 'English', word])

# Add entries for Korean foods
for index, food in enumerate(korean_foods, start=1):
    csv_entries.append([f"korean_food_{index}.wav", 'Korean', food])

# Generate and add entries for combined sentences
for index, food in enumerate(korean_foods, start=1):
    combined_filename = f"I_like_to_eat_korean_food_{index}.wav"
    files = [f"{word}.wav" for word in english_words] + \
        [f"korean_food_{index}.wav"]
    combine_wav_files(files, combined_filename)
    combined_sentence = " ".join(english_words) + " " + food
    csv_entries.append([combined_filename, 'Mixed', combined_sentence])

# Write to CSV
with open('audio_segments.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Language', 'Text'])
    for entry in csv_entries:
        writer.writerow(entry)

print("Dataset creation and CSV file generation completed.")
