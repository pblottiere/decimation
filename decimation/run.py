import decimation

dec = decimation.Decimation()
#dec.display_patchids([1, 2])
#dec.display_patchids([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def lod(level):
    lod = 0
    for i in range(0, level):
        lod = lod + pow(4,i)
    return lod

print("NOF POINTS: ", lod)

#dec.display_sorted_patchids([1, 2, 3, 4, 5], lod)
l = lod(1)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 1, l, show=False)

l = lod(2)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 2, l, show=False)

l = lod(3)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 3, l, show=False)

l = lod(4)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 4, l, show=False)

l = lod(5)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 5, l, show=False)

l = lod(6)
dec.display_patchids([1, 2, 3, 4], "lod_%d.png" % 6, l, show=False)
