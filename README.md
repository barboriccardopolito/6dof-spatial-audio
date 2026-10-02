# 6DoF Spatial Audio Prototype

Real-time spatial audio system developed at Politecnico di Torino.

The project explores 6 Degrees of Freedom spatial audio rendering,
combining real-time head tracking, OSC/UDP communication,
Ambisonics processing and binaural rendering.

## Features

- Real-time 6DoF spatial audio rendering
- Python middleware for sensor data processing
- OSC/UDP communication at 60 FPS
- Ambisonics HOA routing
- HRTF/HRIR binaural rendering
- 16-channel audio routing architecture
- Head-tracking integration
- Real-time operation with a 512-sample audio buffer

## Architecture

Sensor / Head Tracking
        ↓
Python Middleware
        ↓
OSC / UDP
        ↓
REAPER
        ↓
Spatial Processing / Ambisonics
        ↓
HRTF / HRIR
        ↓
Binaural Output

## Technologies

- Python
- NumPy
- python-osc
- REAPER
- OSC / UDP
- Ambisonics
- HRTF / HRIR
- COMPASS 6DoF

## Project Context

Developed as an academic project during the MSc in Cinema and Media
Engineering at Politecnico di Torino.

The system was designed to investigate real-time listener movement
inside a spatial audio environment while maintaining perceptual
consistency of virtual sound sources.

## Author

Riccardo Barbo
MSc Student in Cinema and Media Engineering
Politecnico di Torino
