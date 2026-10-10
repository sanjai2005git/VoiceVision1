import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import config

def build_cnn_lstm_model(input_shape, cnn_filters=config.CNN_FILTERS, lstm_units=config.LSTM_UNITS,
                         dropout_rate=config.DROPOUT, learning_rate=config.LEARNING_RATE):
    """
    Builds and compiles a CNN + Bidirectional LSTM model (or an MLP model if 1D engineered features are enabled) for binary classification.
    """
    if getattr(config, "USE_ENGINEERED_FEATURES", False):
        inputs = keras.Input(shape=input_shape, name="audio_features_input")
        x = layers.Dense(16, activation="relu", name="dense_1")(inputs)
        x = layers.Dense(8, activation="relu", name="dense_2")(x)
        outputs = layers.Dense(1, activation="sigmoid", name="sigmoid_output")(x)
        model = keras.Model(inputs=inputs, outputs=outputs, name="Voice_Age_MLP_Classifier")
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy"])
        return model

    inputs = keras.Input(shape=input_shape, name="audio_features_input")
    
    x = inputs
    
    # 1. Convolutional feature extractor
    for i, filters in enumerate(cnn_filters):
        x = layers.Conv2D(filters, (3, 3), padding="same", name=f"conv2d_{i+1}")(x)
        x = layers.BatchNormalization(name=f"batch_norm_{i+1}")(x)
        x = layers.Activation("relu", name=f"activation_{i+1}")(x)
        
        # Max pool on the first few layers to downsample, keeping sequence length reasonable
        if i < len(cnn_filters) - 1:
            x = layers.MaxPooling2D(pool_size=(2, 2), name=f"max_pooling_{i+1}")(x)
            x = layers.Dropout(dropout_rate, name=f"dropout_conv_{i+1}")(x)
            
    # 2. Reshape spatial-frequency feature maps to temporal sequence
    # Current shape of x: (batch_size, time_steps_reduced, freq_bins_reduced, cnn_filters[-1])
    # We want to reshape it to: (batch_size, time_steps_reduced, freq_bins_reduced * cnn_filters[-1])
    # to feed it into the LSTM.
    shape = x.shape
    time_steps = shape[1]
    freq_bins = shape[2]
    channels = shape[3]
    
    # Ensure they are static integers
    if time_steps is None or freq_bins is None or channels is None:
        # Fallback to dynamic computation using tf.shape if Keras shape is not fully resolved
        x = layers.Reshape((-1, x.shape[2] * x.shape[3]), name="temporal_reshape")(x)
    else:
        x = layers.Reshape((time_steps, freq_bins * channels), name="temporal_reshape")(x)
        
    # 3. Bidirectional LSTM
    x = layers.Bidirectional(
        layers.LSTM(lstm_units, return_sequences=False, name="lstm"),
        name="bidirectional_lstm"
    )(x)
    
    # 4. Classification layers
    x = layers.Dense(64, activation="relu", name="dense_dense")(x)
    x = layers.Dropout(dropout_rate, name="dropout_dense")(x)
    
    outputs = layers.Dense(1, activation="sigmoid", name="sigmoid_output")(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name="Voice_Age_Classifier")
    
    # 5. Compile Model
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    
    return model

if __name__ == "__main__":
    # Test printing model summary
    dummy_input_shape = (501, 64, 1)
    model = build_cnn_lstm_model(dummy_input_shape)
    model.summary()
