import open3d as o3d

# Load a point cloud from a file (e.g., .ply or .pcd)
# Replace 'point_cloud.ply' with the path to your point cloud file
point_cloud = o3d.io.read_point_cloud("/Users/kinshuksingh/Desktop/cups/cupmesh_1.ply")

# Estimate normals for the point cloud
point_cloud.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
)

# Option 1: Poisson Surface Reconstruction
print("Running Poisson surface reconstruction...")
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    point_cloud, depth=9
)

# Optionally crop the mesh to remove unwanted regions
bbox = point_cloud.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)

# Option 2: Ball-Pivoting Algorithm (BPA)
# radii = [0.005, 0.01, 0.02]  # Adjust based on your data
# print("Running Ball-Pivoting Algorithm...")
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
#     point_cloud, o3d.utility.DoubleVector(radii)
# )

# Save the resulting mesh to a file
output_mesh_file = "/Users/kinshuksingh/Downloads/output_mesh.ply"
o3d.io.write_triangle_mesh(output_mesh_file, mesh)
print(f"Mesh saved to {output_mesh_file}")

# Visualize the point cloud and mesh
print("Visualizing...")
o3d.visualization.draw_geometries([point_cloud], window_name="Point Cloud")
o3d.visualization.draw_geometries([mesh], window_name="Mesh")