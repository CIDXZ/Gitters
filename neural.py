import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the pixel values to range [0, 1]
x_train, x_test = x_train / 255.0, x_test / 255.0

# Flatten the images
x_train = x_train.reshape(x_train.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)

# Split the training data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

# Define a function to create the neural network model
def create_model(hidden_layers=1, neurons=64, activation='relu', learning_rate=0.01, dropout_rate=0.2):
    model = Sequential()
    model.add(Flatten(input_shape=(784,)))
    
    for _ in range(hidden_layers):
        model.add(Dense(neurons, activation=activation))
        model.add(Dropout(dropout_rate))  # Add dropout layer
    
    model.add(Dense(10, activation='softmax'))
    
    optimizer = Adam(learning_rate=learning_rate)  # Use Adam optimizer
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# Define learning rate schedule
def learning_rate_schedule(epoch, learning_rate):
    if epoch < 10:
        return learning_rate
    else:
        return learning_rate * tf.math.exp(-0.1)

# Define hyperparameters to explore
hidden_layers_values = [1, 2]
neurons_values = [128, 256]
activation_values = ['relu', 'tanh']
learning_rate_values = [0.001, 0.0001]
dropout_rate_values = [0.3, 0.4]

# Function to plot training history
def plot_training_history(history, title):
    plt.figure(figsize=(12, 6))

    # Plot training & validation accuracy values
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot training & validation loss values
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

# Loop over hyperparameters and train the models
for hidden_layers in hidden_layers_values:
    for neurons in neurons_values:
        for activation in activation_values:
            for learning_rate in learning_rate_values:
                for dropout_rate in dropout_rate_values:
                    model = create_model(hidden_layers=hidden_layers,
                                         neurons=neurons,
                                         activation=activation,
                                         learning_rate=learning_rate,
                                         dropout_rate=dropout_rate)
                    print(f"Training model with {hidden_layers} hidden layer(s), {neurons} neurons, "
                          f"{activation} activation function, learning rate {learning_rate}, "
                          f"and dropout rate {dropout_rate}...")
                    
                    # Add early stopping to prevent overfitting
                    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
                    
                    # Define learning rate scheduler
                    lr_scheduler = LearningRateScheduler(learning_rate_schedule)
                    
                    # Train the model
                    history = model.fit(x_train, y_train,
                                        epochs=20,
                                        batch_size=32,
                                        validation_data=(x_val, y_val),
                                        callbacks=[early_stopping, lr_scheduler])
                    
                    # Plot training history
                    plot_training_history(history, title=f"Training History: {hidden_layers} hidden layer(s), {neurons} neurons, "
                                                          f"{activation} activation function, learning rate {learning_rate}, "
                                                          f"dropout rate {dropout_rate}")
                    
                    # Evaluate the model on test data
                    test_loss, test_accuracy = model.evaluate(x_test, y_test)
                    print(f"Test accuracy: {test_accuracy}")
                    print("-----------------------------------------------------------")
