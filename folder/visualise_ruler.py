import math
import os

def add_red_line_to_obj(obj_file, output_file, focus_point, fb_tilt, side_tilt):
    x, y, z = focus_point

    # Convert angles to radians
    fb_tilt_rad = math.radians(fb_tilt)
    side_tilt_rad = math.radians(side_tilt)

    # Calculate direction vector of the line based on the tilts
    dx = math.cos(fb_tilt_rad) * math.sin(side_tilt_rad)
    dy = math.sin(fb_tilt_rad)
    dz = math.cos(fb_tilt_rad) * math.cos(side_tilt_rad)

    # Normalize the direction vector
    magnitude = math.sqrt(dx**2 + dy**2 + dz**2)
    dx /= magnitude
    dy /= magnitude
    dz /= magnitude

    # Calculate endpoints of the line segment
    half_length = 15  # Half of 30 meters
    x1 = x - half_length * dx
    y1 = y - half_length * dy
    z1 = z - half_length * dz

    x2 = x + half_length * dx
    y2 = y + half_length * dy
    z2 = z + half_length * dz

    # Read the original OBJ file
    with open(obj_file, 'r') as file:
        obj_data = file.readlines()

    # Count existing vertices to determine indices for the new vertices
    vertex_count = sum(1 for line in obj_data if line.startswith('v '))
    vertex_index1 = vertex_count + 1
    vertex_index2 = vertex_count + 2

    # Add the vertices for the red line
    obj_data.append(f"v {x1:.6f} {y1:.6f} {z1:.6f} 1.0 0.0 0.0\n")  # Red vertex
    obj_data.append(f"v {x2:.6f} {y2:.6f} {z2:.6f} 1.0 0.0 0.0\n")  # Red vertex

    # Add the line segment using proper indices
    obj_data.append(f"l {vertex_index1} {vertex_index2}\n")  # Line connecting the two vertices

    # Write to the output OBJ file
    with open(output_file, 'w') as file:
        file.writelines(obj_data)

    print(f"Red line added to OBJ file. Output saved to: {output_file}")

if __name__ == "__main__":
    # Input from the user
    obj_file = input("Enter the path to the input OBJ file: ").strip()
    focus_x = float(input("Enter the X coordinate of the focus point: ").strip())
    focus_y = float(input("Enter the Y coordinate of the focus point: ").strip())
    focus_z = float(input("Enter the Z coordinate of the focus point: ").strip())
    fb_tilt = float(input("Enter the front/back tilt angle in degrees: ").strip())
    side_tilt = float(input("Enter the side tilt angle in degrees: ").strip())

    # Generate the output file name
    output_file = os.path.splitext(obj_file)[0] + "_with_red_line.obj"

    # Add the red line to the OBJ file
    add_red_line_to_obj(obj_file, output_file, (focus_x, focus_y, focus_z), fb_tilt, side_tilt)
