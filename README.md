# Orbital Thermal ROM: Autonomous Thermal Management for Space Edge


## 1. Project Overview


Space orbital datacenters face a critical systems engineering constraint: **Heat Rejection**. In a vacuum, convection is negligible, and thermal management relies entirely on conduction and radiation.
This project implements a **Reduced Order Model (ROM)** Digital Twin. It takes high-fidelity Conjugate Heat Transfer (CHT) data generated in **OpenFOAM**, reduces the dimensionality using **Proper Orthogonal Decomposition (POD)**, and deploys a lightweight inference engine capable of predicting thermal hotspots in real-time on resource-constrained satellite hardware.
## 2. The Systems Architecture (V-Model)


* **System Constraint:** Max $T < 85^\circ C$ during peak compute loads.
* **Latency Requirement:** Thermal prediction $< 100ms$ (faster than the physical thermal time constant).
* **Solution:** Decouple the physics solver (offline) from the control logic (online).


## 3. Methodology


1. **CFD Simulation:** Used `chtMultiRegionSimpleFoam` to simulate electronics cooling in microgravity.
2. **Snapshot Collection:** Extracted temperature fields at varying power loads (10W - 100W).
3. **Model Reduction:** Applied Singular Value Decomposition (SVD) to extract dominant thermal energy modes.
4. **Edge Deployment:** Reconstructed full-field temperature maps on-orbit using linear superposition of modes: $T \approx \bar{T} + \sum a_i \phi_i$.
