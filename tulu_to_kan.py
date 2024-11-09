import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, ImageDataGenerator
import numpy as np
import pandas as pd
import requests
import os
import zipfile
from gtts import gTTS
from io import BytesIO

# Define image dimensions
img_height, img_width = 150, 150
batch_size = 32
confidence_threshold = 0.7

dataset_url = "https://github.com/manishak8089/VarnaMithra-Tulu_to_Multilingual_Translation/releases/download/v2.0/dataset.zip"

# File path to save the downloaded dataset
zip_file_path = "dataset.zip"

# Download the dataset
if not os.path.exists(zip_file_path):
    response = requests.get(dataset_url)
    with open(zip_file_path, "wb") as f:
        f.write(response.content)
    st.success("Dataset downloaded successfully!")

# Unzip the dataset
temp_dir = "temp_dataset"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Set the path to the unzipped dataset
dataset_path = os.path.join(temp_dir, "resize2")  # Adjust this to the correct folder name

# Load model and generator setup
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(img_height, img_width),
    color_mode='grayscale',
    class_mode='categorical',
    batch_size=batch_size,
    subset='training',
    shuffle=True,
    seed=42,
)

model_path = 'tulu_character_recognition_model2.h5'
model_url = 'https://github.com/manishak8089/VarnaMithra-Tulu_to_Multilingual_Translation/releases/download/v1.0/tulu_character_recognition_model2.h5'

# Check if model exists, otherwise download
if not os.path.exists(model_path):
    st.info("Downloading model, please wait...")
    response = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(response.content)
    st.success("Model downloaded successfully!")

# Load model with error handling
try:
    model = load_model(model_path)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
except Exception as e:
    st.error("An error occurred while loading the model.")
    st.text(f"Error details: {e}")


class_indices = train_generator.class_indices
index_to_class = {v: k for k, v in class_indices.items()}

def preprocess_image(img):
    img = img.convert("L")
    img = img.resize((img_width, img_height))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = np.repeat(img_array, 3, axis=-1)
    img_array /= 255.0
    return img_array

def is_image_blank(image_data):
    return np.all(image_data[:, :, 0] == 0) or np.all(image_data[:, :, 0] == 255)

# Enhanced speak function with gTTS for non-English languages
def speak(text, lang='en'):
    if lang == 'en':
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        tts = gTTS(text=text, lang=lang)
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        st.audio(audio_data.getvalue(), format="audio/mp3")

# Instructions modal
def show_instructions():
    st.markdown("""
    <div style='background-color: #e4f7fc; padding: 5px; border-radius: 7px; max-width: 1150px;  font-family: Georgia;'>
        <h2 style='color: #0c5460; font-size: 1.3em;'>How to Use the Drawing Tool</h2>
        <p style='color: #0c5460; font-size: 1.1em;line-height: 1.0;'>1. Draw a single character.</p>
        <p style='color: #0c5460; font-size: 1.1em;line-height: 1.0;'>2. The system will show its predicted Kannada equivalent.</p>
    </div>
    """, unsafe_allow_html=True)



# Set page config with a larger layout
st.set_page_config(page_title="AksharaSetu", layout="wide")

# Create two columns for a better UI layout
col1, col2 = st.columns([2, 1])  # Adjust the width ratio for UI

with col1:
    # Header Section
    st.markdown(
    """
    <div style='background-color: #f1f8fc; padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1); max-width: 90%; '>
        <h1 style='text-align: center; color: #2e4a77; font-family: "Georgia", serif; font-size: 3em; font-weight: bold;'>
            <i style="font-size: 1.1em;">AksharaSetu</i>: The Character Bridge Between Tulu and Kannada
        </h1>
        <p style='text-align: center; color: #3b5a80; font-size: 1.4em; line-height: 1.5em; font-family: "Great Vibes", cursive; font-weight: 300;'>
            Empowering the transition of Tulu characters to Kannada with precision, simplicity, and speed. Bridging languages for seamless communication.
        </p>
    </div>
    """, unsafe_allow_html=True
)


    # Additional content or features can be added here (e.g., instructions button)
    if st.button("🛈 Instructions"):
        show_instructions()

    # Drawing Canvas for character input
    st.write("Draw a Character:")
    canvas_result = st_canvas(
        fill_color="#000000",
        stroke_width=5,
        stroke_color="#FFFFFF",
        background_color="#000000",
        width=150,
        height=150,
        drawing_mode="freedraw",
        key="canvas_1",
    )


# Prediction based on the drawn character
if canvas_result.image_data is not None:
    if not is_image_blank(canvas_result.image_data):
        drawn_image = Image.fromarray((canvas_result.image_data[:, :, :3]).astype("uint8"), "RGB")
        preprocessed_image = preprocess_image(drawn_image)
        predictions_array = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions_array)
        confidence = predictions_array[0][predicted_class]
        
        if confidence >= confidence_threshold:
            predicted_character = index_to_class.get(predicted_class, "Unknown")
            st.markdown(f"<p style='font-size:25px; color:#2e4a77; font-weight:bold;'>Predicted kannada Character: {predicted_character}</p>", unsafe_allow_html=True)
            
            
        else:
            st.markdown("<p style='font-size:25px; color:red; font-weight:bold;'>Unrecognized Character</p>", unsafe_allow_html=True)
