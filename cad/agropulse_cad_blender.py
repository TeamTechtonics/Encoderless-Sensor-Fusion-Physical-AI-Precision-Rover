"""
================================================================================
  AGRO-PULSE 3D CAD GENERATOR — BLENDER 5.2 AUTOMATION SCRIPT
  Project: AGRO-PULSE (Physical AI Agricultural Field Rover)
  Application ID: VK26-AU-PAI-0352
  Theme 7: Physical AI for Resilience and Inclusion (Host: Ashoka University)
  Team: TECHTONICS | Vishwakarma Awards 2026-27

  CAD SUBSYSTEMS & PARAMETRIC ARCHITECTURE:
  ------------------------------------------------
  1. Chassis Frame: 30x30mm 6061-T6 Aluminum box extrusion ladder chassis
  2. 4WD Drivetrain: 4x 100mm Ø lugged all-terrain rubber wheels + 60 RPM gearmotors
  3. Optical Shroud & Vision Bay: Light-sealed shroud + OV9281 Global-Shutter + LED Ring
  4. Ground Sensor Fusion Mount: PMW3901 Optical Flow + VL53L0X ToF Height + BMI160 IMU
  5. Precision Fluidics: 5L HDPE Tank, 12V 40PSI Diaphragm Pump, 200mm Spatial Integration
     Manifold with 3x Active-Zener Micro-Solenoid Nozzles
  6. Avionics Bay (IP65): Dual-tier Raspberry Pi 4B + STM32G431 Deterministic MCU PCB
  7. Solar Canopy & Power: 30W Flexible Solar Panel Roof, MPPT Controller & LiFePO4 Pack

  HOW TO OPEN IN BLENDER GUI:
    /home/akshaya/Downloads/blender-5.2.1-linux-x64/blender \
        /home/akshaya/Downloads/viswakarma/agropulse_assembled.blend
================================================================================
"""

import bpy
import math
import os

OUTPUT_ASSEMBLED = "/home/akshaya/Downloads/viswakarma/agropulse_assembled.blend"
OUTPUT_EXPLODED  = "/home/akshaya/Downloads/viswakarma/agropulse_cad_model.blend"
OUTPUT_STL       = "/home/akshaya/Downloads/viswakarma/agropulse_assembled.stl"
OUTPUT_OBJ       = "/home/akshaya/Downloads/viswakarma/agropulse_assembled.obj"
RENDER_HERO      = "/home/akshaya/Downloads/viswakarma/agropulse_3d_product_hero_render.png"
RENDER_CUTAWAY   = "/home/akshaya/Downloads/viswakarma/agropulse_fig1_architecture_cutaway.png"

MM = 0.001   # Millimeter to Blender meter scale factor

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.lights, bpy.data.cameras):
        for item in list(col):
            col.remove(item)

