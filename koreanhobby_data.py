import subprocess
import os
import csv
from pydub import AudioSegment


def text_to_aiff_to_wav(text, wav_filename, voice, folder='wav_files3', pause_duration=0.5):
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


def combine_wav_files(files, output_file, folder='wav_files3'):
    combined = AudioSegment.empty()
    for file in files:
        wav_path = os.path.join(folder, file)
        combined += AudioSegment.from_wav(wav_path)

    combined.export(os.path.join(folder, output_file), format='wav')


# English words
english_words = ["is", "my", "favorite", "hobby"]
for word in english_words:
    text_to_aiff_to_wav(word, f"{word}.wav", "Samantha")

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

for index, hobby in enumerate(korean_hobbies, start=1):
    text_to_aiff_to_wav(hobby, f"korean_hobby_{index}.wav", "Yuna")

# Generate combined sentences and CSV entries
csv_entries = []

# Add entries for English words
for word in english_words:
    csv_entries.append([f"{word}.wav", 'English', word])

# Add entries for Korean hobbys
for index, hobby in enumerate(korean_hobbies, start=1):
    csv_entries.append([f"korean_hobby_{index}.wav", 'Korean', hobby])

# Generate and add entries for combined sentences
for index, hobby in enumerate(korean_hobbies, start=1):
    combined_filename = f"korean_hobby_sentence_{index}.wav"
    files = [f"korean_hobby_{index}.wav"] + \
        [f"{word}.wav" for word in english_words]
    combine_wav_files(files, combined_filename)
    combined_sentence = hobby + " ".join(english_words) + " "
    csv_entries.append([combined_filename, 'Mixed', combined_sentence])

# Write to CSV
with open('wav_labels3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Language', 'Text'])
    for entry in csv_entries:
        writer.writerow(entry)

print("Dataset creation and CSV file generation completed.")
