import keras_ocr
import numpy as np
import tensorflow as tf

def get_grouped_predictions(image_url):
    pipeline = keras_ocr.pipeline.Pipeline()

    images = [keras_ocr.tools.read(image_url)]

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
                if horizontal_distance < horizontal_threshold:
                    group.append(word_box)
                else:
                    grouped_line.append(group)
                    group = [word_box]
            grouped_line.append(group)  # Add the last group
            grouped_predictions.append(grouped_line)

    grouped_text = []
    for line in grouped_predictions:
        for group in line:
            group_text = ' '.join(word_box[0] for word_box in group)
            grouped_text.append(group_text)

    return grouped_text

def get_sideways_grouped_predictions(image_url):
    pipeline = keras_ocr.pipeline.Pipeline()

    images = [keras_ocr.tools.read(image_url)]

    # Rotate the image 90 degrees clockwise
    images[0] = tf.image.rot90(images[0], k=3).numpy()

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
                if horizontal_distance < horizontal_threshold:
                    group.append(word_box)
                else:
                    grouped_line.append(group)
                    group = [word_box]
            grouped_line.append(group)  # Add the last group
            grouped_predictions.append(grouped_line)

    grouped_text = []
    for line in grouped_predictions:
        for group in line:
            group_text = ' '.join(word_box[0] for word_box in group)
            grouped_text.append(group_text)

    return grouped_text