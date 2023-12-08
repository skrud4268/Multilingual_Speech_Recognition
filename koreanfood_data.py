import subprocess
import os
import csv
from pydub import AudioSegment

def text_to_aiff_to_wav(text, filename, voice):
    # Convert text to aiff file using macOS say command
    aiff_file = f"{filename}.aiff"
    subprocess.run(['say', '-v', voice, '-o', aiff_file, text])

    # Convert aiff file to wav file
    AudioSegment.from_file(aiff_file).export(filename, format="wav")

    # Clean up the aiff file
    os.remove(aiff_file)

# English phrase
english_phrase = "i like to eat"

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

# Ensure the segments and sentences folder exists
os.makedirs('segments', exist_ok=True)
os.makedirs('sentences', exist_ok=True)

# List to store CSV data
csv_data = []

# Silent segment of 400 milliseconds
silent_segment = AudioSegment.silent(duration=400)

# Process each Korean food
for index, food in enumerate(korean_foods):
    # Create the full sentence
    sentence = f"{english_phrase} {food}"
    
    # Split the sentence into words
    words = sentence.split()

    # Initialize an empty audio segment for the sentence
    sentence_audio = AudioSegment.empty()

    # Process each word
    for word_index, word in enumerate(words):
        filename = f"segments/korean_food_{index+1}_chunk_{word_index+1}.wav"
        text_to_aiff_to_wav(word, filename, "Yuna")

        # Load the word audio
        word_audio = AudioSegment.from_wav(filename)

        # Concatenate word audio to the sentence audio
        sentence_audio += word_audio + silent_segment

        # Determine the language of the word
        language = "English" if word in english_phrase else "Korean"

        # Add filename and language to CSV data
        csv_data.append([filename, language])

    # Export the sentence audio
    sentence_audio.export(f"sentences/korean_food_sentence_{index+1}.wav", format="wav")

# Write data to CSV file
with open('korean_food_labels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Language"])
    writer.writerows(csv_data)

