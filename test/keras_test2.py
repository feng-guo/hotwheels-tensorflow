import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

pipeline = keras_ocr.pipeline.Pipeline()

images = [keras_ocr.tools.read('https://i.imgur.com/rPrPOsC.jpg')]

# Rotate the image 90 degrees clockwise
images[0] = tf.image.rot90(images[0], k=3).numpy()

# Display the rotated image
plt.imshow(images[0])
plt.show()

prediction_groups = pipeline.recognize(images)

vertical_threshold = 50
horizontal_threshold = 50

grouped_predictions = []
for predictions in prediction_groups:
    predictions.sort(key=lambda word_box: np.mean(word_box[1][:, 1]))  # Sort vertically
    lines = []
    line = [predictions[0]]
    for word_box in predictions[1:]:
        vertical_distance = np.abs(np.mean(word_box[1][:, 1]) - np.mean(line[-1][1][:, 1]))
        print(f'Word: {word_box[0]}, Vertical distance: {vertical_distance}')
        if vertical_distance < vertical_threshold:
            line.append(word_box)
        else:
            lines.append(line)
            line = [word_box]
    lines.append(line)  # Add the last line

    for line in lines:
        line.sort(key=lambda word_box: np.mean(word_box[1][:, 0]))  # Sort horizontally
        grouped_line = []
        group = [line[0]]
        for word_box in line[1:]:
            horizontal_distance = word_box[1][0, 0] - group[-1][1][2, 0]  # Compare right-most point of first word and left-most point of second word
            print(f'Word: {word_box[0]}, Horizontal distance: {horizontal_distance}')
            if horizontal_distance < horizontal_threshold:
                group.append(word_box)
            else:
                grouped_line.append(group)
                group = [word_box]
        grouped_line.append(group)  # Add the last group
        grouped_predictions.append(grouped_line)

annotations = []
for line in grouped_predictions:
    for group in line:
        group_text = ' '.join(word_box[0] for word_box in group)
        print(f'Group text: {group_text}')
        for word_box in group:
            word = word_box[0]
            box = word_box[1]
            annotations.append((word, box))

fig, ax = plt.subplots(figsize=(20, 20))
keras_ocr.tools.drawAnnotations(image=images[0], predictions=annotations, ax=ax)
plt.show()