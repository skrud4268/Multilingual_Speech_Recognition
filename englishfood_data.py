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

# English food names
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

# Ensure the segments folder exists
os.makedirs('segments', exist_ok=True)
os.makedirs('sentences', exist_ok=True)

# Initialize a list to store chunk labels
csv_data = []

# Silent segment of 400 milliseconds
silent_segment = AudioSegment.silent(duration=400)

# Generate combined sentences and process each segment
for index, food in enumerate(english_foods):
    object_particle = "를" if is_last_letter_vowel(food) else "을"
    combined_text = f"나는 {food} {object_particle} 좋아합니다"
    segments = combined_text.split()

    # Initialize an empty audio segment for the sentence
    sentence_audio = AudioSegment.empty()
    
    # Process each segment
    for segment_index, segment in enumerate(segments):
        filename = f"segments/english_food_{index+1}_chunk_{segment_index+1}.wav"
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
    sentence_audio.export(f"sentences/english_food_sentence_{index+1}.wav", format="wav")

# Write data to CSV file
with open('english_food_labels.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Language"])
    writer.writerows(csv_data)
