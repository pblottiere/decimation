import decimation

dec = decimation.Decimation()
#dec.display_patchids([1, 2])
#dec.display_patchids([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

level = 3
lod = 0
for i in range(0, level):
    lod = lod + pow(i,4)

print("NOF POINTS: ", lod)

dec.display_sorted_patchids([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], lod)
