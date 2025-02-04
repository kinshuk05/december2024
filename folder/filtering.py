import numpy as np

def load_obj_mesh(obj_file):
    """
    Load vertices from an OBJ file.
    Returns a NumPy array of shape (N, 3).
    """
    vertices = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v '):
                # Extract the x, y, z components from each "v" line
                vertices.append(list(map(float, line.split()[1:4])))
    return np.array(vertices)

def cylindrical_mesh_filtering(vertices, radius, anchor_point, y_threshold):
    """
    Filter vertices inside a cylinder centered at the anchor point.
    'radius' is the radius in the XZ plane,
    'y_threshold' is the vertical limit above/below the anchor in the Y axis.
    """
    ax, ay, az = anchor_point
    distances = np.sqrt((vertices[:, 0] - ax) ** 2 + (vertices[:, 2] - az) ** 2)
    y_diff = np.abs(vertices[:, 1] - ay)
    # Keep only points where distance <= radius and |y - anchor_y| <= y_threshold
    return vertices[(distances <= radius) & (y_diff <= y_threshold)]
