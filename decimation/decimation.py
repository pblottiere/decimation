import session
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

    def display_sorted_patchids(self, ids):

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

            pa = self._sort_midoc(pa)

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

    def _sort_midoc(self, pa):

        sorted_pa = pa

        return sorted_pa
