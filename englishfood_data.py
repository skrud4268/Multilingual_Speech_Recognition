import subprocess
import os
import csv
from pydub import AudioSegment


def text_to_aiff_to_wav(text, wav_filename, voice, folder='wav_files2', pause_duration=0.5):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Convert text to speech and save as AIFF
    aiff_filename = os.path.join(folder, wav_filename.replace('.wav', '.aiff'))
    command = ['say', '-v', voice, '-o', aiff_filename, text]
    subprocess.run(command)

    # Convert AIFF to WAV
    wav_filepath = os.path.join(folder, wav_filename)
    subprocess.run(['ffmpeg', '-i', aiff_filename, '-ar',
                   '22050', '-ac', '1', wav_filepath])

    # Remove the AIFF file
    os.remove(aiff_filename)

    # Add pause
    if pause_duration > 0:
        add_pause_to_wav(wav_filepath, pause_duration)


def add_pause_to_wav(wav_file, duration_seconds):
    silence = AudioSegment.silent(duration=duration_seconds * 400)
    sound = AudioSegment.from_wav(wav_file)
    combined = sound + silence
    combined.export(wav_file, format='wav')


def is_last_letter_vowel(word):
    vowels = "aeiou"
    return word[-1] in vowels


def combine_wav_files(files, output_file, folder='wav_files2'):
    combined = AudioSegment.empty()
    for file in files:
        wav_path = os.path.join(folder, file)
        combined += AudioSegment.from_wav(wav_path)

    combined.export(os.path.join(folder, output_file), format='wav')


# Korean words with English descriptions
korean_entries = []
korean_words = {
    "나는": "naneun",
    "을": "eul",
    "를": "reul",
    "좋아합니다": "joahapnida"
}
for korean_word, english_desc in korean_words.items():
    wav_filename = f"{english_desc}.wav"
    text_to_aiff_to_wav(korean_word, wav_filename,
                        voice='Yuna', pause_duration=0.5)
    korean_entries.append([wav_filename, 'Korean', korean_word])

# English food names
english_entries = []
english_foods = [
    "Pizza", "Hamburger", "Pasta", "Sushi", "Taco", "Salad", "Steak", "Curry", "Bagel", "Bread",
    "Apple Pie", "Roast Beef", "Fried Chicken", "Fish and Chips", "Bacon and Eggs", "Pancakes", "Waffles", "Burrito", "Lasagna", "Spaghetti Bolognese",
    "Caesar Salad", "Shepherd's Pie", "Cottage Pie", "Beef Stew", "Pot Roast", "Turkey Sandwich", "Club Sandwich", "Hot Dog", "Barbecue Ribs", "Pulled Pork",
    "Cornbread", "Macaroni and Cheese", "Grits", "Clam Chowder", "Lobster Roll", "Biscuits and Gravy", "Chicken and Waffles", "Nachos", "Quesadilla", "Enchiladas",
    "Tortilla Soup", "Fajitas", "Chicken Alfredo", "Beef Wellington", "Yorkshire Pudding", "Sunday Roast", "Corned Beef Hash", "Eggs Benedict", "Meatloaf", "Potato Salad",
    "Coleslaw", "Jambalaya", "Gumbo", "Po' Boy", "Crawfish Boil", "Baked Beans", "Chicken Pot Pie", "Buffalo Wings", "Chicken Tenders", "Onion Rings",
    "French Fries", "Mashed Potatoes", "Grilled Cheese Sandwich", "BLT Sandwich", "Philly Cheesesteak", "Reuben Sandwich", "Poutine", "Bangers and Mash", "Fish Pie", "Welsh Rarebit",
    "Scotch Eggs", "Cornish Pasty", "Toad in the Hole", "Pea Soup", "Irish Stew", "Cullen Skink", "Haggis", "Black Pudding", "Full English Breakfast", "Banoffee Pie",
    "Trifle", "Eton Mess", "Sticky Toffee Pudding", "Spotted Dick", "Bread and Butter Pudding", "Victoria Sponge Cake", "Scone", "Shortbread", "Crumpet", "Tea Sandwich",  "Deviled Eggs", "Cobb Salad", "Monte Cristo Sandwich", "Chicken Parmesan", "Ratatouille",
    "Beef Stroganoff", "Chili Con Carne", "Eggplant Parmesan", "New England Clam Chowder", "Tiramisu"
]
for food in english_foods:
    wav_filename = f"{food}.wav"
    text_to_aiff_to_wav(food, wav_filename,
                        voice='Samantha', pause_duration=0.5)
    english_entries.append([wav_filename, 'English', food])

# Generate combined sentences
combined_entries = []
counter = 1
for food in english_foods:
    object_particle = "reul" if is_last_letter_vowel(food) else "eul"
    combined_text = f"나는 {food} {object_particle} 좋아합니다"
    combined_filename = f"englishfood_sentence_{counter}.wav"
    files = ["naneun.wav", f"{food}.wav",
             f"{object_particle}.wav", "joahapnida.wav"]
    combine_wav_files(files, combined_filename)
    combined_entries.append([combined_filename, 'Mixed', combined_text])
    counter += 1

# Write to CSV
with open('wav_labels2.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Language', 'Text'])
    for entry in korean_entries + english_entries + combined_entries:
        writer.writerow(entry)

print("WAV files and CSV generated.")
