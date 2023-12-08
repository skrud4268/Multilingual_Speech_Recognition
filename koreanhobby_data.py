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
english_phrase = "is my hobby"

# Korean hobbys
korean_hobbies = [
    "독서", "등산", "요리", "베이킹", "사진 촬영", "그림 그리기", "뜨개질", "캘리그라피", "원예", "낚시",
    "볼링", "테니스", "골프", "수영", "스쿠버 다이빙", "스키", "스노보드", "서핑", "바둑", "체스",
    "요가", "필라테스", "헬스", "조깅", "산책", "자전거 타기", "인라인 스케이트", "보드 게임", "퍼즐", "마술",
    "영화 감상", "연극 관람", "콘서트 가기", "미술관 방문", "박물관 탐방", "여행", "캠핑", "백패킹", "로드 트립", "크루즈 여행",
    "동물 관찰", "새 관찰", "천체 관측", "화석 수집", "우표 수집", "동전 수집", "앤티크 수집", "모델 만들기", "RC카", "드론 조종",
    "컴퓨터 게임", "보드 게임", "퍼즐 게임", "카드 게임", "테이블탑 RPG", "VR 게임", "프로그래밍", "웹 디자인", "그래픽 디자인", "애니메이션 제작",
    "비디오 제작", "블로깅", "팟캐스팅", "음악 감상", "악기 연주", "노래 부르기", "랩", "DJing", "작곡", "춤",
    "무술", "복싱", "태권도", "합기도", "주짓수", "검도", "아처리", "마라톤", "트라이애슬론", "크로스핏",
    "서예", "종이 접기", "도예", "조각", "가죽 공예", "목공", "금속 공예", "유리 공예", "캔들 만들기", "비누 만들기", "와인 시음", "커피 감별", "스케이트보딩", "자동차 튜닝", "드론 레이싱", "스페이스 모델링", "VR 체험", "퀼트 만들기", "저글링", "킥복싱"
]

# Ensure the segments and sentences folder exists
os.makedirs('segments', exist_ok=True)
os.makedirs('sentences', exist_ok=True)

# List to store CSV data
csv_data = []

# Silent segment of 400 milliseconds
silent_segment = AudioSegment.silent(duration=400)

# Process each Korean hobbies
for index, hobby in enumerate(korean_hobbies):
    # Create the full sentence
    sentence = f"{english_phrase} {hobby}"
    
    # Split the sentence into words
    words = sentence.split()

    # Initialize an empty audio segment for the sentence
    sentence_audio = AudioSegment.empty()

    # Process each word
    for word_index, word in enumerate(words):
        filename = f"segments/korean_hobby_{index+1}_chunk_{word_index+1}.wav"
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
    sentence_audio.export(f"sentences/korean_hobby_sentence_{index+1}.wav", format="wav")

# Write data to CSV file
with open('korean_hobby_labels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Language"])
    writer.writerows(csv_data)

