import math

def add_virtual_ruler(anchor_point, fb_tilt, side_tilt, length):
    """
    Create a virtual ruler that passes through the anchor point,
    oriented by front-back tilt (fb_tilt) and side tilt (side_tilt).
    'length' is the total length of the ruler.
    """
    ax, ay, az = anchor_point
    fb_tilt_rad = math.radians(fb_tilt)
    side_tilt_rad = math.radians(side_tilt)
    
    # Calculate half-length displacements
    delta_y_fb = math.sin(fb_tilt_rad) * (length / 2)
    delta_z_fb = math.cos(fb_tilt_rad) * (length / 2)
    delta_x_side = math.sin(side_tilt_rad) * (length / 2)
    delta_y_side = math.cos(side_tilt_rad) * (length / 2)
    
    # The ruler is centered on the anchor point
    start_point = (
        ax - delta_x_side,
        ay - delta_y_fb - delta_y_side,
        az - delta_z_fb
    )
    end_point = (
        ax + delta_x_side,
        ay + delta_y_fb + delta_y_side,
        az + delta_z_fb
    )
    return start_point, end_point
