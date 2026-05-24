import math

# --- Simulation Constants ---
GRAVITY = 9.81  # m/s^2

# --- Core Simulation Functions ---

def calculate_trajectory(initial_velocity, launch_angle_deg, time_steps=100, max_time=None):
    """
    Calculates the trajectory points for a projectile.
    Args:
        initial_velocity (float): Initial speed in m/s.
        launch_angle_deg (float): Launch angle in degrees.
        time_steps (int): Number of points to calculate along the trajectory.
        max_time (float, optional): Maximum time for the simulation. If None, calculated from trajectory.
    Returns:
        list: A list of (x, y) tuples representing the trajectory.
    """
    angle_rad = math.radians(launch_angle_deg)
    vx = initial_velocity * math.cos(angle_rad)
    vy0 = initial_velocity * math.sin(angle_rad)

    if max_time is None:
        # Calculate time of flight
        time_of_flight = (2 * vy0) / GRAVITY
        max_time = time_of_flight * 1.1 # Add a little extra time to show landing

    dt = max_time / time_steps
    trajectory_points = []

    for i in range(time_steps + 1):
        t = i * dt
        x = vx * t
        y = vy0 * t - 0.5 * GRAVITY * t**2
        if y < 0: # Stop when it hits the ground
            y = 0
            if t > 0 and trajectory_points and trajectory_points[-1][1] == 0:
                break # Already landed
        trajectory_points.append((x, y))
        if y == 0 and t > 0: # If it just hit the ground after starting
            break

    return trajectory_points

def get_trajectory_summary(initial_velocity, launch_angle_deg):
    """Calculates max height, range, and time of flight."""
    angle_rad = math.radians(launch_angle_deg)
    vy0 = initial_velocity * math.sin(angle_rad)
    vx = initial_velocity * math.cos(angle_rad)

    time_of_flight = (2 * vy0) / GRAVITY
    max_height = (vy0**2) / (2 * GRAVITY)
    horizontal_range = vx * time_of_flight

    return max_height, horizontal_range, time_of_flight

# --- "AI" (Intelligent Assistant) Function ---
# This function demonstrates a simple "offline AI simulation" by calculating
# solutions to a problem, rather than just simulating a given input.
# It uses mathematical models to provide insights, similar to how an AI might
# analyze data to give recommendations, but entirely offline and rule-based.
def calculate_angles_to_hit_target(initial_velocity, target_distance):
    """
    Calculates the two possible launch angles (in degrees) required to hit a target
    at a given distance on level ground, with a specified initial velocity.
    """
    g = GRAVITY
    x = target_distance
    v0 = initial_velocity

    # Formula derived from projectile motion for range R:
    # R = (v0^2 * sin(2*theta)) / g
    # sin(2*theta) = (g * R) / v0^2
    arg = (g * x) / (v0**2)

    if arg > 1 or arg < 0: # Target is unreachable (e.g., too far or negative distance)
        return [] # Return empty list if no real solution

    # Calculate the two possible angles
    angle1_rad = 0.5 * math.asin(arg)
    angle2_rad = 0.5 * (math.pi - math.asin(arg)) # The complementary angle

    angle1_deg = math.degrees(angle1_rad)
    angle2_deg = math.degrees(angle2_rad)
    
    # Ensure angles are physically sensible (0-90 degrees) and unique
    valid_angles = []
    if 0 <= angle1_deg <= 90:
        valid_angles.append(angle1_deg)
    if 0 <= angle2_deg <= 90 and abs(angle2_deg - angle1_deg) > 0.01: # Avoid near-duplicate for max range
        valid_angles.append(angle2_deg)

    return sorted(valid_angles)


# --- Demonstration ---
if __name__ == "__main__":
    print("--- SimGemma: Offline Projectile Motion Simulator ---")
    print("This example demonstrates a simple STEM simulation that works offline.")
    print("It also includes a basic 'intelligent assistant' feature (offline AI) ")
    print("to help solve problems, rather than just observe simulations.\n")

    # Scenario 1: Basic Simulation
    print("Scenario 1: Simulating a projectile with given initial conditions.")
    initial_v1 = 30.0  # m/s
    angle1 = 45.0      # degrees
    print(f"  Initial Velocity: {initial_v1} m/s, Launch Angle: {angle1}°")

    trajectory1 = calculate_trajectory(initial_v1, angle1)
    max_h1, range1, time_f1 = get_trajectory_summary(initial_v1, angle1)

    print(f"  Calculated Max Height: {max_h1:.2f} m")
    print(f"  Calculated Horizontal Range: {range1:.2f} m")
    print(f"  Calculated Time of Flight: {time_f1:.2f} s")
    print("  (Trajectory points calculated, but not printed for brevity)\n")

    # Scenario 2: Using the "Offline AI Assistant" to find angles for a target
    print("Scenario 2: Using the 'Offline AI Assistant' to find launch angles to hit a target.")
    initial_v2 = 40.0  # m/s
    target_dist = 120.0 # meters
    print(f"  Given Initial Velocity: {initial_v2} m/s, Target Distance: {target_dist} m")

    # This is the "AI" part: it calculates solutions based on physics principles.
    # It's 'offline' because it uses local computations, no external services.
    # It's 'AI-like' because it helps solve a problem proactively,
    # rather than just reacting to user input for a single simulation run.
    required_angles = calculate_angles_to_hit_target(initial_v2, target_dist)

    if required_angles:
        print(f"  The 'AI Assistant' suggests the following launch angles to hit {target_dist}m:")
        for angle in required_angles:
            print(f"    - {angle:.2f}°")
            # Demonstrate by simulating one of the suggested angles
            traj_ai = calculate_trajectory(initial_v2, angle)
            _, range_ai, _ = get_trajectory_summary(initial_v2, angle)
            print(f"      (Simulating {angle:.2f}°: Range achieved {range_ai:.2f} m)")
    else:
        print(f"  The 'AI Assistant' determined that {target_dist}m is unreachable with {initial_v2} m/s.")
        max_possible_range = (initial_v2**2) / GRAVITY
        print(f"  (Maximum possible range with {initial_v2} m/s is {max_possible_range:.2f} m)\n")

    # Scenario 3: Target unreachable
    print("Scenario 3: Target unreachable demonstration.")
    initial_v3 = 20.0  # m/s
    target_dist3 = 100.0 # meters (too far for 20 m/s)
    print(f"  Given Initial Velocity: {initial_v3} m/s, Target Distance: {target_dist3} m")
    required_angles3 = calculate_angles_to_hit_target(initial_v3, target_dist3)
    if not required_angles3:
        print(f"  The 'AI Assistant' confirmed that {target_dist3}m is unreachable with {initial_v3} m/s.")
        max_possible_range3 = (initial_v3**2) / GRAVITY
        print(f"  (Maximum possible range with {initial_v3} m/s is {max_possible_range3:.2f} m)\n")
    else:
        print(f"  Unexpected: Angles found for unreachable target. {required_angles3}")

    print("--- End of SimGemma Example ---")