import numpy as np
import math
from sklearn.decomposition import PCA
import os
import re 

input_file = input("Enter the input OBJ file path: ")
anchor_x = float(input("Enter the X coordinate of the anchor point: "))
anchor_y = float(input("Enter the Y coordinate of the anchor point: "))
anchor_z = float(input("Enter the Z coordinate of the anchor point: "))
fb_tilt = float(input("Enter the front-back tilt (negative for back tilt): "))
side_tilt = float(input("Enter the side tilt (negative for left tilt): "))

radius = 0.3
y_threshold = 0.2
anchor_point = (anchor_x, anchor_y, anchor_z)

def load_obj_mesh(obj_file):
    """ Parse the .obj file to extract vertices. """
    vertices = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Vertex
                parts = line.split()
                vertices.append([float(p) for p in parts[1:4]])
    return np.array(vertices)

def cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold):
    """ Filter the mesh to retain vertices inside a cylinder. """
    anchor_x, anchor_y, anchor_z = anchor_point

    # Apply filtering
    distances = np.sqrt((vertices[:, 0] - anchor_x) * 2 + (vertices[:, 2] - anchor_z) * 2)
    y_diff = np.abs(vertices[:, 1] - anchor_y)
    mask = (distances <= radius) & (y_diff <= y_threshold)

    return vertices[mask]

def add_virtual_ruler(vertices, anchor_point, fb_tilt, side_tilt):
    """ Add a virtual ruler to the vertices. """
    x, y, z = anchor_point
    fb_tilt_rad = math.radians(fb_tilt)
    side_tilt_rad = math.radians(side_tilt)

    y_range = vertices[:, 1].max() - vertices[:, 1].min()
    line_length = y_range

    # Front-back tilt: Tilt in the XY plane (around the X-axis)
    delta_y_fb = math.sin(fb_tilt_rad) * (line_length / 2)
    delta_z_fb = math.cos(fb_tilt_rad) * (line_length / 2)

    # Side tilt: Tilt in the YZ plane (around the Z-axis)
    delta_x_side = math.sin(side_tilt_rad) * (line_length / 2)
    delta_y_side = math.cos(side_tilt_rad) * (line_length / 2)

    # Calculate the start and end points of the ruler
    x1, y1, z1 = x - delta_x_side, y - delta_y_fb - delta_y_side, z - delta_z_fb
    x2, y2, z2 = x + delta_x_side, y + delta_y_fb + delta_y_side, z + delta_z_fb

    return (x1, y1, z1), (x2, y2, z2)

def calculate_principal_axis(vertices):
    """ Perform PCA to determine the principal axis. """
    pca = PCA(n_components=3)
    pca.fit(vertices)
    principal_axis = pca.components_[0]
    centroid = pca.mean_

    projections = vertices @ principal_axis
    min_proj, max_proj = projections.min(), projections.max()

    axis_start = centroid + min_proj * principal_axis
    axis_end = centroid + max_proj * principal_axis

    return axis_start, axis_end

def calculate_angle(axis_start, axis_end, ruler_start, ruler_end):
    """ Calculate the angle between the principal axis and the virtual ruler. """
    vector1 = np.array(axis_end) - np.array(axis_start)
    vector2 = np.array(ruler_end) - np.array(ruler_start)

    vector1 /= np.linalg.norm(vector1)
    vector2 /= np.linalg.norm(vector2)

    dot_product = np.dot(vector1, vector2)
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))
    return np.degrees(angle_rad)

# Load mesh and filter
vertices = load_obj_mesh(input_file)
filtered_vertices = cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold)

# Add a virtual ruler
ruler_start, ruler_end = add_virtual_ruler(filtered_vertices, anchor_point, fb_tilt, side_tilt)

# Determine the principal axis
axis_start, axis_end = calculate_principal_axis(filtered_vertices)

# Calculate the angle between the principal axis and the virtual ruler
angle = calculate_angle(axis_start, axis_end, ruler_start, ruler_end)

print(f"Angle between principal axis and virtual ruler: {angle:.2f} degrees")
