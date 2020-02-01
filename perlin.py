import noise
import numpy as np

def gen_perlin(shape, scale, octaves, persistence, lacunarity):
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i / scale,
                                        j / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=shape[0],
                                        repeaty=shape[1],
                                        base=0)

    out = {}
    rows = 0
    for i in world:
        cols = 0
        for ii in i:
            out.setdefault((rows, cols),int(bool(round(ii*10))))
            cols += 1
        rows += 1
    return out