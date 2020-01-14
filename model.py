import csv
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, Dropout, Conv2D, MaxPooling2D
import matplotlib.image as mpimg


lines =[]
with open('dataset/driving_log.csv') as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		lines.append(line)

images = []
measurements = []
augmented_images = []
augmented_measurements = []
correction = [0, 0.2, -0.2]
for line in lines:
	for i in range(3):
		source_path = line[i]
		filename = source_path.split('/')[-1]
		current_path = 'dataset/IMG/' + filename
		image = mpimg.imread(current_path)
		images.append(image)
		measurement = float(line[3]) + correction[i]
		augmented_images.append(image)
		augmented_images.append(cv2.flip(image, 1)) # Flip the image for Data Augmentation
		augmented_measurements.append(measurement)
		augmented_measurements.append(measurement* -1.0) # Invert the angel of steering measurement for the flipped augmented image
		measurements.append(measurement)

# X_train = np.array(images)
# y_train = np.array(measurements)

# Convert Augmented dataset to numpy array for training
X_train = np.array(augmented_images) 
y_train = np.array(augmented_measurements)


model = Sequential()
model.add(Lambda(lambda x : x/255.0 - 0.5, input_shape = (160, 320, 3)))
model.add(Cropping2D(cropping = ((70, 0), (0, 0)))) # Crop the top 70 pixels 
model.add(Conv2D(24, 5, 5, activation='relu', subsample=(2, 2)))
model.add(Conv2D(36, 5, 5, activation='relu', subsample=(2, 2)))
# model.add(Dropout(0.2))
model.add(Conv2D(48, 5, 5, activation='relu', subsample=(2, 2)))
model.add(Conv2D(64, 3, 3, activation='relu'))
# model.add(Dropout(0.2))
model.add(Conv2D(64, 3, 3, activation='relu'))
# model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1))
model.summary()

model.compile(loss ='mse', optimizer = 'adam')
model.fit(X_train, y_train, validation_split =0.2, shuffle = True, nb_epoch = 2)
model.save('model.h5')


