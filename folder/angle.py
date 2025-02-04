import numpy as np

def calculate_angle(v1_start, v1_end, v2_start, v2_end):
    """
    Calculate the angle between two lines (v1 and v2),
    each defined by start and end points.
    """
    v1 = np.array(v1_end) - np.array(v1_start)
    v2 = np.array(v2_end) - np.array(v2_start)
    
    # Normalize
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Dot product -> angle
    dot_val = np.dot(v1, v2)
    # Clip to avoid numerical issues
    dot_val = np.clip(dot_val, -1.0, 1.0)
    
    angle_degrees = np.degrees(np.arccos(dot_val))
    return angle_degrees
