import open3d as o3d
import numpy as np
import os

def load_obj_vertices(obj_file):
    """ Manually parse the .obj file to extract vertices. """
    vertices = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):  # 'v' lines indicate vertices
                parts = line.split()
                x, y, z = map(float, parts[1:4])
                vertices.append([x, y, z])
    return np.array(vertices)

def generate_sphere_cluster(center, radius, num_points):
    """ Generate a cluster of points randomly distributed inside a sphere. """
    points = []
    for _ in range(num_points):
        # Random spherical coordinates
        u = np.random.uniform(0, 1)
        v = np.random.uniform(0, 1)
        theta = 2 * np.pi * u
        phi = np.arccos(2 * v - 1)
        
        # Convert to cartesian coordinates
        r = np.random.uniform(0, radius)
        x = center[0] + r * np.sin(phi) * np.cos(theta)
        y = center[1] + r * np.sin(phi) * np.sin(theta)
        z = center[2] + r * np.cos(phi)
        
        points.append([x, y, z])
    
    return np.array(points)

def cylindrical_filtering(input_file, radius, anchor_point, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load the vertices manually from the .obj file
    points = load_obj_vertices(input_file)

    # Extract the x, y, z coordinates of the anchor point
    anchor_x, anchor_y, anchor_z = anchor_point

    # Apply cylindrical filter (retain points inside the cylinder)
    filtered_points = []
    for point in points:
        x, y, z = point
        distance = np.sqrt((x - anchor_x) ** 2 + (z - anchor_z) ** 2)
        if distance <= radius:
            filtered_points.append([x, y, z])
    
    # Add the anchor point
    filtered_points.append([anchor_x, anchor_y, anchor_z])

    # Convert the filtered points to a numpy array
    filtered_points = np.array(filtered_points)

    # Generate a cluster of 10,000 red points around the anchor point in a small sphere
    sphere_points = generate_sphere_cluster(anchor_point, 0.01, 10000)

    # Combine the filtered points with the red cluster
    all_points = np.vstack([filtered_points, sphere_points])

    # Create a new point cloud with the combined points
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(all_points)

    # Set the color of the points
    colors = np.ones((all_points.shape[0], 3))  # Default color: white
    
    # Color the red cluster points (last 10,000 points)
    colors[-10000:] = [1, 0, 0]  # Set color to red for the sphere points
    
    # Assign colors to the point cloud
    filtered_pcd.colors = o3d.utility.Vector3dVector(colors)

    # Debug: Print the color of the anchor point
    print(f"Anchor point color: {colors[-10000]}")  # Should print [1.0, 0.0, 0.0] for red

    # Save the filtered point cloud to a PLY file in the output folder
    ply_filename = os.path.join(output_folder, os.path.basename(input_file).replace(".obj", ".ply"))
    o3d.io.write_point_cloud(ply_filename, filtered_pcd)
    
    # Now save the filtered point cloud to a .obj file (without color information)
    obj_filename = os.path.join(output_folder, os.path.basename(input_file).replace(".obj", ".obj"))
    print(f"PLY file saved at: {ply_filename}")
    print(f"Manually convert the .ply file to .obj as Open3D cannot directly export colored point clouds to .obj format.")

# Get inputs from the user
input_file = input("Enter the input OBJ file path: ")
radius = float(input("Enter the radius of the cylinder: "))
anchor_x = float(input("Enter the X coordinate of the anchor point: "))
anchor_y = float(input("Enter the Y coordinate of the anchor point: "))
anchor_z = float(input("Enter the Z coordinate of the anchor point: "))
anchor_point = (anchor_x, anchor_y, anchor_z)
output_folder = input("Enter the output folder path: ")

# Run the filtering function
cylindrical_filtering(input_file, radius, anchor_point, output_folder)
