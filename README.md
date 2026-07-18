# Exoplanet-Orbital-Simulator 🪐

This Python application provides an interactive 3D visualization of exoplanet orbits. It connects directly to the NASA Exoplanet Archive to fetch real-world astrophysical data, allowing users to explore and simulate the orbital paths of known exoplanetary systems.

## What this project does
1. Queries the NASA Exoplanet Archive for planet name, semi-major axis, eccentricity, inclination, and argument of periapsis.
2. Cleans the data to ensure only valid orbital parameters are used.
3. Calculates the 3D orbital trajectory based on Keplerian elements.
4. Renders a rotatable, zoomable 3D plot using PySide6 and Matplotlib.

## Setup
```bash
pip install -r requirements.txt
