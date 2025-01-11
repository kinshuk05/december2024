import numpy as np
import os
import math
from sklearn.decomposition import PCA

def load_obj_mesh(obj_file):
    """ Parse the .obj file to extract vertices, normals, and faces. """
    vertices = []
    normals = []
    faces = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Vertex
                parts = line.split()
                vertices.append([float(p) for p in parts[1:4]])
            elif line.startswith('vn '):  # Normal
                parts = line.split()
                normals.append([float(p) for p in parts[1:4]])
            elif line.startswith('f '):  # Face
                parts = line.split()[1:]
                face = [int(p.split('/')[0]) - 1 for p in parts]
                faces.append(face)
    return np.array(vertices), np.array(normals), np.array(faces)

def cylindrical_mesh_filtering(input_file, radius, anchor_point, y_threshold):
    """ Filter the mesh to retain vertices inside a cylinder. """
    vertices, normals, faces = load_obj_mesh(input_file)
    anchor_x, anchor_y, anchor_z = anchor_point

    # Apply filtering
    distances = np.sqrt((vertices[:, 0] - anchor_x) ** 2 + (vertices[:, 2] - anchor_z) ** 2)
    y_diff = np.abs(vertices[:, 1] - anchor_y)
    mask = (distances <= radius) & (y_diff <= y_threshold)

    # Map old vertex indices to new indices
    index_map = {i: new_i for new_i, i in enumerate(np.where(mask)[0])}

    # Filter vertices and normals
    filtered_vertices = vertices[mask]
    filtered_normals = normals[mask] if normals.size > 0 else []

    # Filter faces
    filtered_faces = [[index_map[v] for v in face if v in index_map] for face in faces]
    filtered_faces = [face for face in filtered_faces if len(face) == len(faces[0])]

    return filtered_vertices, filtered_normals, filtered_faces

def save_obj(file_path, vertices, normals, faces):
    """ Save the mesh to an OBJ file. """
    with open(file_path, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        if len(normals) > 0:
            for n in normals:
                f.write(f"vn {n[0]} {n[1]} {n[2]}\n")
        for face in faces:
            face_str = " ".join(str(v + 1) for v in face)
            f.write(f"f {face_str}\n")

def add_virtual_ruler(vertices, anchor_point, fb_tilt, side_tilt, num_points=5):
    """ Add a virtual ruler to the vertices. """
    x, y, z = anchor_point
    fb_tilt_rad = math.radians(fb_tilt)
    side_tilt_rad = math.radians(side_tilt)

    y_range = vertices[:, 1].max() - vertices[:, 1].min()
    line_length = y_range

    # Calculate ruler endpoints
    delta_y_fb = math.sin(fb_tilt_rad) * (line_length / 2)
    delta_z_fb = math.cos(fb_tilt_rad) * (line_length / 2)
    delta_x_side = math.sin(side_tilt_rad) * (line_length / 2)
    delta_y_side = math.cos(side_tilt_rad) * (line_length / 2)

    x1, y1, z1 = x - delta_x_side, y - delta_y_fb - delta_y_side, z - delta_z_fb
    x2, y2, z2 = x + delta_x_side, y + delta_y_fb + delta_y_side, z + delta_z_fb

    # Generate intermediate points
    ruler_points = [
        [x1 + t * (x2 - x1), y1 + t * (y2 - y1), z1 + t * (z2 - z1)]
        for t in np.linspace(0, 1, num_points + 2)
    ]
    return vertices.tolist() + ruler_points, (x1, y1, z1), (x2, y2, z2)

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

def main():
    # Get user inputs
    input_file = input("Enter the input OBJ file path: ")
    anchor_x = float(input("Enter the X coordinate of the anchor point: "))
    anchor_y = float(input("Enter the Y coordinate of the anchor point: "))
    anchor_z = float(input("Enter the Z coordinate of the anchor point: "))
    output_folder = input("Enter the output folder path: ")
    fb_tilt = float(input("Enter the front-back tilt (negative for back tilt): "))
    side_tilt = float(input("Enter the side tilt (negative for left tilt): "))

    radius = 0.3
    y_threshold = 0.2
    anchor_point = (anchor_x, anchor_y, anchor_z)

    # Filter the mesh
    filtered_vertices, filtered_normals, filtered_faces = cylindrical_mesh_filtering(
        input_file, radius, anchor_point, y_threshold
    )

    # Add a virtual ruler
    all_vertices, ruler_start, ruler_end = add_virtual_ruler(filtered_vertices, anchor_point, fb_tilt, side_tilt)

    # Determine the principal axis
    axis_start, axis_end = calculate_principal_axis(np.array(all_vertices))

    # Calculate the angle between the principal axis and the virtual ruler
    angle = calculate_angle(axis_start, axis_end, ruler_start, ruler_end)

    # Save the final OBJ file
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(input_file).replace(".obj", "_processed.obj"))
    save_obj(output_file, np.array(all_vertices), filtered_normals, filtered_faces)

    print(f"Processed OBJ saved to: {output_file}")
    print(f"Angle between principal axis and virtual ruler: {angle:.2f} degrees")

if __name__ == "__main__":
    main()
