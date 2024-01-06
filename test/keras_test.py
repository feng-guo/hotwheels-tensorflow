import keras_ocr
import matplotlib.pyplot as plt
import numpy as np

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# Get a set of three example images
images = [
    keras_ocr.tools.read(url) for url in [
        'https://i.imgur.com/rPrPOsC.jpg',
        'https://i.imgur.com/o1ThsTj.jpg',
        # 'https://i.imgur.com/QcfXern.jpg',
    ]
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# Group words that are close to each other
grouped_predictions = []
for predictions in prediction_groups:
    # Sort predictions by y-coordinate of the bounding box
    predictions.sort(key=lambda word_box: np.mean(word_box[1][:, 1]))
    grouped_prediction = []
    current_line = []
    for word, box in predictions:
        if current_line and np.abs(np.mean(box[:, 1]) - np.mean(current_line[-1][1][:, 1])) < 50:
            # If the current word is close to the previous word vertically, append it to the current line
            current_line.append([word, box])
        else:
            # Otherwise, start a new line
            if current_line:
                # Sort the words in the current line by x-coordinate
                current_line.sort(key=lambda word_box: np.mean(word_box[1][:, 0]))
                grouped_prediction.extend(current_line)
            current_line = [[word, box]]
    # Don't forget to add the last line
    if current_line:
        current_line.sort(key=lambda word_box: np.mean(word_box[1][:, 0]))
        grouped_prediction.extend(current_line)
    grouped_predictions.append(grouped_prediction)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, grouped_predictions):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

plt.show()