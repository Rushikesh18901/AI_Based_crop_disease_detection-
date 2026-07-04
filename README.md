#  AI-Based Crop Yield & Disease Prediction System

> An AI-powered smart farming solution that detects crop diseases from leaf images, estimates crop health, recommends pesticides and fertilizers, calculates dosage, provides spray schedules, and supports weather-based farming decisions.

---

##  Project Overview

Agriculture is one of the most important sectors of the economy, but crop diseases significantly reduce productivity and yield. This project uses **Artificial Intelligence** and **Deep Learning** to detect crop diseases from leaf images and provides intelligent recommendations to farmers for effective crop management.

The system helps farmers by providing:

-  Crop Disease Detection
-  Pesticide Recommendation
-  Dosage Calculator
-  Fertilizer Recommendation
-  Next Spray Schedule
-  Weather-Based Spray Recommendation
-  Crop Health Analysis
-  History Management
-  Multi-language Support (English, Hindi & Marathi)

---

# Features

##  AI Disease Detection
- Detects crop diseases using leaf images.
- Deep Learning model based on MobileNetV2.
- Displays prediction confidence.

---

##  Plant Identification

Automatically identifies:

- Tomato
- Potato
- Apple
- Corn (Maize)

---

##  Crop Health Analysis

Displays

- Health Score
- Estimated Yield Loss
- Confidence Score

---

##  Pesticide Recommendation

Suggests

- Recommended pesticide
- Dosage per litre
- Spray interval

---

##  Smart Dosage Calculator

Automatically calculates

Example

```
1 Litre → 2.5 g

Tank Size = 20 Litres

Required Dosage = 50 g
```

---

##  Fertilizer Recommendation

Provides

- Fertilizer Name
- Usage Instructions
- Application Frequency

---

##  Safety Instructions

Displays

- Protective equipment
- Safe handling guidelines
- Spray precautions

---

##  Spray Reminder System

Shows

- Next Spray Date
- Days Remaining
- Spray Status

Allows farmers to save reminders.

---

##  Weather-Based Recommendation

Uses **OpenWeather API**

Displays

- Temperature
- Humidity
- Weather Condition

Recommends

 Safe to Spray

or

 Avoid Spraying

depending on weather conditions.

---

##  History Management

Stores every prediction in history.

Includes

- Date
- Plant
- Disease
- Confidence
- Pesticide

---

##  Analytics Dashboard

Displays

- Total Predictions
- Most Common Disease
- Disease Frequency
- Crop Analysis
- Recent History

---

##  Multi-language Support

Supports

- 🇬🇧 English
- 🇮🇳 Hindi
- 🇮🇳 Marathi

---

#  Deep Learning Model

Model Used

- MobileNetV2

Technique

- Transfer Learning

Framework

- TensorFlow
- Keras

Image Size

```
224 × 224
```

---

#  Dataset

Dataset Used

**PlantVillage Dataset**

Contains

- Healthy Leaves
- Diseased Leaves

Supported Crops

- Apple
- Corn
- Potato
- Tomato

---

#  Tech Stack

## Programming

- Python

## AI & Deep Learning

- TensorFlow
- Keras
- MobileNetV2

## Computer Vision

- OpenCV
- NumPy

## Data Processing

- Pandas

## Dashboard

- Streamlit

## Weather API

- OpenWeatherMap API

## Database

CSV Files

- pesticide_database.csv
- fertilizer_database.csv
- history.csv
- spray_schedule.csv

---

#  Project Structure

```
AI-Based-Crop-Yield-Disease-Prediction/
│
├── app.py
├── train_model.py
├── requirements.txt
│
├── models/
│   ├── crop_disease_model.h5
│   └── label_mapping.json
│
├── utils/
│   ├── prediction.py
│   ├── recommendation_engine.py
│   ├── fertilizer_engine.py
│   ├── dosage_calculator.py
│   ├── weather.py
│   ├── analytics.py
│   ├── reminder.py
│   ├── history_manager.py
│   ├── translator.py
│   ├── health_score.py
│   ├── yield_estimator.py
│   └── safety_alert.py
│
├── database/
│   ├── pesticide_database.csv
│   ├── fertilizer_database.csv
│   ├── history.csv
│   └── spray_schedule.csv
│
├── dataset/
│
└── README.md
```

---



#  Dashboard Features

- Upload Crop Image
- AI Disease Detection
- Confidence Score
- Health Score
- Yield Loss
- Pesticide Recommendation
- Dosage Calculator
- Fertilizer Recommendation
- Weather Recommendation
- Spray Reminder
- Analytics Dashboard
- History Management

---

#  Future Improvements

- Mobile Application
- IoT Sensor Integration
- Drone-Based Crop Monitoring
- Voice Assistant
- SMS Notifications
- Cloud Deployment
- Real-Time Disease Monitoring
- AI Chatbot for Farmers

---

#  Author
**Rushikesh Bhavar**
B.Sc. Data Science  
Department of Technology  
Savitribai Phule Pune University

