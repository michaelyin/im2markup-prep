import numpy as np
from scipy.spatial import distance
from skimage.draw._draw import line


class Stroke(object):
    def __init__(self, id, coords, ref=None, truth="", norm_w=None, norm_h=None):
        """
        id, stroke/trace id in Inkml file
        coords, coordinates of trace points
        ref, reference of the symbol the trace belongs to
        norm_w, normalized width
        norm_h, normalized height
        """
        self.id = id
        self.coords = coords
        self.ref = ref
        self.truth = truth
        self.norm_w = norm_w
        self.norm_h = norm_h
        self.normed_connected_coords = None  # self.connect_points()
        self.bounding_box = None
        self.coords_h10000 = None  # refer to seshat sample.cc: Renormalize to height [0,10000] keeping the aspect ratio

    def calc_coords_h10000(self, H, W, x_min, y_min, x_max, y_max):
        '''
        called during the inkml file loading process
        Parameters
        ----------
        H
        W
        x_min
        y_min
        x_max
        y_max

        Returns
        -------

        '''
        coords_tmp = np.array(self.coords)
        coords_tmp[0, :] = (coords_tmp[0, :] - x_min) * W/(x_max - x_min)
        coords_tmp[1, :] = (coords_tmp[1, :] - y_min) * H/(y_max - y_min)
        self.coords_h10000 = coords_tmp.astype(int)

    def get_bounding_box_h10000(self):
            bbx = np.min(self.coords_h10000[0, :]), np.min(self.coords_h10000[1, :]), np.max(self.coords_h10000[0, :]), np.max(self.coords_h10000[1, :])
            return bbx

    def connect_points(self):
        """
        connect points with lines
        """
        points = []
        normed_coords = np.array(self.coords)
        normed_coords[0, :] = normed_coords[0, :] * 10.0 / self.norm_w
        normed_coords[1, :] = normed_coords[1, :] * 10.0 / self.norm_h
        normed_coords = normed_coords.astype(int)
        prev_coords = normed_coords[:, 0]
        for idx in range(1, normed_coords.shape[1]):
            rr, cc = line(prev_coords[0], prev_coords[1], normed_coords[0, idx], normed_coords[1, idx])
            points.append([rr, cc])
            prev_coords = normed_coords[:, idx]
        if points == []:
            return normed_coords
        else:
            return np.concatenate(points, axis=1)

    def set_norm(self, norm_w, norm_h):
        """
        set normalized width and height, and calculate normalized coordinates
        """
        self.norm_w = norm_w
        self.norm_h = norm_h
        self.normed_connected_coords = self.connect_points()

    def set_truth(self, truth):
        self.truth = truth

    def set_ref(self, ref):
        self.ref = ref

    def __str__(self):
        return "coords: %s, ref: %s" % (self.coords, self.ref)

    def get_width(self):
        return np.max(self.coords[0, :]) - np.min(self.coords[0, :])

    def get_height(self):
        return np.max(self.coords[1, :]) - np.min(self.coords[1, :])

    def min_dist(self, trace2):
        dist = distance.cdist(self.coords_h10000.T, trace2.coords_h10000.T, 'euclidean')
        return np.min(dist)

    def seg_feature(self, other):
        """
        calculate features for segmentation(if it should be grouped with trace2 or not)
        """
        mind = self.min_dist(other)

        x1 = np.mean(self.normed_connected_coords[0, :])
        y1 = np.mean(self.normed_connected_coords[1, :])
        x2 = np.mean(other.normed_connected_coords[0, :])
        y2 = np.mean(other.normed_connected_coords[1, :])
        size1 = max(self.get_width(), self.get_height())
        size2 = max(other.get_width(), other.get_height())
        size_diff = np.abs(size1 - size2) / (np.linalg.norm([10.0, 10.0]))
        hor_diff = np.abs(x1 - x2) / 10.0
        ver_diff = np.abs(y1 - y2) / 10.0
        return hor_diff, ver_diff, size_diff, dist


    def distance(self, other):
        '''
        calculate euclidean distance between this stroke and other stroke.
        :param other:
        :return:
        '''
        dist = distance.cdist(self.coords_h10000.T, other.coords_h10000.T, 'euclidean')
        #print '\n', self.coords_h10000.shape, trace2.coords_h10000.shape
        #print dist.shape
        #print np.where(dist == dist.min())
        #print dist.argmin()
        # dist = dist / (np.linalg.norm([self.norm_h,self.norm_w]))
        #dist = dist / (np.linalg.norm([10.0, 10.0]))
        dmin = np.min(dist)

        return np.min(dist)

    def get_bounding_box(self):
        if self.bounding_box == None:
            self.bounding_box = np.min(self.coords[0, :]), np.min(self.coords[1, :]), np.max(self.coords[0, :]), np.max(
            self.coords[1, :])
        return self.bounding_box

    def visible(self, trace2, trace_map):
        """
        calculate if it's visible to trace2, which means
        no other traces block them
        """
        rr1, cc1 = self.normed_connected_coords[0, :], self.normed_connected_coords[1,
                                                       :]  # np.nonzero(trace_map == self.id)
        cd1 = np.vstack([rr1, cc1])
        rr2, cc2 = trace2.normed_connected_coords[0, :], trace2.normed_connected_coords[1,
                                                         :]  # np.nonzero(trace_map == trace2.id)
        cd2 = np.vstack([rr2, cc2])
        dist = distance.cdist(cd1.T, cd2.T, 'euclidean')

        x, y = np.unravel_index(np.argmin(dist), dist.shape)
        x1, y1 = cd1[:, x]
        x2, y2 = cd2[:, y]

        rr, cc = line(int(x1), int(y1), int(x2), int(y2))
        for idx in range(len(rr)):
            pixels = (trace_map[rr[idx] - 1:rr[idx] + 2, cc[idx] - 1:cc[idx] + 1] != self.id) \
                     * (trace_map[rr[idx] - 1:rr[idx] + 2, cc[idx] - 1:cc[idx] + 1] != trace2.id) \
                     * (trace_map[rr[idx] - 1:rr[idx] + 2, cc[idx] - 1:cc[idx] + 1] != -1)
            if np.sum(pixels) != 0: return 0
        return 1

    def segmentation_feature(self, trace2):
        """
        calculate features for segmentation(if it should be grouped with trace2 or not)
        """
        dist = self.distance(trace2)

        x1 = np.mean(self.normed_connected_coords[0, :])
        y1 = np.mean(self.normed_connected_coords[1, :])
        x2 = np.mean(trace2.normed_connected_coords[0, :])
        y2 = np.mean(trace2.normed_connected_coords[1, :])
        size1 = max(self.get_width(), self.get_height())
        size2 = max(trace2.get_width(), trace2.get_height())
        size_diff = np.abs(size1 - size2) / (np.linalg.norm([10.0, 10.0]))
        hor_diff = np.abs(x1 - x2) / 10.0
        ver_diff = np.abs(y1 - y2) / 10.0
        return hor_diff, ver_diff, size_diff, dist


def get_bounding_box(traces):
    """

    Parameters
    ----------
    traces: list of Trace object

    Returns
    -------
    tuple (x, y, s, t)

    """
    x_min, y_min, x_max, y_max = traces[0].get_bounding_box()
    for idx in range(1, len(traces)):
        curr_x_min, curr_y_min, curr_x_max, curr_y_max = traces[idx].get_bounding_box()
        x_min = min(x_min, curr_x_min)
        y_min = min(y_min, curr_y_min)
        x_max = max(x_max, curr_x_max)
        y_max = max(y_max, curr_y_max)
    return x_min, y_min, x_max, y_max

def get_bounding_box_h1000(traces):
    """

    Parameters
    ----------
    traces: list of Trace object

    Returns
    -------
    tuple (x, y, s, t)

    """
    x_min, y_min, x_max, y_max = traces[0].get_bounding_box_h10000()
    for idx in range(1, len(traces)):
        curr_x_min, curr_y_min, curr_x_max, curr_y_max = traces[idx].get_bounding_box_h10000()
        x_min = min(x_min, curr_x_min)
        y_min = min(y_min, curr_y_min)
        x_max = max(x_max, curr_x_max)
        y_max = max(y_max, curr_y_max)
    return x_min, y_min, x_max, y_max
