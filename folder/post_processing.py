import numpy as np
import math
from sklearn.decomposition import PCA

# User input
input_file = input("Enter the input OBJ file path: ")
anchor_x, anchor_y, anchor_z = map(float, input("Enter the anchor point coordinates (x y z): ").split())
fb_tilt = float(input("Enter the front-back tilt (negative for back tilt): "))
side_tilt = float(input("Enter the side tilt (negative for left tilt): "))

# Constants
radius = 0.3
y_threshold = 0.2
anchor_point = (anchor_x, anchor_y, anchor_z)

def load_obj_mesh(obj_file):
    """Load vertices from an OBJ file."""
    vertices = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.split()[1:4])))
    return np.array(vertices)

def cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold):
    """Filter vertices inside a cylinder centered at the anchor point."""
    ax, ay, az = anchor_point
    distances = np.sqrt((vertices[:, 0] - ax)**2 + (vertices[:, 2] - az)**2)
    y_diff = np.abs(vertices[:, 1] - ay)
    return vertices[(distances <= radius) & (y_diff <= y_threshold)]

def add_virtual_ruler(anchor_point, fb_tilt, side_tilt, length):
    """Create a virtual ruler that passes through the anchor point based on tilt angles."""
    ax, ay, az = anchor_point
    fb_tilt_rad, side_tilt_rad = map(math.radians, (fb_tilt, side_tilt))
    
    # Calculate half-length displacements
    delta_y_fb = math.sin(fb_tilt_rad) * (length / 2)
    delta_z_fb = math.cos(fb_tilt_rad) * (length / 2)
    delta_x_side = math.sin(side_tilt_rad) * (length / 2)
    delta_y_side = math.cos(side_tilt_rad) * (length / 2)
    
    # Virtual ruler endpoints (centered on the anchor point)
    start_point = (ax - delta_x_side,
                   ay - delta_y_fb - delta_y_side,
                   az - delta_z_fb)
    end_point   = (ax + delta_x_side,
                   ay + delta_y_fb + delta_y_side,
                   az + delta_z_fb)
    return start_point, end_point

def calculate_principal_axis(vertices, anchor_point):
    """
    Calculate the principal axis using PCA and then translate the line so that it passes through the anchor point.
    """
    pca = PCA(n_components=3).fit(vertices)
    direction = pca.components_[0]
    centroid = pca.mean_
    
    projections = vertices @ direction
    min_proj, max_proj = projections.min(), projections.max()
    
    # Compute the original endpoints from PCA
    old_start = centroid + min_proj * direction
    old_end   = centroid + max_proj * direction
    
    # Find the center of the original line and compute the translation offset
    old_center = (old_start + old_end) / 2
    offset = np.array(anchor_point) - old_center
    
    # Translate the endpoints so that the new line passes through the anchor point
    new_start = old_start + offset
    new_end   = old_end + offset
    return new_start, new_end

def calculate_angle(v1_start, v1_end, v2_start, v2_end):
    """Calculate the angle between two lines defined by their endpoints."""
    v1 = np.array(v1_end) - np.array(v1_start)
    v2 = np.array(v2_end) - np.array(v2_start)
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

# Processing
vertices = load_obj_mesh(input_file)
filtered_vertices = cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold)

# Use the y-range of the filtered vertices as the ruler length
ruler_length = filtered_vertices[:, 1].ptp()

# Compute virtual ruler and principal axis
ruler_start, ruler_end = add_virtual_ruler(anchor_point, fb_tilt, side_tilt, ruler_length)
axis_start, axis_end   = calculate_principal_axis(filtered_vertices, anchor_point)
angle = calculate_angle(axis_start, axis_end, ruler_start, ruler_end)
print(f"Angle between principal axis and virtual ruler: {angle:.2f} degrees")

# Generate 1000 points along the principal axis and the virtual ruler using loops.
num_points = 1000
principal_points = []
ruler_points = []

for i in range(num_points):
    t = i / (num_points - 1)  # parameter t in [0,1]
    # Compute point on the principal axis
    pt_axis = [axis_start[j] + t * (axis_end[j] - axis_start[j]) for j in range(3)]
    principal_points.append(pt_axis)
    
    # Compute point on the virtual ruler
    pt_ruler = [ruler_start[j] + t * (ruler_end[j] - ruler_start[j]) for j in range(3)]
    ruler_points.append(pt_ruler)

# Write all points to a single PLY file.
# Colors:
#   - Filtered vertices: white (255, 255, 255)
#   - Principal axis points: blue (0, 0, 255)
#   - Virtual ruler points: red (255, 0, 0)
#   - Anchor point: green (0, 255, 0)
def write_all_to_ply(filename, filtered_pts, principal_pts, ruler_pts, anchor_pt):
    total_pts = len(filtered_pts) + len(principal_pts) + len(ruler_pts) + 1  # +1 for the anchor point
    with open(filename, 'w') as f:
        # Write PLY header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {total_pts}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # Write filtered vertices (white)
        for pt in filtered_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 255 255 255\n")
        
        # Write principal axis points (blue)
        for pt in principal_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 0 0 255\n")
        
        # Write virtual ruler points (red)
        for pt in ruler_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 255 0 0\n")
        
        # Write the anchor point (green)
        f.write(f"{anchor_pt[0]} {anchor_pt[1]} {anchor_pt[2]} 0 255 0\n")

output_filename = "combined_output.ply"
write_all_to_ply(output_filename, filtered_vertices, principal_points, ruler_points, anchor_point)
print(f"Combined PLY file generated: '{output_filename}'.")
