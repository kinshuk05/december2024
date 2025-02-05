import numpy as np

# Import from our separate modules
from filtering import load_obj_mesh, cylindrical_mesh_filtering
from ruler import add_virtual_ruler
from principal_axis import calculate_principal_axis
from angle import calculate_angle
from writing import write_all_to_ply

def main():
    # 1) Get user input
    input_file = input("Enter the input OBJ file path: ")
    anchor_x, anchor_y, anchor_z = map(float, input("Enter the anchor point coordinates x y z separated by spaces: ").split())
    fb_tilt = float(input("Enter the front-back tilt (negative for back tilt): "))
    side_tilt = float(input("Enter the side tilt (negative for left tilt): "))

    anchor_point = np.array([anchor_x, anchor_y, anchor_z], dtype=float)

    # Constants for filtering
    radius = 0.3
    y_threshold = 0.2

    # 2) Load and filter the OBJ mesh
    vertices = load_obj_mesh(input_file)
    filtered_vertices = cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold)
    
    # 3) Use the Y-range of the filtered vertices to define the ruler length
    ruler_length = np.ptp(filtered_vertices[:, 1])
    
    # 4) Compute the virtual ruler
    ruler_start, ruler_end = add_virtual_ruler(anchor_point, fb_tilt, side_tilt, ruler_length)
    
    # 5) Compute the principal axis (and shift it to pass through anchor_point)
    axis_start, axis_end = calculate_principal_axis(filtered_vertices, anchor_point)
    
    # 6) Calculate the angle
    angle_val = calculate_angle(axis_start, axis_end, ruler_start, ruler_end)
    print(f"Angle between principal axis and virtual ruler: {angle_val:.2f} degrees")

    # 7) Generate line points
    num_points = 1000
    principal_points = []
    ruler_points = []
    
    for i in range(num_points):
        t = i / (num_points - 1)
        
        # Interpolate along principal axis
        px = axis_start[0] + t * (axis_end[0] - axis_start[0])
        py = axis_start[1] + t * (axis_end[1] - axis_start[1])
        pz = axis_start[2] + t * (axis_end[2] - axis_start[2])
        principal_points.append([px, py, pz])
        
        # Interpolate along virtual ruler
        rx = ruler_start[0] + t * (ruler_end[0] - ruler_start[0])
        ry = ruler_start[1] + t * (ruler_end[1] - ruler_start[1])
        rz = ruler_start[2] + t * (ruler_end[2] - ruler_start[2])
        ruler_points.append([rx, ry, rz])
    
    # 8) Write to a single PLY file
    output_filename = "combined_output.ply"
    write_all_to_ply(output_filename, filtered_vertices, principal_points, ruler_points, anchor_point)
    print(f"Combined PLY file generated: '{output_filename}'.")

if __name__ == "__main__":
    main()
