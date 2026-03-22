def strip_frame(frame, strip_width):
    width = frame.shape[1]

    center_x = width // 2
    start_x = center_x - strip_width // 2
    end_x = center_x + strip_width // 2

    stripped_frame = frame[:, start_x:end_x]

    return stripped_frame
