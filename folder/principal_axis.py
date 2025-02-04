import numpy as np
from sklearn.decomposition import PCA

def calculate_principal_axis(vertices, anchor_point):
    """
    Perform PCA on the given vertices to find the primary direction (first component).
    Then shift that axis so it passes through the given anchor point.
    """
    pca = PCA(n_components=3).fit(vertices)
    direction = pca.components_[0]   # The principal direction
    centroid = pca.mean_
    
    # Find the extent (min_proj, max_proj) of the vertices along 'direction'
    projections = vertices @ direction
    min_proj, max_proj = projections.min(), projections.max()
    
    # Original endpoints of the PCA axis
    old_start = centroid + min_proj * direction
    old_end   = centroid + max_proj * direction
    
    # Shift the axis so its midpoint is at anchor_point
    old_center = (old_start + old_end) / 2.0
    offset = anchor_point - old_center  # vector from old center to anchor
    
    new_start = old_start + offset
    new_end   = old_end + offset
    
    return new_start, new_end
