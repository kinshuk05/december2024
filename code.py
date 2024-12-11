input_file = "/Users/kinshuksingh/Downloads/cup_2.txt" #enter path of file
output_file = "/Users/kinshuksingh/Desktop/cup2.ply"

# Read points from the input file
with open(input_file, "r") as f:
    points = f.readlines()

# Validate and reformat points
valid_points = []
for line in points:
    values = line.strip().split(",")  # Split by commas
    if len(values) == 3:             # Ensure exactly 3 values (x, y, z)
        try:
            x, y, z = map(float, values)  # Convert to floats to verify validity
            valid_points.append(f"{x} {y} {z}\n")  # Reformat as `x y z`
        except ValueError:
            continue  # Skip lines with invalid data

num_points = len(valid_points)

# Write header and data to the output file
header = f"""ply
format ascii 1.0
element vertex {num_points}
property float x
property float y
property float z
end_header
"""

with open(output_file, "w") as f:
    f.write(header)
    f.writelines(valid_points[:num_points])  
