import numpy as np

def calculate_angle_between_lines(axis_start, axis_end, point1, point2):
    # Convert points to numpy arrays
    axis_start = np.array(axis_start)
    axis_end = np.array(axis_end)
    point1 = np.array(point1)
    point2 = np.array(point2)

    # Calculate direction vectors
    vector1 = axis_end - axis_start
    vector2 = point2 - point1

    # Normalize vectors
    vector1_norm = vector1 / np.linalg.norm(vector1)
    vector2_norm = vector2 / np.linalg.norm(vector2)

    # Calculate dot product and angle
    dot_product = np.dot(vector1_norm, vector2_norm)
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))  # Clipping for numerical stability
    angle_deg = np.degrees(angle_rad)

    return angle_rad, angle_deg

# Example points
axis_start = [ 0.1885837,  -2.61450801, -0.94083671]  # Start point of first line
axis_end = [-0.1665417,  1.1256594, -0.996178 ]    # End point of first line
x1, y1, z1 = 0.3250997864238513, -2.01980917502284, -0.9666000000000001     # Start point of second line
x2, y2, z2 = -0.3472997864238513, 1.6986091750228403, -0.9665999999999999    # End point of second line

# Calculate angle
angle_rad, angle_deg = calculate_angle_between_lines(
    axis_start, axis_end,
    [x1, y1, z1], [x2, y2, z2]
)

print(f"Angle between lines: {angle_rad:.4f} radians, {angle_deg:.2f} degrees")
