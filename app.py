import streamlit as st
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define image dimensions and paths
img_height, img_width = 150, 150
batch_size = 32
data_dir = 'D:\\Tulu_lipi\\dataset'

# Data augmentation and normalization
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,  # 20% of data for validation
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)
# Load the trained model
model = load_model('tulu_character_recognition_model2.h5')



# Define a dictionary mapping class indices to Kannada folder names
class_indices = train_generator.class_indices  # Assuming train_generator is available
index_to_class = {v: k for k, v in class_indices.items()}

# Function to load and preprocess an image
def load_and_preprocess_image(uploaded_file):
    img = Image.open(uploaded_file).convert('RGB')
    img = img.resize((img_width, img_height))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.0
    return img_array

# Streamlit App
st.title("Tulu Handwritten Character Translator")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Preprocess and predict
    img_array = load_and_preprocess_image(uploaded_file)
    predictions = model.predict(img_array)
    
   
    
    # Get predicted class
    predicted_class = np.argmax(predictions)
    predicted_folder = index_to_class.get(predicted_class, "Unknown")

    # Display the result
    st.write(f"The image belongs to folder: {predicted_folder}")
