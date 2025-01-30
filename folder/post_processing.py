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
            if line.startswith('v '):  # Vertex line
                vertices.append(list(map(float, line.split()[1:4])))
    return np.array(vertices)

def cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold):
    """Filter vertices inside a cylinder centered at the anchor point."""
    ax, ay, az = anchor_point
    distances = np.sqrt((vertices[:, 0] - ax) ** 2 + (vertices[:, 2] - az) ** 2)
    y_diff = np.abs(vertices[:, 1] - ay)
    return vertices[(distances <= radius) & (y_diff <= y_threshold)]

def add_virtual_ruler(anchor_point, fb_tilt, side_tilt, length):
    """Create a virtual ruler based on tilt angles."""
    ax, ay, az = anchor_point
    fb_tilt_rad, side_tilt_rad = map(math.radians, (fb_tilt, side_tilt))

    # Calculate displacements due to tilts
    delta_y_fb, delta_z_fb = math.sin(fb_tilt_rad) * (length / 2), math.cos(fb_tilt_rad) * (length / 2)
    delta_x_side, delta_y_side = math.sin(side_tilt_rad) * (length / 2), math.cos(side_tilt_rad) * (length / 2)

    # Define ruler endpoints
    return [(ax - delta_x_side, ay - delta_y_fb - delta_y_side, az - delta_z_fb),
            (ax + delta_x_side, ay + delta_y_fb + delta_y_side, az + delta_z_fb)]

def calculate_principal_axis(vertices):
    """Perform PCA to determine the principal axis."""
    pca = PCA(n_components=3).fit(vertices)
    principal_axis, centroid = pca.components_[0], pca.mean_
    
    projections = vertices @ principal_axis
    min_proj, max_proj = projections.min(), projections.max()

    return centroid + min_proj * principal_axis, centroid + max_proj * principal_axis

def calculate_angle(v1_start, v1_end, v2_start, v2_end):
    """Calculate the angle between two vectors."""
    v1, v2 = np.array(v1_end) - v1_start, np.array(v2_end) - v2_start
    v1, v2 = v1 / np.linalg.norm(v1), v2 / np.linalg.norm(v2)

    return np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

# Processing
vertices = load_obj_mesh(input_file)
filtered_vertices = cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold)
ruler_start, ruler_end = add_virtual_ruler(anchor_point, fb_tilt, side_tilt, filtered_vertices[:, 1].ptp())
axis_start, axis_end = calculate_principal_axis(filtered_vertices)
angle = calculate_angle(axis_start, axis_end, ruler_start, ruler_end)

print(f"Angle between principal axis and virtual ruler: {angle:.2f} degrees")
