from constants import RADIUS, SQRT3

def get_surface_pos(pos):
    """
    Returns a subsurface corresponding to the surface, hopefully with trim_cell wrapped around the blit method.
    """
    row = pos[0]
    col = pos[1]
    width = 2 * RADIUS
    height = RADIUS * SQRT3

    # midy = (row - math.ceil(col / 2.0)) * height + (height / 2 if col % 2 == 1 else 0) + height/2
    # Alternate the offset of the cells based on column
    offset = RADIUS * SQRT3 / 2 if col % 2 else 0
    # Calculate the offset of the cell
    midy = offset + SQRT3 * row * RADIUS + height/2
    midx = 1.5 * RADIUS * col + width/2

    return (midx, midy)