import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from pydub import AudioSegment
from pydub.playback import play

# Load model
model = load_model("saved_model.h5")

# Define categories
categories = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']

# Function to make predictions on a single image
def predict_single_image(img, model):
    img_array = np.array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = prediction[0][predicted_class]

    return predicted_class, confidence

def main():
    st.set_page_config(
        page_title="Distracted Driver APP",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # # Header photo
    # header_image = "Drive Safe.jpg"
    # st.image(header_image, use_column_width=True)

    # Define image paths for each page
    home_image = "Drive Safe.jpg"
    image_predictor_image = "be_safe.png"
    about_us_image = "Drive Safe.jpg"

    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Image Predictor", "About Us"])

    # Display the selected page
    if page == "Home":
        home_page(home_image)
    elif page == "Image Predictor":
        image_predictor_page(image_predictor_image)
    elif page == "About Us":
        about_us_page(about_us_image)

def home_page(image_path):
    st.image(image_path, use_column_width=True)
    st.title('Distracted Driver App')
    st.markdown("""
    ## Business Overview

    You're probably wondering why this APP? Well, road safety remains a critical concern around the world, with distracted driving claimed as being a leading cause of accidents. Distracted driving accounts for at least **9%** of annual car accidents in USA and is the leading cause of accidents worldwide.  

    According to an NTSA report on accidents in 2023, **1,072** people were killed on our roads, with the main causes being drunk driving, speeding and distracted driving. In Kenya we already have measures in place to tackle the first two: Alcoblow for drunk-driving, speed guns and speed governors for speeding. There seems to be nothing in place to tackle the third cause and that is where our project comes in.  

    This project aims to leverage computer vision and machine learning techniques to develop a system capable of detecting distracted drivers in real-time, contributing to enhanced road safety measures.

    ## Problem Statement

    Distracted driving poses significant risks, including accidents, injuries, and fatalities. Identifying and mitigating instances of distraction while driving is crucial to reducing road accidents.  

    The ballooning of car insurance claims led Directline Insurance, Kenya, to engage us in this project, with a vision to lower the rising claims from their customers.
    """, unsafe_allow_html=True)


def play_sound(sound_file):
    sound = AudioSegment.from_mp3(sound_file)
    play(sound)    

def image_predictor_page(image_path):
    st.image(image_path, use_column_width=True)
    st.title("Driver Image Classification App")

    uploaded_file = st.file_uploader("Choose a driver image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

        # Make predictions
        predicted_class, confidence = predict_single_image(image, model)

        st.write(f"Predicted Class: {categories[predicted_class]}")
        st.write(f"Confidence: {confidence:.2%}")

        # Check if the predicted class is not c1
        if categories[predicted_class] != 'c1':
            # Play sound if the predicted class is not c1
            play_sound("button.mp3")

def about_us_page(image_path):
    st.image(image_path, use_column_width=True)
    st.title('About Us')

    st.subheader('Meet the Team')
    st.write("""
        We are all data science students from Flat Iron Moringa School, working on our capstone project.
    """)

    team_members = {
        "Leonard Gachimu": "https://github.com/leogachimu",
        "Rowlandson Kariuki": "link-to-rowlandson-repo",
        "Francis Njenga": "https://github.com/GaturaN",
        "Mourine Mwangi": "link-to-mourine-repo",
        "Khadija Omar": "link-to-khadija-repo",
        "Victor Mawira": "link-to-victor-repo",
        "Onesphoro Kibunja": "https://github.com/Ones-Muiru"
    }

    for name, link in team_members.items():
        st.markdown(f"- [{name}]({link})")

if __name__ == "__main__":
    main()