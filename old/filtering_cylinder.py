import numpy as np
import os

def load_obj_mesh(obj_file):
    """ Parse the .obj file to extract vertices, normals, and faces. """
    vertices = []
    normals = []
    faces = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Vertex
                parts = line.split()
                x, y, z = map(float, parts[1:4])
                vertices.append([x, y, z])
            elif line.startswith('vn '):  # Normal
                parts = line.split()
                nx, ny, nz = map(float, parts[1:4])
                normals.append([nx, ny, nz])
            elif line.startswith('f '):  # Face
                parts = line.split()[1:]
                # Convert face indices to zero-based indexing
                face = [int(p.split('/')[0]) - 1 for p in parts]
                faces.append(face)
    return np.array(vertices), np.array(normals), np.array(faces)

def cylindrical_mesh_filtering(input_file, radius, anchor_point, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load the mesh (vertices, normals, faces)
    vertices, normals, faces = load_obj_mesh(input_file)

    # Extract the x, y, z coordinates of the anchor point
    anchor_x, anchor_y, anchor_z = anchor_point

    # Apply cylindrical filter (retain points inside the cylinder)
    vertex_mask = []
    for vertex in vertices:
        x, y, z = vertex
        distance = np.sqrt((x - anchor_x) ** 2 + (z - anchor_z) ** 2)
        vertex_mask.append(distance <= radius)
    vertex_mask = np.array(vertex_mask)

    # Create a mapping from old vertex indices to new indices
    index_map = {i: new_i for new_i, i in enumerate(np.where(vertex_mask)[0])}

    # Filter vertices and normals
    filtered_vertices = vertices[vertex_mask]
    filtered_normals = normals[vertex_mask] if len(normals) > 0 else []

    # Filter faces: Include only faces where all vertices are in the cylinder
    filtered_faces = []
    for face in faces:
        if all(v in index_map for v in face):
            filtered_faces.append([index_map[v] for v in face])

    # Save the filtered mesh to a new OBJ file
    output_obj_file = os.path.join(output_folder, os.path.basename(input_file).replace(".obj", "_filtered.obj"))
    with open(output_obj_file, 'w') as f:
        # Write vertices
        for v in filtered_vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        
        # Write normals (if available)
        if len(filtered_normals) > 0:
            for n in filtered_normals:
                f.write(f"vn {n[0]} {n[1]} {n[2]}\n")
        
        # Write faces
        for face in filtered_faces:
            face_str = " ".join(str(v + 1) for v in face)  # Convert back to one-based indexing
            f.write(f"f {face_str}\n")

    print(f"Filtered mesh saved at: {output_obj_file}")

# Get inputs from the user
input_file = input("Enter the input OBJ file path: ")
radius = float(input("Enter the radius of the cylinder: "))
anchor_x = float(input("Enter the X coordinate of the anchor point: "))
anchor_y = float(input("Enter the Y coordinate of the anchor point: "))
anchor_z = float(input("Enter the Z coordinate of the anchor point: "))
anchor_point = (anchor_x, anchor_y, anchor_z)
output_folder = input("Enter the output folder path: ")

# Run the filtering function
cylindrical_mesh_filtering(input_file, radius, anchor_point, output_folder)
