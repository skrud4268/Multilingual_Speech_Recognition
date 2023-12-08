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

def is_last_letter_vowel(word):
    vowels = "aeiouAEIOU"
    return word[-1] in vowels

# English hobby names
english_hobbies = [
    "Painting",
    "Gardening",
    "Cooking",
    "Photography",
    "Playing chess",
    "Hiking",
    "Dancing",
    "Playing the guitar",
    "Birdwatching",
    "Origami",
    "Rock climbing",
    "Knitting",
    "Playing basketball",
    "Yoga",
    "Reading",
    "Fishing",
    "Collecting stamps",
    "Playing video games",
    "Sculpting",
    "Calligraphy",
    "Playing tennis",
    "Singing",
    "Model building",
    "Swimming",
    "Horseback riding",
    "Pottery",
    "Astronomy",
    "Playing the piano",
    "Crossword puzzles",
    "Rollerblading",
    "Surfing",
    "Woodworking",
    "Baking",
    "Archery",
    "Geocaching",
    "Playing board games",
    "Mountain biking",
    "Writing poetry",
    "Meditation",
    "Scuba diving",
    "Playing soccer",
    "Genealogy",
    "Fencing",
    "Playing the flute",
    "Coin collecting",
    "Playing volleyball",
    "Tai chi",
    "Canoeing",
    "Playing the drums",
    "Puzzle solving",
    "Beekeeping",
    "Glassblowing",
    "Slacklining",
    "Parkour",
    "Stand-up comedy",
    "Pottery",
    "Ice skating",
    "Astronomy",
    "Martial arts",
    "Wine tasting",
    "Billiards",
    "Magic tricks",
    "Beekeeping",
    "Fossil hunting",
    "Playing the saxophone",
    "Surfing",
    "Urban exploration",
    "Puppetry",
    "Hula hooping",
    "Wine making",
    "Beekeeping",
    "Disc golf",
    "Ghost hunting",
    "Knifemaking",
    "Wine collecting",
    "Skydiving",
    "Cross-stitching",
    "Juggling",
    "Ghost hunting",
    "Beekeeping",
    "Doll making",
    "Scrapbooking",
    "Soap making",
    "Wine tasting",
    "Glass etching",
    "Playing the harp",
    "Archery tag",
    "Puzzle solving",
    "Beekeeping",
    "Gemstone cutting",
    "Candle making",
    "Parkour",
    "RC car racing",
    "Origami",
    "Beekeeping",
    "Collecting vintage toys",
    "Drone racing",
    "Quilting",
    "Knifemaking",
    "Beekeeping"
]


# Ensure the segments folder exists
os.makedirs('segments', exist_ok=True)
os.makedirs('sentences', exist_ok=True)

# Initialize a list to store chunk labels
csv_data = []

# Silent segment of 400 milliseconds
silent_segment = AudioSegment.silent(duration=400)

# Generate combined sentences and process each segment
for index, hobby in enumerate(english_hobbies):
    object_particle = "은" if is_last_letter_vowel(hobby) else "는"
    combined_text = f"{hobby} {object_particle} 정말 재밌어요"
    segments = combined_text.split()

    # Initialize an empty audio segment for the sentence
    sentence_audio = AudioSegment.empty()
    
    # Process each segment
    for segment_index, segment in enumerate(segments):
        filename = f"segments/english_hobby_{index+1}_chunk_{segment_index+1}.wav"
        text_to_aiff_to_wav(segment, filename, "Yuna")

        # Load the word audio
        word_audio = AudioSegment.from_wav(filename)

        # Concatenate word audio to the sentence audio
        sentence_audio += word_audio + silent_segment
        
        # Determine if the segment is English or Korean and append the label to the list
        if segment.encode('utf-8').isalpha():
            language = "English"
        else:
            language = "Korean"
        
        # Add filename and language to CSV data
        csv_data.append([filename, language])

    # Export the sentence audio
    sentence_audio.export(f"sentences/english_hobby_sentence_{index+1}.wav", format="wav")

# Write data to CSV file
with open('english_hobby_labels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Language"])
    writer.writerows(csv_data)
