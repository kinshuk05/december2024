import numpy as np
from sklearn.decomposition import PCA

def add_principal_axis_to_point_cloud(input_file, output_file):
    # Parse the point cloud from the OBJ file
    points = []
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts and parts[0] == 'v':  # Process only vertex lines
                # Extract only x, y, z (first three numeric values)
                points.append([float(parts[1]), float(parts[2]), float(parts[3])])

    points = np.array(points)  # Convert to NumPy array

    # Perform PCA
    pca = PCA(n_components=3)
    pca.fit(points)
    principal_axis = pca.components_[0]  # Primary principal component
    centroid = pca.mean_  # Mean point of the point cloud

    # Project points onto the principal axis to find its extent
    projections = points @ principal_axis
    min_proj, max_proj = projections.min(), projections.max()

    # Define start and end points of the axis line
    axis_start = centroid + min_proj * principal_axis
    axis_end = centroid + max_proj * principal_axis

    # Write the updated point cloud with the principal axis to the OBJ file
    with open(output_file, 'w') as f:
        # Write original lines (vertices)
        with open(input_file, 'r') as infile:
            for line in infile:
                if line.startswith('v '):  # Only process vertex lines
                    f.write(line)

        # Write the principal axis vertices
        f.write(f"v {axis_start[0]} {axis_start[1]} {axis_start[2]} 1.0 1.0 1.0\n")
        f.write(f"v {axis_end[0]} {axis_end[1]} {axis_end[2]} 1.0 1.0 1.0\n")

        # Write the line connecting the principal axis points
        start_idx = len(points) + 1  # OBJ indices start from 1
        end_idx = start_idx + 1
        f.write(f"l {start_idx} {end_idx}\n")

    print(f"Principal axis added and saved to {output_file}")

# Example usage
input_point_cloud = "/Users/kinshuksingh/Downloads/bottle_final_final.obj"  # Input OBJ file
output_point_cloud = "/Users/kinshuksingh/Downloads/bottle_with_principal_axis.obj"
add_principal_axis_to_point_cloud(input_point_cloud, output_point_cloud)

