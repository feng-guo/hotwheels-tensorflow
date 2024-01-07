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
            match = re.search(r'<font color=".*?">(.*?)<\/font>|\'\'\'(.*?)\'\'\'', s)  # Match text enclosed in <font> tags or triple quotes
            if match is not None:
                text = match.group(1) if match.group(1) else match.group(2)  # If the first group is None (no match), use the second group
                text = text.replace("'", "")
                match = re.search(r'New for (\d{4})!', text)
                if match:
                    year = match.group(1)
                    other.append(f'New {year}')
                elif 'Super Treasure Hunt' in text:
                    other.append('STH')
                elif 'Treasure Hunt' in text:
                    other.append('TH')
                elif 'Kroger' in text:
                    other.append('Kroger Exclusive')
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
with open(os.path.join(os.path.dirname(__file__), '../data/cars_2024.json'), 'w') as file:
    file.write(json_data)