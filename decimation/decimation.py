import session
from math import sqrt, pow
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Decimation(object):

    def __init__(self):
        self.db = session.Session()

    def display_patchids(self, ids):
        # init img
        fig,ax = plt.subplots(1)

        # get data
        xs = []
        ys = []

        minx = 9999999999999
        miny = 9999999999999
        for id in ids:
            mx = self.db.get_patch_min(id)['x']
            my = self.db.get_patch_min(id)['y']
            if mx < minx:
                minx = mx
            if my < miny:
                miny = my

        for id in ids:
            pa = self.db.get_patch(id)

            # build points
            mi = 0
            ma = 0
            for pt in pa:
                mi = self.db.get_patch_min(id)
                ma = self.db.get_patch_max(id)

                xs.append(pt['x'] - minx)
                ys.append(pt['y'] - miny)

            # build rectangle
            r = patches.Rectangle((mi['x'] - minx, mi['y']-miny),
                    ma['x'] - mi['x'], ma['y'] - mi['y'],
                    ec='r', lw=2, fc='none', fill='true')
            ax.add_patch(r)

        plt.scatter(xs,ys)

        # draw
        plt.title('PC Patch')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('ScatterPlot.png')
        plt.show()

    def display_sorted_patchids(self, ids, n=None):

        # init img
        fig,ax = plt.subplots(1)

        # get data
        xs = []
        ys = []

        minx = 9999999999999
        miny = 9999999999999
        for id in ids:
            mx = self.db.get_patch_min(id)['x']
            my = self.db.get_patch_min(id)['y']
            if mx < minx:
                minx = mx
            if my < miny:
                miny = my

        for id in ids:
            pa = self._sorted_midoc(id)

            # build points
            mi = self.db.get_patch_min(id)
            ma = self.db.get_patch_max(id)

            if n == None:
                for pt in pa:
                    xs.append(pt['x'] - minx)
                    ys.append(pt['y'] - miny)
            else:
                sub = pa[0:n]
                for pt in sub:
                    xs.append(pt['x'] - minx)
                    ys.append(pt['y'] - miny)

            # build rectangle
            r = patches.Rectangle((mi['x'] - minx, mi['y']-miny),
                    ma['x'] - mi['x'], ma['y'] - mi['y'],
                    ec='r', lw=2, fc='none', fill='true')
            ax.add_patch(r)

            # display center
            center = self._center(pa)
            c = plt.Circle((center[0] - minx, center[1]-miny), 0.1, color='g')
            ax.add_artist(c)

        plt.scatter(xs,ys)

        # draw
        plt.title('PC Patch')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('ScatterPlot.png')
        plt.show()

    def _sorted_midoc(self, id):

        pa = self.db.get_patch(id)
        sorted_pa = []
        pts_candidates = pa

        mi = self.db.get_patch_min(id)
        ma = self.db.get_patch_max(id)

        # bb = [xmin ymin, xmax, ymax]
        fullbb = [mi['x'], mi['y']]
        fullbb.append(ma['x'])
        fullbb.append(ma['y'])

        iter = 0
        while len(pts_candidates) > 0:
            # bbs : list of points candidates
            bbs = self._cut_boundingbox(fullbb, pts_candidates, pow(4, iter))
            iter = iter + 1

            for bb in bbs:
                mindist = 9999999999
                center = self._center(bb)

                i = 0
                idx = -1
                for pt in bb:
                    t1 = pow(center[0] - pt['x'], 2)
                    t2 = pow(center[1] - pt['y'], 2)
                    dist = sqrt(t1 + t2)

                    if dist < mindist:
                        mindist = dist
                        idx = i

                    i = i+1

                if idx >= 0:
                    try:
                        sorted_pa.append(bb[idx])
                        pts_candidates.remove(bb[idx])
                    except:
                        pass

        return sorted_pa

    def _max(self, pts):
        maxx = 0
        maxy = 0
        for pt in pts:
            x = pt['x']
            y = pt['y']
            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
        return [maxx, maxy]

    def _min(self, pts):
        minx = 9999999999
        miny = 9999999999
        for pt in pts:
            x = pt['x']
            y = pt['y']
            if x < minx:
                minx = x
            if y < miny:
                miny = y
        return [minx, miny]

    def _center(self, pts):
        ma = self._max(pts)
        mi = self._min(pts)
        centerx = (ma[0] - mi[0]) / 2 + mi[0]
        centery = (ma[1] - mi[1]) / 2 + mi[1]
        return [centerx, centery]

    def _cut_boundingbox(self, fullbb, pts, nbb):

        #
        ma = self._max(pts)
        mi = self._min(pts)

        width = fullbb[2] - fullbb[0]
        height = fullbb[3] - fullbb[1]

        stepx = float(width) / sqrt(nbb)
        stepy = float(height) / sqrt(nbb)

        # search limits
        bbs = []
        for i in range(0, int(sqrt(nbb))):
            for j in range(0, int(sqrt(nbb))):
                xbeg = float(mi[0]) + i*stepx - 0.01
                ybeg = float(mi[1]) + j*stepy - 0.01

                xend = float(mi[0]) + (i+1)*stepx + 0.01
                yend = float(mi[1]) + (j+1)*stepy + 0.01

                bb = []
                for pt in pts:
                    if pt['x'] >= xbeg and pt['x'] <= xend \
                        and pt['y'] >= ybeg and pt['y'] <= yend:
                        bb.append(pt)
                bbs.append(bb)

        return bbs