def make_material(name, rgb, rough=0.35, metal=0.0, alpha=1.0, emit=None, emit_str=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if alpha < 1.0:
        m.blend_method = 'BLEND'
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value  = (*rgb[:3], 1.0)
    b.inputs["Roughness"].default_value   = rough
    b.inputs["Metallic"].default_value    = metal
    b.inputs["Alpha"].default_value       = alpha
    if emit:
        b.inputs["Emission Color"].default_value    = (*emit[:3], 1.0)
        b.inputs["Emission Strength"].default_value = emit_str
    return m

def add_box(name, center, size, material=None):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(center[0]*MM, center[1]*MM, center[2]*MM),
        scale=(size[0]*MM, size[1]*MM, size[2]*MM)
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def add_cyl(name, center, radius, height, rotation=(0,0,0), material=None, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius*MM,
        depth=height*MM,
        location=(center[0]*MM, center[1]*MM, center[2]*MM),
        rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def build_agropulse_subsystems():
    # Materials Palette
    m_al_silver   = make_material("Al6061_Extrusion", (0.85, 0.87, 0.90), rough=0.25, metal=0.90)
    m_al_black    = make_material("Anodized_Black_Al", (0.10, 0.11, 0.13), rough=0.35, metal=0.85)
    m_rubber_tire = make_material("Lugged_Rubber_Tire", (0.04, 0.04, 0.05), rough=0.85, metal=0.0)
    m_rim_gold    = make_material("Wheel_Rim_Anodized", (0.85, 0.65, 0.15), rough=0.30, metal=0.80)
    m_shroud_abs  = make_material("Optical_Shroud_Matte", (0.12, 0.13, 0.15), rough=0.60, metal=0.0)
    m_tank_hdpe   = make_material("Chemical_Tank_HDPE", (0.88, 0.92, 0.95), rough=0.20, metal=0.05, alpha=0.65)
    m_fluid_chem  = make_material("Agrochemical_Liquid", (0.15, 0.75, 0.45), rough=0.15, metal=0.1, alpha=0.60)
    m_pump_metal  = make_material("Diaphragm_Pump_Cast", (0.22, 0.25, 0.28), rough=0.45, metal=0.75)
    m_brass_valve = make_material("Brass_Solenoid_Body", (0.78, 0.60, 0.20), rough=0.30, metal=0.85)
    m_ss_plunger  = make_material("Stainless_SS316", (0.90, 0.92, 0.94), rough=0.20, metal=0.95)
    m_solar_panel = make_material("Solar_Canopy_Mono", (0.02, 0.05, 0.12), rough=0.15, metal=0.40)
    m_solar_frame = make_material("Solar_Frame_Blue", (0.05, 0.40, 0.85), rough=0.35, metal=0.60)
    m_pcb_fr4     = make_material("Electronics_FR4", (0.05, 0.45, 0.25), rough=0.35, metal=0.10)
    m_acrylic_lid = make_material("Enclosure_Clear_Lid", (0.85, 0.92, 0.98), rough=0.10, metal=0.0, alpha=0.40)
    m_sensor_gold = make_material("Sensor_Optics_Gold", (0.95, 0.75, 0.20), rough=0.25, metal=0.90)
    m_lens_glass  = make_material("Camera_Lens_Coated", (0.15, 0.20, 0.35), rough=0.05, metal=0.10, alpha=0.85)
    m_led_emit    = make_material("Strobe_LED_Array", (1.0, 1.0, 1.0), rough=0.10, metal=0.0, emit=(1.0, 1.0, 1.0), emit_str=8.0)
    m_hose_poly   = make_material("Reinforced_Fluid_Hose", (0.10, 0.45, 0.85), rough=0.40, metal=0.0)

    # 1. CHASSIS FRAME (420x240mm, Z = 65mm)
    add_box("Chassis_Rail_Left", (0, 110, 65), (420, 30, 30), m_al_silver)
    add_box("Chassis_Rail_Right", (0, -110, 65), (420, 30, 30), m_al_silver)
    add_box("Cross_Member_Front", (195, 0, 65), (30, 190, 30), m_al_silver)
    add_box("Cross_Member_MidFront", (65, 0, 65), (30, 190, 30), m_al_silver)
    add_box("Cross_Member_MidRear", (-65, 0, 65), (30, 190, 30), m_al_silver)
    add_box("Cross_Member_Rear", (-195, 0, 65), (30, 190, 30), m_al_silver)
    add_box("Chassis_Skid_Plate", (0, 0, 48), (410, 240, 4), m_al_black)

    # 2. 4WD WHEELS (100mm Ø)
    wheel_coords = [
        ("Front_Left",  140,  155),
        ("Front_Right", 140, -155),
        ("Rear_Left",  -140,  155),
        ("Rear_Right", -140, -155)
    ]
    for label, wx, wy in wheel_coords:
        rot_y = (math.pi / 2, 0, 0)
        motor_y = 115 if wy > 0 else -115
        add_cyl(f"Motor_Gearbox_{label}", (wx, motor_y, 65), 18, 45, rot_y, m_al_black)
        shaft_y = 138 if wy > 0 else -138
        add_cyl(f"Drive_Shaft_{label}", (wx, shaft_y, 50), 6, 20, rot_y, m_ss_plunger)
        add_cyl(f"Wheel_Rim_{label}", (wx, wy, 50), 38, 34, rot_y, m_rim_gold)
        add_cyl(f"Tire_Tread_{label}", (wx, wy, 50), 50, 40, rot_y, m_rubber_tire)
        for i in range(12):
            ang = i * (2 * math.pi / 12)
            lx = wx + 48 * math.cos(ang)
            lz = 50 + 48 * math.sin(ang)
            add_box(f"Lug_{label}_{i}", (lx, wy, lz), (6, 38, 8), m_rubber_tire)

    # 3. OPTICAL SHROUD & CAMERA (X = +100mm)
    add_box("Optical_Shroud_Top", (100, 0, 78), (150, 130, 6), m_shroud_abs)
    add_box("Optical_Shroud_Left", (100, 65, 45), (150, 6, 60), m_shroud_abs)
    add_box("Optical_Shroud_Right", (100, -65, 45), (150, 6, 60), m_shroud_abs)
    add_box("Optical_Shroud_FrontSkirt", (175, 0, 45), (6, 130, 60), m_shroud_abs)
    add_box("Shroud_Dust_Fringe", (100, 0, 18), (148, 128, 4), m_rubber_tire)

    add_box("OV9281_Camera_PCB", (100, 0, 82), (32, 32, 4), m_pcb_fr4)
    add_cyl("OV9281_Lens_Barrel", (100, 0, 72), 8, 16, (0, 0, 0), m_al_black)
    add_cyl("OV9281_Optical_Glass", (100, 0, 63), 6, 2, (0, 0, 0), m_lens_glass)

    add_cyl("Strobe_LED_Ring_Bezel", (100, 0, 70), 22, 6, (0, 0, 0), m_al_black)
    for i in range(8):
        ang = i * (2 * math.pi / 8)
        led_x = 100 + 16 * math.cos(ang)
        led_y = 0 + 16 * math.sin(ang)
        add_cyl(f"Strobe_LED_{i}", (led_x, led_y, 67), 3, 3, (0, 0, 0), m_led_emit)

    # 4. SENSOR FUSION (X = +15mm)
    add_box("Sensor_Fusion_Bracket", (15, 0, 52), (45, 55, 5), m_al_black)
    add_box("PMW3901_PCB", (15, 14, 55), (20, 20, 3), m_pcb_fr4)
    add_cyl("PMW3901_PinHole_Lens", (15, 14, 49), 4, 6, (0, 0, 0), m_sensor_gold)
    add_box("VL53L0X_ToF_PCB", (15, -14, 55), (20, 16, 3), m_pcb_fr4)
    add_box("VL53L0X_Emitter_Optic", (15, -14, 49), (8, 12, 4), m_al_black)
    add_box("BMI160_IMU_Chip", (0, 0, 82), (12, 12, 3), m_pcb_fr4)

    # 5. FLUIDICS & 200mm MANIFOLD (X = -100mm)
    add_box("Chemical_Tank_Body", (-90, 0, 125), (140, 160, 95), m_tank_hdpe)
    add_box("Chemical_Liquid_Fill", (-90, 0, 115), (134, 154, 75), m_fluid_chem)
    add_cyl("Tank_Fill_Neck", (-90, 45, 178), 22, 16, (0, 0, 0), m_al_black)
    add_cyl("Tank_Breather_Cap", (-90, 45, 188), 26, 10, (0, 0, 0), m_al_silver)

    add_box("Diaphragm_Pump_Motor", (-20, 50, 98), (75, 45, 45), m_pump_metal)
    add_cyl("Pump_Pressure_Head", (-20, 80, 98), 22, 28, (0, math.pi/2, 0), m_al_black)
    add_cyl("Pressure_Accumulator", (-20, -50, 98), 18, 55, (0, 0, 0), m_ss_plunger)
    add_cyl("Pressure_Transducer_Sensor", (-55, 60, 85), 10, 24, (math.pi/2, 0, 0), m_brass_valve)

    add_cyl("Hose_Tank_To_Pump", (-55, 50, 85), 5, 60, (0, math.pi/2, 0), m_hose_poly)
    add_cyl("Hose_Pump_To_Manifold", (-60, 0, 75), 5, 80, (math.pi/2, 0, 0), m_hose_poly)

    add_box("Spray_Manifold_Rail", (-100, 0, 68), (22, 160, 16), m_al_black)
    for idx, ny in enumerate([-60, 0, 60]):
        add_cyl(f"Solenoid_Valve_Body_{idx}", (-100, ny, 62), 12, 28, (0, 0, 0), m_brass_valve)
        add_cyl(f"Solenoid_Plunger_{idx}", (-100, ny, 72), 8, 16, (0, 0, 0), m_ss_plunger)
        add_cyl(f"Micro_Nozzle_Tip_{idx}", (-100, ny, 44), 5, 10, (0, 0, 0), m_brass_valve)
        add_cyl(f"Spray_Plume_Cone_{idx}", (-100, ny, 20), 18, 38, (0, 0, 0), m_fluid_chem, vertices=16)

    # 6. CENTRAL AVIONICS BAY (X = +60mm)
    add_box("Avionics_Enclosure_Base", (60, 0, 105), (130, 150, 45), m_al_black)
    add_box("Avionics_Clear_Lid", (60, 0, 130), (132, 152, 6), m_acrylic_lid)

    add_box("Raspberry_Pi_4B_PCB", (60, -35, 95), (85, 56, 3), m_pcb_fr4)
    add_box("Pi4B_Dual_Heatsink", (60, -35, 103), (50, 40, 12), m_al_silver)
    add_cyl("Pi_Cooling_Fan_1", (48, -35, 110), 12, 3, (0, 0, 0), m_al_black)
    add_cyl("Pi_Cooling_Fan_2", (72, -35, 110), 12, 3, (0, 0, 0), m_al_black)

    add_box("STM32G431_Control_PCB", (60, 35, 95), (85, 60, 3), m_pcb_fr4)
    for i in range(3):
        add_box(f"MOSFET_Driver_{i}", (45 + i*15, 55, 103), (8, 4, 14), m_al_black)
    add_box("Zener_Snubber_Module", (60, 20, 100), (22, 14, 6), m_al_silver)

    add_cyl("Telemetry_Antenna_Base", (115, 65, 130), 6, 12, (0, 0, 0), m_brass_valve)
    add_cyl("Telemetry_Antenna_Whip", (115, 65, 185), 3, 100, (0, 0, 0), m_rubber_tire)
    add_cyl("Master_Power_Switch", (115, -60, 115), 8, 14, (math.pi/2, 0, 0), m_rim_gold)
    add_cyl("LED_Indicator_Green", (115, -45, 115), 4, 6, (math.pi/2, 0, 0), m_led_emit)
    add_cyl("LED_Indicator_Blue", (115, -35, 115), 4, 6, (math.pi/2, 0, 0), m_solar_frame)

    # 7. SOLAR CANOPY & POWER DECK
    for slabel, sx, sy in [("Front_L", 170, 105), ("Front_R", 170, -105), ("Rear_L", -170, 105), ("Rear_R", -170, -105)]:
        add_cyl(f"Canopy_Post_{slabel}", (sx, sy, 150), 6, 170, (0, 0, 0), m_al_silver)

    add_box("LiFePO4_Battery_Pack", (-15, 0, 150), (120, 75, 45), m_al_black)
    add_box("MPPT_Charge_Controller", (60, 0, 150), (60, 50, 25), m_solar_frame)

    add_box("Solar_Canopy_Substrate", (0, 0, 240), (430, 270, 5), m_solar_frame)
    add_box("Solar_Cells_Active_Array", (0, 0, 243), (410, 250, 2), m_solar_panel)
    for bx in range(-180, 190, 45):
        add_box(f"Solar_Busbar_X_{bx}", (bx, 0, 244), (2, 246, 1), m_al_silver)
    for by in range(-100, 110, 50):
        add_box(f"Solar_Busbar_Y_{by}", (0, by, 244), (406, 2, 1), m_al_silver)

def setup_scene_environment():
    # Target center Empty at (0, 0, 120mm)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0.0, 0.0, 0.12))
    target = bpy.context.active_object
    target.name = "Target_Center"

    # Key Light
    bpy.ops.object.light_add(type='AREA', location=(0.7, -0.8, 0.9))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 220.0
    key.data.size = 0.8
    key.data.color = (1.0, 0.98, 0.92)

    # Fill Light
    bpy.ops.object.light_add(type='AREA', location=(-0.7, -0.6, 0.7))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 110.0
    fill.data.size = 1.0
    fill.data.color = (0.80, 0.92, 1.0)

    # Back Rim Light
    bpy.ops.object.light_add(type='SPOT', location=(0.0, 0.9, 0.9))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 240.0
    rim.data.spot_size = math.radians(75)

    # Under-Chassis Soil Glow Light
    bpy.ops.object.light_add(type='POINT', location=(0.0, 0.0, 0.03))
    glow = bpy.context.active_object
    glow.name = "Glow_Light"
    glow.data.energy = 20.0
    glow.data.color = (0.2, 0.85, 0.45)

    # 1. Product Hero Camera with Track To constraint
    bpy.ops.object.camera_add(location=(0.68, -0.72, 0.42))
    cam_hero = bpy.context.active_object
    cam_hero.name = "Camera_Product_Hero"
    cam_hero.data.lens = 48
    c1 = cam_hero.constraints.new(type='TRACK_TO')
    c1.target = target
    c1.track_axis = 'TRACK_NEGATIVE_Z'
    c1.up_axis = 'UP_Y'

    # 2. Side Cutaway Camera with Track To constraint
    bpy.ops.object.camera_add(location=(0.0, -0.92, 0.16))
    cam_cutaway = bpy.context.active_object
    cam_cutaway.name = "Camera_Side_Cutaway"
    cam_cutaway.data.lens = 42
    c2 = cam_cutaway.constraints.new(type='TRACK_TO')
    c2.target = target
    c2.track_axis = 'TRACK_NEGATIVE_Z'
    c2.up_axis = 'UP_Y'

    # Render settings
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = True

def render_and_export():
    # Save Assembled Master Blend File
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_ASSEMBLED)
    print(f"Saved: {OUTPUT_ASSEMBLED}")

    # Export STL
    for obj in bpy.context.scene.objects:
        obj.select_set(obj.type == 'MESH')
    try:
        bpy.ops.wm.stl_export(filepath=OUTPUT_STL)
        print(f"Exported: {OUTPUT_STL}")
    except Exception as e:
        print("STL note:", e)

    # Export OBJ
    try:
        bpy.ops.wm.obj_export(filepath=OUTPUT_OBJ)
        print(f"Exported: {OUTPUT_OBJ}")
    except Exception as e:
        print("OBJ note:", e)

    # Render Hero View
    cam_hero = bpy.data.objects.get("Camera_Product_Hero")
    if cam_hero:
        bpy.context.scene.camera = cam_hero
        bpy.context.scene.render.filepath = RENDER_HERO
        bpy.ops.render.render(write_still=True)
        print(f"Rendered: {RENDER_HERO}")

    # Render Cutaway View
    cam_cutaway = bpy.data.objects.get("Camera_Side_Cutaway")
    if cam_cutaway:
        bpy.context.scene.camera = cam_cutaway
        bpy.context.scene.render.filepath = RENDER_CUTAWAY
        bpy.ops.render.render(write_still=True)
        print(f"Rendered: {RENDER_CUTAWAY}")

if __name__ == "__main__":
    clear_scene()
    build_agropulse_subsystems()
    setup_scene_environment()
    render_and_export()
