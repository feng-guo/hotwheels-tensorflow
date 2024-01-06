import json
import re
import os
from link_getter import get_image_url
from urllib.parse import quote

# Read the file
with open(os.path.join(os.path.dirname(__file__), 'data_2024.txt'), 'r') as file:
    data = file.read()

# Split the file into lines
lines = data.split('\n')

# Initialize a list to hold the cars
cars = []

# Iterate over the lines
for i, line in enumerate(lines):
    # Check if the line starts with '|-', indicating a new car
    if line.startswith('|-'):
        # Extract the necessary information using regular expressions
        src = re.search(r'\[\[File:(.*?)\|', lines[i + 6]).group(1)
        if src and (src.endswith('.webp') or src == 'Image Not Available.jpg'):
            src = 'https://static.wikia.nocookie.net/hotwheels/images/b/b5/Image_Not_Available.jpg'
        else:
            src = 'https://hotwheels.fandom.com/wiki/File:' + quote(src.replace(' ', '_'))
            src = get_image_url(src)
        print('src:', src)

        alt_match = re.search(r'\[\[(.*?)\]\]', lines[i + 3])
        if alt_match is not None:
            alt_text = alt_match.group(1)
            if '|' in alt_text:
                alt = alt_text.split('|')[1]  # Take the text after '|'
            else:
                alt = alt_text
        print('alt:', alt)

        series_match = re.search(r'<font color=".*?">(.*?)<\/font>', lines[i + 4])
        if series_match is not None:
            series = series_match.group(1)
        print('series:', series)

        series_position = lines[i + 5][1:]  # Trim the first '|' character
        print('series_position:', series_position)

        year_position = lines[i + 2][1:].lstrip('0') + '/250'  # Trim the first '|' character, remove leading zeros, and append '/250'
        print('year_position:', year_position)

        other = []
        for s in lines[i + 4].split('<br')[1:]:
            match = re.search(r'<font color=".*?">(.*?)<\/font>', s.replace("'''", ""))  # Remove triple quotes
            if match is not None:
                text = match.group(1).replace("'", "")
                if 'New for 2023!' in text:
                    other.append('New 2023')
                if 'New for 2022!' in text:
                    other.append('New 2022')
                elif 'Exclusive' in text:
                    # Split the text into words
                    words = text.split(' ')
                    # Find the index of 'Exclusive'
                    index = words.index('Exclusive')
                    # Join all the words before 'Exclusive'
                    before_exclusive = ' '.join(words[:index])
                    # Add the words before 'Exclusive' to other
                    other.append(before_exclusive)
                elif 'Super Treasure Hunt' in text:
                    other.append('STH')
                elif 'Treasure Hunt' in text:
                    other.append('TH')
                else:
                    other.append(text)

        print('other:', other)

        # Create a dictionary for the car
        car = {
            'src': src,
            'alt': alt,
            'tags': {
                'series': series,
                'seriesPosition': series_position,
                'modelYear': 2023,
                'yearPosition': year_position,
                'other': other
            }
        }

        # Append the car to the list
        cars.append(car)

# Convert the list to JSON
json_data = json.dumps(cars, indent=2)

# Write the JSON to a file
with open(os.path.join(os.path.dirname(__file__), 'cars_2024.json'), 'w') as file:
    file.write(json_data)