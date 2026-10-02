# 6DoF Spatial Audio — Real-Time Head-Tracked Rendering Prototype

Real-time **6 Degrees of Freedom (6DoF) spatial audio prototype** combining
Python middleware, motion/head tracking, OSC/UDP communication,
Higher-Order Ambisonics and binaural rendering in REAPER.

Developed as an academic project during the MSc in **Cinema and Media Engineering**
at **Politecnico di Torino**.

---

## Why this project

Traditional binaural audio reproduces a spatial scene from a fixed listening position.

This project explores a more interactive approach: the listener can move and rotate
inside a virtual acoustic environment while the system continuously updates the
spatial rendering of the sound field.

The goal was to design a real-time pipeline capable of translating tracking data into
audio-rendering parameters while maintaining spatial consistency and low-latency
interaction.

---

## What I worked on

My contribution focused on the software and real-time audio pipeline, including:

- development of a **Python middleware** for processing tracking data;
- real-time communication between the tracking system and REAPER using **OSC/UDP**;
- management and transformation of positional/orientation data;
- integration with the spatial audio rendering environment;
- testing and debugging of the real-time interaction pipeline;
- analysis of routing, phase and spatial rendering behavior.

> This repository contains the technical material and implementation used for the
> academic prototype.

---

## System Architecture

```text
       Head / Motion Tracking
                │
                │ position + orientation
                ▼
       ┌─────────────────────┐
       │  Python Middleware  │
       │ middleware_6dof.py  │
       └─────────────────────┘
                │
              OSC/UDP
                │
                ▼
       ┌─────────────────────┐
       │       REAPER        │
       │ Spatial Audio Scene │
       └─────────────────────┘
                │
                ▼
     Higher-Order Ambisonics
                │
                ▼
        HRTF / HRIR Rendering
                │
                ▼
          Binaural Output
                │
                ▼
            Headphones
