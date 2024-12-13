import os

def split_multiple_entries(input_file, output_dir):
    """
    Splits a single input file containing multiple 'Vertices' and 'Triangles' sections
    into separate files for each entry.

    Parameters:
    - input_file (str): The path to the input file.
    - output_dir (str): The directory where output files will be saved.
    """
    # Read the input file
    with open(input_file, 'r') as infile:
        data = infile.read()

    # Split the file into parts using "Vertices:" as the marker
    parts = data.split("Vertices:\n")
    
    # Validate the number of entries
    if len(parts) <= 1:
        raise ValueError("No 'Vertices:' sections found in the file.")

    # Remove the first empty part before the first "Vertices:"
    parts = parts[1:] 

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save each entry to a separate file
    for i, part in enumerate(parts, start=1):
        output_file = os.path.join(output_dir, f"entry_{i}.txt")
        with open(output_file, 'w') as outfile:
            outfile.write("Vertices:" + part)

    print(f"Successfully split into {len(parts)} files in the directory: {output_dir}")

# Example usage
input_file = "/Users/kinshuksingh/Downloads/cupmesh_1.txt"       # Replace with the path to your input file
output_dir = "/Users/kinshuksingh/Desktop/"      # Directory to save the split files
split_multiple_entries(input_file, output_dir)
