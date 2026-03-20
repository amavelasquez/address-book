def validate_x_coord(x: float):
    if x >= -180 and x <= 180:
        return True
    return False

def validate_y_coord(y: float):
    if y >= -90 and y <= 90:
        return True
    return False