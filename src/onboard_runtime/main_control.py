import numpy as np
import joblib
import time

class SatelliteThermalController:
    def __init__(self, model_path):
        # Load the lightweight ROM (approx 5MB vs 50GB raw data)
        data = joblib.load(model_path)
        self.modes = data['modes']       # Shape: (Points, Modes)
        self.mean_field = data['mean']   # Shape: (Points,)

        # System Limits
        self.MAX_TEMP_C = 85.0

    def get_sensor_readings(self):
        # In a real system, this reads from I2C/SPI thermistors
        # Here we simulate inputs (coefficients for the modes)
        # correlating to current CPU Load + Solar Radiation pressure
        return np.random.rand(self.modes.shape[1])

    def predict_field(self):
        """
        Reconstructs the full 3D temperature field in milliseconds.
        Equation: T_approx = T_mean + Phi * coefficients
        """
        coeffs = self.get_sensor_readings()
        reconstructed_T = self.mean_field + self.modes @ coeffs
        return reconstructed_T

    def control_loop(self):
        while True:
            start_time = time.time()

            # 1. Sense & Infer
            current_temp_field = self.predict_field()
            max_hotspot = np.max(current_temp_field)

            # 2. Control Logic (Bang-Bang or PID)
            if max_hotspot > self.MAX_TEMP_C:
                print(f"[ALERT] Predicted Hotspot: {max_hotspot:.2f}C. Throttling CPU.")
                self.actuate_thermal_control(mode="ACTIVE_COOLING")
            else:
                print(f"[NOMINAL] Peak Temp: {max_hotspot:.2f}C")

            # 3. Telemetry Check
            # Ensure loop runs at 10Hz (Systems Constraint)
            elapsed = time.time() - start_time
            time.sleep(max(0, 0.1 - elapsed))

    def actuate_thermal_control(self, mode):
        # Logic to trigger Louvers or VCHPs (Variable Conductance Heat Pipes)
        pass

if __name__ == "__main__":
    sat = SatelliteThermalController("../../data/trained_modes/thermal_rom.pkl")
    sat.control_loop()
