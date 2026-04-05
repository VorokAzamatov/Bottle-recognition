def angle_2_steps(angle, steps_per_rev):
    return int( round( angle * steps_per_rev / 360 ) )


def x_2_angle(x, frames_width):
    return (x / frames_width) * 360


def compute_delta_angle(current_angle, target_angle):
    delta = target_angle - current_angle

    if delta > 180:
        delta -= 360
    elif delta < -180:  
        delta += 360

    return delta