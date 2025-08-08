import tkinter as tk
from tkinter import ttk, messagebox

GRAVITY = 9.81

aircraft_presets = {
    "SR-71 Blackbird": {
        "wing_area": 170, "velocity": 983, "altitude": 25000,
        "aircraft_weight": 67600, "lift_coefficient": 0.067, "drag_coefficient": 0.00092
    },
    "Boeing 747": {
        "wing_area": 511, "velocity": 260, "altitude": 10668,
        "aircraft_weight": 1710000, "lift_coefficient": 0.52, "drag_coefficient": 0.022
    },
    "Concorde": {
        "wing_area": 360, "velocity": 605, "altitude": 17770,
        "aircraft_weight": 1090000, "lift_coefficient": 0.125, "drag_coefficient": 0.004
    },
    "F-22 Raptor": {
        "wing_area": 78, "velocity": 670, "altitude": 19000,
        "aircraft_weight": 288422, "lift_coefficient": 0.282, "drag_coefficient": 0.052
    },
    "B-52 Stratofortress": {
        "wing_area": 370, "velocity": 288, "altitude": 15000,
        "aircraft_weight": 1180000, "lift_coefficient": 0.784, "drag_coefficient": 0.0119
    }
}

def air_density_calculation(altitude):
    if altitude <= 11000:
        return 1.225
    elif altitude <= 20000:
        return 0.3639
    elif altitude <= 32000:
        return 0.0880
    elif altitude <= 47000:
        return 0.00132
    elif altitude <= 51000:
        return 0.0014
    elif altitude <= 71000:
        return 0.0009
    else:
        return 0

def convert_units(unit, wing_area, velocity, altitude, weight):
    if unit == "Imperial":
        wing_area = wing_area / 10.764  # ft² → m²
        velocity = velocity * 0.51444   # knots → m/s
        altitude = altitude / 3.281     # ft → m
        weight = weight * 4.448         # lb → N
    return wing_area, velocity, altitude, weight

def calculate_lift(cl, rho, area, vel):
    return 0.5 * cl * rho * area * vel ** 2

def calculate_drag(cd, rho, area, vel):
    return 0.5 * cd * rho * area * vel ** 2

def calculate_stall_speed(weight, rho, area, cl):
    return ((2 * weight) / (rho * area * cl)) ** 0.5

# Main GUI function
def calculate():
    if mode_var.get() == "Preset":
        preset = presets_var.get()
        if preset not in aircraft_presets:
            messagebox.showerror("Error", "Select a valid aircraft preset.")
            return
        data = aircraft_presets[preset]
        wing_area = data["wing_area"]
        velocity = data["velocity"]
        altitude = data["altitude"]
        aircraft_weight = data["aircraft_weight"]
        cl = data["lift_coefficient"]
        cd = data["drag_coefficient"]
    else:
        try:
            wing_area = float(entry_wing_area.get())
            velocity = float(entry_velocity.get())
            altitude = float(entry_altitude.get())
            aircraft_weight = float(entry_weight.get())
            cl = float(entry_cl.get())
            cd = float(entry_cd.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter all fields as numbers.")
            return
        if any(v <= 0 for v in [wing_area, velocity, altitude, aircraft_weight, cl, cd]):
            messagebox.showerror("Error", "All values must be greater than 0.")
            return

        wing_area, velocity, altitude, aircraft_weight = convert_units(
            unit_var.get(), wing_area, velocity, altitude, aircraft_weight
        )

    weight = (aircraft_weight / 9.806) * 9.81
    rho = air_density_calculation(altitude)
    lift = calculate_lift(cl, rho, wing_area, velocity)
    drag = calculate_drag(cd, rho, wing_area, velocity)
    stall_speed = calculate_stall_speed(weight, rho, wing_area, cl)

    result = f"Air Density: {rho:.3f} kg/m³\n"
    result += f"Lift Force: {lift:.2f} N\n"
    result += f"Drag Force: {drag:.2f} N\n"
    result += f"Stall Speed: {stall_speed:.2f} m/s\n"

    if lift >= weight and velocity > stall_speed:
        result += "\n✅ Aircraft is ready for flight!"
    elif velocity <= stall_speed:
        result += "\n⚠️ Velocity is below stall speed. Aircraft will stall."
    else:
        result += "\n❌ Aircraft is not generating enough lift."

    output_text.set(result)

def reset():
    # Clear input fields
    for entry in entries:
        entry.delete(0, tk.END)

    # Reset preset dropdown
    presets_var.set("")
    
    # Reset mode and units
    mode_var.set("Preset")
    unit_var.set("SI")

    # Clear output
    output_text.set("")

# Tkinter GUI setup
root = tk.Tk()
root.title("Aircraft Flight Calculator")

mode_var = tk.StringVar(value="Preset")
unit_var = tk.StringVar(value="SI")
output_text = tk.StringVar()

frame_top = ttk.Frame(root)
frame_top.pack(padx=10, pady=10)

ttk.Label(frame_top, text="Choose Mode:").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(frame_top, text="Preset", variable=mode_var, value="Preset").grid(row=0, column=1)
ttk.Radiobutton(frame_top, text="Custom", variable=mode_var, value="Custom").grid(row=0, column=2)

ttk.Label(frame_top, text="Presets:").grid(row=1, column=0, sticky="w")
presets_var = tk.StringVar()
preset_menu = ttk.Combobox(frame_top, textvariable=presets_var, values=list(aircraft_presets.keys()))
preset_menu.grid(row=1, column=1, columnspan=2, sticky="ew")

ttk.Label(frame_top, text="Units:").grid(row=2, column=0, sticky="w")
ttk.OptionMenu(frame_top, unit_var, "SI", "SI", "Imperial").grid(row=2, column=1, sticky="w")

frame_inputs = ttk.LabelFrame(root, text="Custom Input")
frame_inputs.pack(padx=10, pady=10, fill="x")

labels = [
    "Wing Area (m² or ft²):", "Velocity (m/s or knots):", "Altitude (m or ft):",
    "Weight (N or lb):", "Lift Coefficient (Cl):", "Drag Coefficient (Cd):"
]
entries = []
for i, label in enumerate(labels):
    ttk.Label(frame_inputs, text=label).grid(row=i, column=0, sticky="w")
    entry = ttk.Entry(frame_inputs)
    entry.grid(row=i, column=1, sticky="ew")
    entries.append(entry)

entry_wing_area, entry_velocity, entry_altitude, entry_weight, entry_cl, entry_cd = entries

ttk.Button(root, text="Calculate", command=calculate).pack(pady=5)
ttk.Label(root, textvariable=output_text, justify="left", wraplength=400).pack(padx=10, pady=10)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=5)

ttk.Button(btn_frame, text="Calculate", command=calculate).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Reset", command=reset).grid(row=0, column=1, padx=5)

root.mainloop()
