'''This script ganarates simple map. Map file takes format 19 x 13 of matrix,
rows of numbers separated with space indicating what tile is it
Current tiles:
0 - empty tile
(tiles 1-20 are solid tiles, they collide with other objects)
1 - basic floor tile
(> 20 transparent tiles)
'''
import numpy as np

width = 19
height = 13

basic_map = []
for i in range(height - 1):
    basic_map.append([0] * width)
    # self.floor.append((tile, (64 * i, 768)))
basic_map.append([1] * width)

a = np.array(basic_map)
mat = np.matrix(a)
with open('outfile.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%d')
