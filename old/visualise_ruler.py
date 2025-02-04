import math
import os

def calculate_range_y(obj_file):
    """
    Calculate the range of y-coordinates in the given OBJ file.

    Args:
        obj_file (str): Path to the OBJ file.

    Returns:
        float: Range of y-coordinates (max_y - min_y).
    """
    min_y, max_y = float('inf'), float('-inf')

    with open(obj_file, 'r') as file:
        for line in file:
            if line.startswith("v "):
                components = line.split()
                y = float(components[2])  # Extract the y-coordinate
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    return max_y - min_y

def add_points_to_obj(obj_file, focus_point, fb_tilt, side_tilt, num_points=1000):
    """
    Add a series of points at regular intervals between two endpoints in an OBJ file.

    Args:
        obj_file (str): Path to the input OBJ file.
        focus_point (tuple): Coordinates of the focus point (x, y, z).
        fb_tilt (float): Front-back tilt in degrees.
        side_tilt (float): Side tilt in degrees.
        num_points (int): Number of points to add between the endpoints (default: 1000).

    Returns:
        str: Path to the output OBJ file with the added points.
    """
    # Focus point coordinates
    x, y, z = focus_point

    # Calculate tilt angles in radians
    fb_tilt_rad = math.radians(fb_tilt)
    side_tilt_rad = math.radians(side_tilt)

    # Calculate the range of y-coordinates and determine line length
    y_range = calculate_range_y(obj_file)
    line_length = 1.5 * y_range

    # Calculate deviations for the red line
    delta_y_fb = math.sin(fb_tilt_rad) * (line_length / 2)
    delta_z_fb = math.cos(fb_tilt_rad) * (line_length / 2)

    delta_x_side = math.sin(side_tilt_rad) * (line_length / 2)
    delta_y_side = math.cos(side_tilt_rad) * (line_length / 2)

    # Compute the two endpoints of the red line
    # The focus point is the midpoint, so adjust accordingly
    x1 = x - delta_x_side
    y1 = y - delta_y_fb - delta_y_side
    z1 = z - delta_z_fb

    x2 = x + delta_x_side
    y2 = y + delta_y_fb + delta_y_side
    z2 = z + delta_z_fb

    # Read the original OBJ file
    with open(obj_file, 'r') as file:
        lines = file.readlines()

    # Separate sections of the file
    vertices = []
    normals = []
    other_lines = []

    for line in lines:
        if line.startswith("v "):
            vertices.append(line)
        elif line.startswith("vn "):
            normals.append(line)
        else:
            other_lines.append(line)

    # Calculate step size for evenly spaced points
    step_size = 1.0 / (num_points + 1)

    # Add points at regular intervals
    for i in range(1, num_points + 1):
        t = i * step_size
        x_point = x1 + (x2 - x1) * t
        y_point = y1 + (y2 - y1) * t
        z_point = z1 + (z2 - z1) * t
        vertices.append(f"v {x_point} {y_point} {z_point}\n")

    # Determine output file name
    base_name, ext = os.path.splitext(obj_file)
    output_file = f"{base_name}_with_points{ext}"

    # Write the modified OBJ file, preserving all information
    with open(output_file, 'w') as file:
        file.writelines(vertices)
        file.writelines(normals)
        file.writelines(other_lines)

    return output_file


# Example usage
if __name__ == "__main__":
    obj_file = input("Enter the path to the input OBJ file: ").strip()
    focus_x = float(input("Enter the x-coordinate of the focus point: "))
    focus_y = float(input("Enter the y-coordinate of the focus point: "))
    focus_z = float(input("Enter the z-coordinate of the focus point: "))
    focus_point = (focus_x, focus_y, focus_z)
    fb_tilt = float(input("Enter the front-back tilt in degrees: "))
    side_tilt = float(input("Enter the side tilt in degrees: "))

    output_file = add_points_to_obj(obj_file, focus_point, fb_tilt, side_tilt)
    print(f"Modified OBJ file saved as: {output_file}")
