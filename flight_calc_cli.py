air_density = 0
GRAVITY = 9.81

# Added a preset dictionary, will consider adding more in the future
aircraft_presets = {
    "SR-71 Blackbird": {
        "wing_area": 170,
        "velocity": 983,
        "altitude": 25000,
        "aircraft_weight": 67600,
        "lift_coefficient": 0.067,
        "drag_coefficient": 0.00092 
    },
    "Boeing 747": {
        "wing_area": 511,
        "velocity": 260,
        "altitude": 10668,
        "aircraft_weight": 1710000,
        "lift_coefficient": 0.52,
        "drag_coefficient": 0.022
    },
    "Concorde": {
        "wing_area": 360,
        "velocity": 605,
        "altitude": 17770,
        "aircraft_weight": 1090000,
        "lift_coefficient": 0.125,
        "drag_coefficient": 0.004 
    },
    "F-22 Raptor": {
        "wing_area": 78,
        "velocity": 670,
        "altitude": 19000,
        "aircraft_weight": 288422,
        "lift_coefficient": 0.282,
        "drag_coefficient": 0.052
    },
    "B-52 Stratofortress": {
        "wing_area": 370,
        "velocity": 288,
        "altitude": 15000,
        "aircraft_weight": 1180000,
        "lift_coefficient": 0.784,
        "drag_coefficient": 0.0119
    }
}

# Allows you to choose either a custom or preset version for flight calculation
def choose_aircraft():
    print("\nAvailable aircraft presets:")
    for name in aircraft_presets:
        print(f" - {name}")
    print(" - custom")

    while True:
        choice = input("Enter aircraft name or 'custom' (case-sensitive): ")
        if choice in aircraft_presets:
            return aircraft_presets[choice]
        elif choice == "custom":
            return None
        else:
            print("Invalid choice. Choose from the list.")

# Checks and makes sure that input is both a number as well as a positive number

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Enter a number greater than 0.")
            else:
                return value
        except ValueError:
            print("Invalid input. Enter a numeric value.")

# converting imperial units to SI for easier calculation    
def convert_units(unit, wing_area, velocity, altitude, weight):
    if unit == "imperial":
        wing_area = wing_area / 10.764  # ft² → m²
        velocity = velocity * 0.51444   # knots → m/s
        altitude = altitude / 3.281     # ft → m
        weight = weight * 4.448         # lb → N
    return wing_area, velocity, altitude, weight
    
## Using a standard ISA model to calulcation air density based off of altitude (in kg/m^3)
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
    
# Next threee functions calculate lift, drag, and stall speeed respectively    
def calculate_lift(lift_coefficient, air_density, wing_area, velocity):
    return 0.5 * lift_coefficient * air_density * wing_area * velocity**2

def calculate_drag(drag_coefficient, air_density, wing_area, velocity):
    return 0.5 * drag_coefficient * air_density * wing_area * velocity**2

def calculate_stall_speed(weight, air_density, wing_area, lift_coefficient):
    return ((2 * weight) / (air_density * wing_area * lift_coefficient)) ** 0.5

# Main function where everything is run

def main():
    print("===Aircraft Flight Calculator===")
    print("Welcome to our aircraft flight calculator, where we check the ability of your aircraft to lift off and sustain flight!")

    # Runs the choose_aircraft() function, followed by an if/else statement based on whether you chose a preset aircraft or custom meatsurements.
    preset_data = choose_aircraft()

    if preset_data:

        # Pulls the numbers from the dictionary to save as variables for calculation
        wing_area = preset_data["wing_area"]
        velocity = preset_data["velocity"]
        altitude = preset_data["altitude"]
        aircraft_weight = preset_data["aircraft_weight"]
        lift_coefficient = preset_data["lift_coefficient"]
        drag_coefficient = preset_data["drag_coefficient"]

        weight = (aircraft_weight / 9.806) * 9.81

        air_density = air_density_calculation(altitude)
        lift = calculate_lift(lift_coefficient, air_density, wing_area, velocity)
        drag = calculate_drag(drag_coefficient, air_density, wing_area, velocity)
        stallSpeed = calculate_stall_speed(weight, air_density, wing_area, lift_coefficient)

        print("")
        print(f"=== Aircraft Flight Report ===")
        print(f"Air density: {air_density:.3f} kg/m³")
        print(f"Lift Force: {lift:.2f} N")
        print(f"Drag Force: {drag:.2f} N")
        if (lift >= weight and velocity > stallSpeed):
            print("✅ Aircraft is ready for flight!")
        elif (velocity <= stallSpeed):
            print("⚠️ Warning: Velocity is below stall speed. Aircraft will stall.")
        else:
            print("❌ Aircraft is not generating enough lift for flight.")
        print("")
    else:
        unit = input("Choose your units (SI or Imperial): ").lower()

        wing_area = get_positive_float("Enter wing area (m² or ft²): ")
        velocity = get_positive_float("Enter velocity (m/s or knots): ")
        altitude = get_positive_float("Enter altitude (m or ft): ")
        aircraft_weight = get_positive_float("Enter weight (Newtons or pounds): ")
        lift_coefficient = get_positive_float("Enter lift coefficient (Cl): ")
        drag_coefficient = get_positive_float("Enter drag coefficient (Cd): ")

        ## Ask for different inputs to calculate lift, drag and stall speed

        wing_area, velocity, altitude, aircraft_weight = convert_units(unit, wing_area, velocity, altitude, aircraft_weight)

        # Calculating weight to input for stall speed

        weight = (aircraft_weight / 9.806) * 9.81

        air_density = air_density_calculation(altitude)
        lift = calculate_lift(lift_coefficient, air_density, wing_area, velocity)
        drag = calculate_drag(drag_coefficient, air_density, wing_area, velocity)
        stallSpeed = calculate_stall_speed(weight, air_density, wing_area, lift_coefficient)

        print("")
        print("=== Aircraft Flight Report ===")
        print(f"Air density: {air_density:.3f} kg/m³")
        print(f"Lift Force: {lift:.2f} N")
        print(f"Drag Force: {drag:.2f} N")
        if (lift >= weight and velocity > stallSpeed):
            print("✅ Aircraft is ready for flight!")
        elif (velocity <= stallSpeed):
            print("⚠️ Warning: Velocity is below stall speed. Aircraft will stall.")
        else:
            print("❌ Aircraft is not generating enough lift for flight.")
        print("")

main()