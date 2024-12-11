import os
import re

directory = '/Users/kinshuksingh/Desktop/models2/'
files = os.listdir(directory)
index = 0
while index < len(files):
    filename = files[index]
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename)) as f:
            def parse_data(file_path):
                """
                Parses vertices and triangle data from the provided input file.
                Handles both indices and explicit vertex definitions (after 'Vertices:').
                """
                vertices = []
                triangles = []
                parsing_triangles = False  # Switch to parse triangles after encountering the marker
                temp_vertices_for_triangles = []  # Temporarily store vertices associated with the triangles

                with open(file_path, 'r') as file:
                    for line in file:
                        # Switch parsing logic upon encountering the triangle marker
                        if "Triangle (with corresponding vertices):" in line:
                            parsing_triangles = True
                            continue

                        if not parsing_triangles:
                            # Parse general vertices
                            coords = re.findall(r"-?\d+\.?\d*(?:e[-+]?\d+)?", line)
                            if len(coords) == 3:
                                vertices.append([float(coords[0]), float(coords[1]), float(coords[2])])

                        else:
                            # Parse triangle index definitions
                            if line.startswith("Triangle:"):
                                # Extract triangle indices
                                match = re.search(r"\((\d+), (\d+), (\d+)\)", line)
                                if match:
                                    triangle_indices = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
                                    temp_vertices_for_triangles.clear()
                                    triangles.append({"indices": triangle_indices, "vertices": []})
                            elif line.startswith("Vertices:"):
                                # Parse vertices that follow this triangle definition
                                coords = re.findall(r"-?\d+\.?\d*(?:e[-+]?\d+)?", line[len("Vertices:"):])
                                if len(coords) == 3:
                                    temp_vertices_for_triangles.append([float(coords[0]), float(coords[1]), float(coords[2])])
                                    if len(temp_vertices_for_triangles) == 3:
                                        # Map the vertices to the triangle once 3 vertex coordinates are encountered
                                        triangles[-1]["vertices"] = temp_vertices_for_triangles.copy()

                # Map all explicit triangle vertices to indices
                vertex_map = {}
                unique_vertices = []
                for v in vertices:
                    if tuple(v) not in vertex_map:
                        vertex_map[tuple(v)] = len(unique_vertices)
                        unique_vertices.append(v)

                # Map the explicit triangle vertices (provided by `Vertices:`) to indices in the final vertices list
                mapped_triangles = []
                for tri in triangles:
                    indices = [
                        vertex_map[tuple(tri["vertices"][0])],
                        vertex_map[tuple(tri["vertices"][1])],
                        vertex_map[tuple(tri["vertices"][2])]
                    ]
                    mapped_triangles.append(indices)

                return unique_vertices, mapped_triangles


            def write_ply(output_path, vertices, triangles):
                """
                Writes the vertices and triangles data into a PLY file.
                """
                with open(output_path, 'w') as ply_file:
                    # Write PLY header
                    ply_file.write("ply\n")
                    ply_file.write("format ascii 1.0\n")
                    ply_file.write(f"element vertex {len(vertices)}\n")
                    ply_file.write("property float x\n")
                    ply_file.write("property float y\n")
                    ply_file.write("property float z\n")
                    ply_file.write(f"element face {len(triangles)}\n")
                    ply_file.write("property list uchar int vertex_indices\n")
                    ply_file.write("end_header\n")
                    
                    # Write vertex coordinates
                    for v in vertices:
                        ply_file.write(f"{v[0]} {v[1]} {v[2]}\n")
                    
                    # Write triangle indices
                    for tri in triangles:
                        ply_file.write(f"3 {tri[0]} {tri[1]} {tri[2]}\n")


            input_file = f"/Users/kinshuksingh/Desktop/split_textfiles/entry_{index+1}.txt"  # Input text file
            output_ply = f"/Users/kinshuksingh/Desktop/modelsply2/entry_{index+1}.ply"  # Path to save the PLY file

            vertices, triangles = parse_data(input_file)
            write_ply(output_ply, vertices, triangles)

            print(f"PLY file successfully created at: {output_ply}")

    index += 1