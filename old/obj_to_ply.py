import trimesh

def convert_obj_to_ply(obj_file_path, ply_file_path):
    """
    Converts a .obj file to a .ply file.

    Parameters:
        obj_file_path (str): Path to the input .obj file.
        ply_file_path (str): Path to the output .ply file.
    """
    try:
        # Load the .obj file
        mesh = trimesh.load(obj_file_path)
        
        # Export as .ply
        mesh.export(ply_file_path)
        print(f"Conversion successful! Saved as {ply_file_path}")
   

# Example usage
obj_file = "example.obj"  # Replace with your .obj file path
ply_file = "example.ply"  # Replace with your desired .ply file path
convert_obj_to_ply(obj_file, ply_file)
