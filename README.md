# 🏭 Grinding Machine Predictive Maintenance System (Version 3.0)

> **Industrial IoT-based Predictive Maintenance System for a Surface Grinding Machine using RS485 Modbus, ESP32, Flask, Streamlit and Machine Learning.**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![ESP32](https://img.shields.io/badge/ESP32-IoT-red)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![License](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Project Overview

This project is an Industrial IoT and Machine Learning based Predictive Maintenance System developed for a surface grinding machine.

The system continuously acquires electrical parameters from a **SELEC MFM384 Three-Phase Multifunction Energy Meter** through **RS485 Modbus RTU**, transfers the data using an **ESP32**, processes it through a **Flask server**, stores it locally, and visualizes real-time machine health on a **Streamlit Dashboard**.

A Machine Learning model analyzes the incoming data and predicts the operational health of the grinding machine to support predictive maintenance and reduce unexpected downtime.

---

## 🎯 Objectives

- Collect real-time electrical parameters from an industrial grinding machine.
- Monitor machine health continuously.
- Detect abnormal operating conditions.
- Predict machine condition using Machine Learning.
- Provide a live industrial dashboard.
- Demonstrate Industrial IoT integration for predictive maintenance.

---

## ⚙️ Hardware Used

- SELEC MFM384 Three-Phase Multifunction Energy Meter
- MAX485 RS485 to TTL Converter
- ESP32 Development Board
- Surface Grinding Machine
- Wi-Fi Network
- Industrial Power Supply

---

## 💻 Software Stack

- Python
- Flask
- Streamlit
- Pandas
- NumPy
- Scikit-Learn
- Arduino IDE
- VS Code

---

## 📡 System Architecture

```

Grinding Machine
│
▼

SELEC MFM384 Energy Meter
│
▼

RS485 Modbus RTU
│
▼

MAX485 Converter
│
▼

ESP32
│ WiFi
▼

Flask Server
│
▼

CSV Storage
│
▼

Machine Learning
│
▼

Streamlit Dashboard

```

---

## ✨ Features

- Real-time Industrial IoT Data Acquisition
- RS485 Modbus Communication
- ESP32 Wi-Fi Integration
- Live Streamlit Dashboard
- Machine Learning Health Prediction
- Automatic Data Logging
- Real-time Visualization
- Asset Health Monitoring
- Industrial Sensor Integration

---
