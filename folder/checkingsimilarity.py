import numpy as np

def load_points_from_file(filename):
    """
    Load points from a text file. Assumes each line in the file contains
    a point in the format: Vertices:x,y,z or x,y,z

    Parameters:
        filename (str): Path to the text file.

    Returns:
        ndarray: Array of points (Nx3).
    """
    points = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Vertices:"):
                line = line[len("Vertices:"):]
            parts = line.split(',')
            if len(parts) == 3:
                points.append([float(coord) for coord in parts])
    return np.array(points)

def percentage_common_points(cloud1, cloud2, radius):
    """
    Calculate the percentage of common points between two point clouds.

    Parameters:
        cloud1 (ndarray): First point cloud (Nx3 array of points).
        cloud2 (ndarray): Second point cloud (Mx3 array of points).
        radius (float): Radius to consider points as "common".

    Returns:
        float: Percentage of common points relative to the total number of points.
    """
    cloud1 = np.asarray(cloud1)
    cloud2 = np.asarray(cloud2)

    # Create a kd-tree for efficient spatial searches
    from scipy.spatial import cKDTree
    
    tree1 = cKDTree(cloud1)
    tree2 = cKDTree(cloud2)

    total_points = len(cloud2)
    progress_intervals = total_points // 10
    completed_intervals = 0

    # Find points in cloud2 that are close to cloud1's points within the radius
    matched_points_2 = set()
    for i, point in enumerate(cloud2):
        if i % progress_intervals == 0 and completed_intervals < 10:
            completed_intervals += 1
            print(f"Completed {completed_intervals * 10}% of the points.")
        neighbors = tree1.query_ball_point(point, radius)
        matched_points_2.update(neighbors)

    # Find points in cloud1 that are close to cloud2's points within the radius
    matched_points_1 = set()
    for i, point in enumerate(cloud1):
        if i % progress_intervals == 0 and completed_intervals < 10:
            completed_intervals += 1
            print(f"Completed {completed_intervals * 10}% of the points.")
        neighbors = tree2.query_ball_point(point, radius)
        matched_points_1.update(neighbors)

    # Total unique common points
    total_common_points = len(matched_points_1 | matched_points_2)

    # Total points in both clouds
    total_points = len(cloud1)+len(cloud2)

    # Calculate percentage of common points
    percentage = (total_common_points / total_points) * 100

    return percentage

# Example usage
if __name__ == "__main__":
    # Load point clouds from text files
    file1 = "/Users/kinshuksingh/Downloads/cup_1.txt"
    file2 = "/Users/kinshuksingh/Downloads/cup_2.txt"

    cloud1 = load_points_from_file(file1)
    cloud2 = load_points_from_file(file2)

    radius = 0.03  # Define a small radius
    percentage = percentage_common_points(cloud1, cloud2, radius)
    print(f"Percentage of common points: {percentage:.2f}%")
