# AGRO-PULSE 3D CAD & Mechanical Hardware Bay
### Application ID: VK26-AU-PAI-0352 | Theme 7: Physical AI for Resilience and Inclusion
**Mentor Institute: Ashoka University | Team: TECHTONICS | Vishwakarma Awards 2026–27**

---

## 📦 3D CAD Files Manifest

| File | Format | Description | Compatibility |
|------|:------:|-------------|---------------|
| `agropulse_assembled.blend` | Blender 3D (`.blend`) | Fully assembled 7-subsystem master CAD assembly with PBR materials, studio lighting, and cameras. | Blender 4.x / 5.2+ |
| `agropulse_cad_model.blend` | Blender 3D (`.blend`) | **Exploded mechanical view** showing chassis, 4WD drivetrain, fluidic tank, avionics bay, and solar roof. | Blender 4.x / 5.2+ |
| `agropulse_assembled.stl` | Stereolithography (`.stl`) | Watertight solid mesh for additive manufacturing / 3D printing. | Cura, PrusaSlicer, Bambu Studio |
| `agropulse_cad_model.stl` | Stereolithography (`.stl`) | Exploded 3D mesh for mechanical fit analysis. | Any 3D Slicer |
| `agropulse_assembled.obj` / `.mtl` | Universal Wavefront OBJ | Textured universal 3D mesh for SolidWorks, Autodesk Fusion 360, FreeCAD, or WebGL viewers. | CAD / WebGL |
| `agropulse_3d_product_hero_render.png` | 1080p Image | 3D product hero render showing full rover assembly. | Image Viewer |
| `agropulse_fig1_architecture_cutaway.png` | 1080p Image | Internal cutaway illustrating the 200 mm spatial camera-to-nozzle offset. | Image Viewer |

---

## 🛠️ The 7 Mechanical & Pneumatic Sub-Assemblies

### 1. 4WD Chassis Frame (Aluminum 6061-T6)
- **Geometry:** 420 × 240 mm ladder frame with 30 × 30 mm square box extrusions.
- **Skid Plate:** 4.0 mm black-anodized aluminum underbelly plate for rock and furrow protection.
- **Ground Clearance:** 50.0 mm nominal field clearance.

### 2. 4WD Drivetrain & All-Terrain Wheels
- **Tires:** 4× 100 mm Ø (40 mm wide) deep-chevron lugged agricultural rubber tires.
- **Rims:** Gold-anodized machined aluminum rims with stainless steel drive shafts.
- **Motors:** 4× 60 RPM 20 kg·cm high-torque planetary geared DC motors.

### 3. Under-Chassis Optical Shroud & Vision Bay (Front)
- **Optical Tunnel Shroud:** Flexible rubberized/ABS enclosure (150 × 130 × 60 mm) blocking 100% of ambient sunlight glare and moving shadows.
- **Camera:** Downward-facing Omnivision OV9281 Global-Shutter monochrome camera ($X = +100\text{ mm}$).
- **Illumination:** Hardware-strobed high-CRI white LED ring array (8 LEDs).

### 4. Encoderless Sensor Fusion Mount (Center)
- **Optical Flow:** Downward PMW3901 tracking sensor measuring real-time ground-relative motion vectors ($\Delta x, \Delta y$).
- **Laser ToF Rangefinder:** Downward VL53L0X Time-of-Flight sensor for dynamic ground distance ($h_{\text{ground}}$) scaling.
- **IMU:** BMI160 6-DOF IMU mounted at vehicle center of mass for pitch/roll/yaw body compensation.

### 5. Precision Fluidic Injection System (200 mm Spatial Offset)
- **Chemical Tank:** 5-Liter translucent HDPE tank with threaded fill cap and level gradients.
- **Diaphragm Pump:** 12V 40 PSI heavy-duty pump mounted on anti-vibration rubber dampers.
- **Pulse Damper:** Hydraulic inline accumulator + 0–100 PSI pressure transducer.
- **3-Nozzle Manifold:** Positioned at $X = -100\text{ mm}$ (**exactly 200 mm behind the camera at $X = +100\text{ mm}$**).
- **Valves:** 3× high-speed micro-solenoid valves with sub-1.2 ms Active Zener shutoff and conical micro-nozzle tips.

### 6. Central Weatherproof Avionics Bay (IP65)
- **Tier 1:** Raspberry Pi 4B (Edge AI MobileNetV2-SSD perception & local Wi-Fi AP) with dual cooling fans.
- **Tier 2:** STM32G431 deterministic real-time MCU PCB + custom MOSFET Active Zener snubber driver board.
- **External Interfaces:** IP67 master toggle switch, dual status LEDs, and high-gain 2.4 GHz antenna.

### 7. Off-Grid 30W Flexible Solar Canopy & Power Deck
- **Structure:** 4× Anodized aluminum stanchion posts rising to $Z = 240\text{ mm}$.
- **Canopy:** 30W flexible monocrystalline solar panel curved as an aerodynamic roof.
- **Charge Controller:** 12V MPPT solar regulator.
- **Battery:** 12.8V 4S LiFePO4 battery pack (6+ hours continuous off-grid operation).

---

## 🖨️ 3D Printing & Fabrication Guidelines

- **Chassis & Brackets:** Polycarbonate (PC) or PETG (4 perimeters, 40% gyroid infill).
- **Optical Shroud & Tires:** TPU 95A / Shore-85A flexible filament for shock absorption and ground sealing.
- **Chemical Tank:** Chemical-resistant HDPE or Polypropylene.
