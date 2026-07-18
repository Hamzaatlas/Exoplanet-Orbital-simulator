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
```
## Run
```bash
python simulation1.py
```
## Roadmap
- [x] Integrate NASA Exoplanet Archive API
- [x] Implement 3D rotation matrix math
- [x] Build interactive PySide6 GUI
- [ ] Add support for "Longitude of Ascending Node" if available
- [ ] Add ability to save plots as image files


## Data Sources (Official and FREE ;) )
[NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

[Matplotlib Documentation](https://matplotlib.org/)

[PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
