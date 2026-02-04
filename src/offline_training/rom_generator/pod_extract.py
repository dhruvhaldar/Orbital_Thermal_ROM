import numpy as np
import pyvista as pv
from scipy.linalg import svd
import joblib

class ThermalPOD:
    def __init__(self, case_path):
        self.case_path = case_path
        self.snapshots = []

    def load_openfoam_data(self):
        """
        Reads VTK data exported from OpenFOAM using PyVista.
        Parses temperature fields 'T' from the electronics region.
        """
        print(f"Loading VTK snapshots from {self.case_path}...")
        # (Mock logic: In reality, you'd loop through time directories)
        mesh = pv.read(f"{self.case_path}/postProcessing/sample/0/T.vtk")
        self.snapshots.append(mesh['T'])
        # Convert list to Matrix X (Space x Time)
        self.X = np.array(self.snapshots).T

    def compute_modes(self, energy_threshold=0.99):
        """
        Performs SVD to extract dominant thermal modes.
        """
        print("Computing SVD...")
        U, S, Vt = svd(self.X, full_matrices=False)

        # Calculate energy captured
        cumulative_energy = np.cumsum(S**2) / np.sum(S**2)
        r = np.searchsorted(cumulative_energy, energy_threshold) + 1

        print(f"Reduced model to {r} modes (captured {energy_threshold*100}% energy).")

        self.Phi = U[:, :r]  # Spatial modes
        self.mean_T = np.mean(self.X, axis=1)

        return self.Phi, self.mean_T

    def save_model(self, output_path):
        joblib.dump({'modes': self.Phi, 'mean': self.mean_T}, output_path)

if __name__ == "__main__":
    pod = ThermalPOD("../openfoam_case")
    pod.load_openfoam_data()
    pod.compute_modes()
    pod.save_model("../../../data/trained_modes/thermal_rom.pkl")
