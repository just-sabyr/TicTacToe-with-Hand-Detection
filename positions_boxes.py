
def positions(box_1_x, box_1_y, box_length): 
    """
    9x2: (b1_x, b1_y), (b2_x, b2_y) ...
    """
    for col in range(3):
        for row in range(3):
            yield(box_1_x + row*box_length, box_1_y + col*box_length)


if __name__ == "__main__":
    box_pos = positions(800, 100, 200)
    for pos in box_pos:
        print(pos)