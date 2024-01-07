from hotwheels_predictor import get_grouped_predictions, get_sideways_grouped_predictions
from difflib import SequenceMatcher
import json
import os

def process_hotwheels_image(image_url):
    # Call get_grouped_predictions with the image url
    text_array = get_grouped_predictions(image_url)

    year_position = None
    series_position = None

    # Iterate over the text array
    for text in text_array[:]:
        # Check if the text is purely made up of numbers
        if text.isdigit():
            # Check if it ends with 250
            if text.endswith('250') and text != '250':
                original = text
                print('original:', original)
                # Replace '1' with '/' if it's in front of '250'
                if text[-4] == '1':
                    text = text[:-4] + '/' + text[-3:]
                year_position = text
                text_array.remove(original)
            # Check if it ends with 5, 10, or 12
            elif text.endswith(('5', '10', '12')) and text not in ('5', '10', '12'):
                original = text
                print('original:', original)
                # Get the length of the matched string
                match_length = len(next((ending for ending in ('5', '10', '12') if text.endswith(ending)), ''))
                # Replace '1' with '/' if it's in front of the number
                if text[-match_length-1] == '1':
                    text = text[:-match_length-1] + '/' + text[-match_length:]
                series_position = text
                text_array.remove(original)

    # Remove any text that is less than 3 characters long
    text_array = [text for text in text_array if len(text) >= 3]

    # Call get_sideways_grouped_predictions with the image url
    sideways_text_array = get_sideways_grouped_predictions(image_url)

    # Remove all items in that array that is shorter than 5 characters
    sideways_text_array = [text for text in sideways_text_array if len(text) >= 5]

    print('year_position:', year_position)
    print('series_position:', series_position)
    print('text_array:', text_array)
    print('sideways_text_array:', sideways_text_array)

    match = search_best_match(year_position, series_position, text_array, sideways_text_array)

    # Replace the 'src' field with the image_url
    if match is not None:
        match['src'] = image_url

    print(match)

    return match

def search_best_match(year_position, series_position, text_array, sideways_text_array):
    # Load the JSON files
    filenames = ['cars_2023.json', 'cars_2022.json', 'cars_2024.json']
    data = []
    for filename in filenames:
        with open(os.path.join('data', filename)) as f:
            data.extend(json.load(f))

    best_match = None
    best_score = -1

    # Iterate over each object in the data
    for obj in data:
        score = 0

        # Compare the remaining strings in the text_array to the string after alt
        # Only the best match string in the array is counted towards the score
        best_text_score = max(SequenceMatcher(None, text.lower(), obj['alt'].lower()).ratio() for text in text_array)
        score += best_text_score

        # Try to exactly match the seriesPosition and yearPosition strings
        if series_position is not None:
            score += SequenceMatcher(None, obj['tags']['seriesPosition'].lower(), series_position.lower()).ratio()
        if year_position is not None:
            score += SequenceMatcher(None, obj['tags']['yearPosition'].lower(), year_position.lower()).ratio()

        # Compare the strings from the sideways_text_array with the series string
        best_sideways_text_score = max(SequenceMatcher(None, text.lower(), obj['tags']['series'].lower()).ratio() for text in sideways_text_array)
        score += best_sideways_text_score

        # Update the best match if this object has a higher score
        if score > best_score:
            best_match = obj
            best_score = score

    # Return the object that matches the inputs the best
    return best_match