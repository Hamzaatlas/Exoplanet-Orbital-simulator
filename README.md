# Exoplanet-Orbital-simulator

This Python application provides an interactive 3D visualization of exoplanet orbits. It connects directly to the **NASA Exoplanet Archive** to fetch real-world astrophysical data, allowing users to explore and simulate the orbital paths of known exoplanetary systems.

## How it works:
*   **Data Acquisition**: The application uses `astroquery` to perform an ADQL query on the NASA Exoplanet Archive's `ps` (Planetary Systems) table, retrieving essential Keplerian parameters such as semi-major axis, eccentricity, inclination, and the argument of periapsis.
*   **Orbital Mechanics**: For every selected planet, the code generates a set of 2D coordinates representing an ellipse in the orbital plane based on the planet's eccentricity and semi-major axis.
*   **3D Transformation**: Using the retrieved orbital elements, the application constructs a 3D rotation matrix to transform the flat ellipse into its correct orientation in 3D space.
*   **Interactive Visualization**: The interface is built using `PySide6` and `Matplotlib`. It provides a scrollable list of planets; when a planet is selected, the application dynamically calculates its 3D orbit and renders it in a rotatable, zoomable 3D plot with the host star centered at the origin.
