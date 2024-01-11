import pickle
import numpy as np
import pyttsx3
import speech_recognition as sr
import pandas as pd

# Load the saved model
RF_pkl_filename = 'RandomForest.pkl'  # Replace with the path to your .pkl file
with open(RF_pkl_filename, 'rb') as Model_pkl:
    loaded_model = pickle.load(Model_pkl)

# Set feature names (if available)
if hasattr(loaded_model, 'set_feature_names'):
    feature_names = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing', 'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level']
    loaded_model.set_feature_names(feature_names)

# Initialize Speech Recognition for English
recognizer = sr.Recognizer()

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Set English language for text-to-speech
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')  # English voice


import csv
import os

# Function to load existing user details from a CSV file
def load_user_details():
    user_details = []
    file_name = 'user_details.csv'

    if os.path.exists(file_name):
        with open(file_name, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_details.append(row)
    return user_details

# Function to save user details to a CSV file
def save_user_details(user_details):
    file_name = 'user_details.csv'

    with open(file_name, 'w', newline='') as file:
        fieldnames = list(user_details[0].keys()) if user_details else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(user_details)
        
user_details = load_user_details()
        
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_yes_no_input(prompt):
    speak(prompt)
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(prompt)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        input_text = recognizer.recognize_google(audio, language='en-US')
        print(f"User input: {input_text}")
        return input_text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please speak clearly.")
        return get_yes_no_input(prompt)
    except sr.RequestError:
        speak("Sorry, there was an error processing your request.")
        return None


    
def get_age_input():
    speak("Please state your age.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please state your age.")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        age = recognizer.recognize_google(audio, language='en-US')
        age_value = int(age)
        if 0 < age_value < 150:  # Assuming a reasonable age range
            return age_value
        else:
            speak("Please state a valid age.")
            return get_age_input()
    except (sr.UnknownValueError, ValueError):
        speak("Please state a valid numeric age.")
        return get_age_input()
    except sr.RequestError:
        speak("Sorry, there was an error processing your request.")
        return None
def get_categorical_input_map(prompt, mapping):
    speak(prompt)
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(prompt)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        input_text = recognizer.recognize_google(audio, language='en-US')
        input_value = mapping.get(input_text.lower())
        if input_value is None:
            speak("Please provide a valid response.")
            return get_categorical_input_map(prompt, mapping)
        return input_value
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please speak clearly.")
        return get_categorical_input_map(prompt, mapping)
    except sr.RequestError:
        speak("Sorry, there was an error processing your request.")
        return None

blood_pressure_mapping = {'low': 1, 'normal': 2, 'high': 0}
cholesterol_mapping = {'low': 1, 'normal': 2, 'high': 0}

    
while True:
    speak("Hello i am smart bot ai made with machine learning")

    Fever = get_yes_no_input("Do you have fever? Say 'yes' or 'no'")
    Fever = 1 if 'yes' in Fever else 0 if 'no' in Fever else None

    if Fever is None:
        continue

    Cough = get_yes_no_input("Do you have a cough? Say 'yes' or 'no'")
    Cough = 1 if 'yes' in Cough else 0 if 'no' in Cough else None

    if Cough is None:
        continue

    Fatigue = get_yes_no_input("Do you have fatigue? Say 'yes' or 'no'")
    Fatigue = 1 if 'yes' in Fatigue else 0 if 'no' in Fatigue else None

    if Fatigue is None:
        continue

    Breathing = get_yes_no_input("Do you have difficulty breathing? Say 'yes' or 'no'")
    Breathing = 1 if 'yes' in Breathing else 0 if 'no' in Breathing else None

    if Breathing is None:
        continue

    # Similarly, add more questions for other symptoms...

    Age = get_age_input()
    Gender = get_yes_no_input("Are you Male ? Say 'yes' or 'no'")
    Gender = 1 if 'yes' in Gender else 0 if 'no' in Gender else None
    Blood = get_categorical_input_map("Please state your blood pressure level as low, normal, or high.", blood_pressure_mapping)

    Cholesterol = get_categorical_input_map("Please state your cholesterol level as low, normal, or high.", cholesterol_mapping)
    

    # Append user details to the list
    
    # Prepare the input data for prediction
    input_data = [Fever, Cough, Fatigue, Breathing, Age, Gender, Blood, Cholesterol]  # Adjust this according to your model's input features
    input_data_as_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_array.reshape(1, -1)

    # Make prediction using the loaded model
    prediction = loaded_model.predict(input_data_reshaped)
    user_info = {
        'Fever': Fever,
        'Cough': Cough,
        'Fatigue': Fatigue,
        'Difficulty Breathing': Breathing,
        'Age': Age,
        'Gender': Gender,
        'Blood Pressure': Blood,
        'Cholesterol Level': Cholesterol,
        'Dieases' : prediction
    }
    
    user_details.append(user_info)
    print(prediction)
    # precautions part
    speak("your have")
    speak(prediction)
    # Replace this with your appropriate action based on the prediction
    save_user_details(user_details)
