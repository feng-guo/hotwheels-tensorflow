import json
from hot_wheels_matcher import process_hotwheels_image

def convert_images_to_json(image_urls):
    # Process each image and collect the resulting JSON objects
    json_objects = [process_hotwheels_image(url) for url in image_urls]

    # Output the JSON objects to a file
    with open('tmp/test_cars.json', 'w') as f:
        json.dump(json_objects, f)