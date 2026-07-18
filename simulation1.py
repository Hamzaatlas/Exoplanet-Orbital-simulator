import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QListWidget
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

# --------------------------------------------------------------
# 1️⃣  Correct ADQL query
# --------------------------------------------------------------
QUERY = "pl_name, pl_orbsmax, pl_orbeccen, pl_orbincl, pl_orblper"

class OrbitPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Exoplanet Orbit Simulator")
        self.resize(1000, 700)

        # ----- Load the exoplanet catalogue -----
        try:
            raw_table = NasaExoplanetArchive.query_criteria(
                table="ps", select=QUERY
            )
            self.data = raw_table.to_pandas()
        except Exception as exc:
            print("\n=== FAILED QUERY ===")
            print(QUERY)
            raise exc

        # Rename columns locally
        self.data = self.data.rename(columns={
            "pl_orbsmax": "semi_major_axis",
            "pl_orbeccen": "eccentricity",
            "pl_orbincl": "inclination",
            "pl_orblper": "arg_periapsis"
        })

        # Add a default Longitude of Ascending Node (0 degrees)
        self.data["long_asc_node"] = 0.0

        # Keep only rows that have the required fields
        self.data = self.data.dropna(
            subset=["semi_major_axis", "eccentricity", "inclination", "arg_periapsis"]
        )
        
        self.planet_names = self.data["pl_name"].tolist()

        # ----- UI construction -----
        # Use QHBoxLayout to put the list on the left and the plot on the right
        layout = QHBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.planet_names)
        self.list_widget.currentTextChanged.connect(self.plot_orbit)

        # Add the list widget and give it a stretch factor of 1
        layout.addWidget(self.list_widget, 1)

        # Matplotlib canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Add the canvas and give it a stretch factor of 3 (so it's larger)
        layout.addWidget(self.canvas, 3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # --------------------------------------------------------------
    # 2️⃣  Build the 3‑D orbit from Keplerian elements
    # --------------------------------------------------------------
    def get_rotation_matrix(self, inc, omega, node):
        i, w, n = np.radians([inc, omega, node])
        return np.array([
            [np.cos(n)*np.cos(w) - np.sin(n)*np.sin(w)*np.cos(i),
             -np.cos(n)*np.sin(w) - np.sin(n)*np.cos(w)*np.cos(i),
              np.sin(n)*np.sin(i)],
            [np.sin(n)*np.cos(w) + np.cos(n)*np.sin(w)*np.cos(i),
             -np.sin(n)*np.sin(w) + np.cos(n)*np.cos(w)*np.cos(i),
             -np.cos(n)*np.sin(i)],
            [np.sin(w)*np.sin(i), np.cos(w)*np.sin(i), np.cos(i)]
        ])

    def plot_orbit(self, planet_name):
        planet = self.data[self.data["pl_name"] == planet_name].iloc[0]

        a  = planet["semi_major_axis"]
        e  = planet["eccentricity"]
        inc = planet["inclination"]
        omega = planet["arg_periapsis"]
        node = planet["long_asc_node"]

        # Generate points on the ellipse in the orbital plane
        theta = np.linspace(0, 2*np.pi, 250)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        xy = np.vstack((r * np.cos(theta), r * np.sin(theta))).T

        # Rotate to 3‑D space
        R = self.get_rotation_matrix(inc, omega, node)
        
        # FIXED MATH: Transpose the coordinates properly before and after multiplication
        points_3d = np.vstack((xy.T, np.zeros_like(theta))) # Shape becomes (3, 250)
        rotated_points = R @ points_3d                      # (3,3) * (3,250) works perfectly!
        xyz = rotated_points.T                              # Transpose back to (250, 3) for plotting

        # ---- Matplotlib 3‑D drawing ----
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection="3d")
        ax.plot(xyz[:, 0], xyz[:, 1], xyz[:, 2], label=planet_name)
        ax.scatter(0, 0, 0, color="orange", s=150, label="Host Star")  # host star
        
        ax.set_title(f"Orbit of {planet_name}")
        ax.set_xlabel("X (AU)")
        ax.set_ylabel("Y (AU)")
        ax.set_zlabel("Z (AU)")
        ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OrbitPlotter()
    win.show()
    sys.exit(app.exec())