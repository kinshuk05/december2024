def write_all_to_ply(filename, filtered_pts, principal_pts, ruler_pts, anchor_pt):
    """
    Write all points (filtered mesh vertices, principal axis line points,
    virtual ruler points, and the anchor point) to a single PLY file.
    """
    total_pts = len(filtered_pts) + len(principal_pts) + len(ruler_pts) + 1  # +1 for anchor
    
    with open(filename, 'w') as f:
        # PLY header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {total_pts}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # 1) Filtered vertices (white)
        for pt in filtered_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 255 255 255\n")
        
        # 2) Principal axis (blue)
        for pt in principal_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 0 0 255\n")
        
        # 3) Virtual ruler (red)
        for pt in ruler_pts:
            f.write(f"{pt[0]} {pt[1]} {pt[2]} 255 0 0\n")
        
        # 4) Anchor point (green)
        f.write(f"{anchor_pt[0]} {anchor_pt[1]} {anchor_pt[2]} 0 255 0\n")
