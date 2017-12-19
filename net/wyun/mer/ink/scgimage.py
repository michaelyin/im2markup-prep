from net.wyun.mer.ink.stroke import Stroke
from net.wyun.mer.ink import scginkparser
import numpy as np
from net.wyun.mer.ink.stroke import get_bounding_box
from scipy import misc

class ScgImage(object):

    def __init__(self, scg_content, scg_id=1):
        self.id = scg_id
        self.content = scg_content
        #self.dummySample = Sample('data/inkml/65_alfonso.inkml')
        #self.w_h_ratio = 1.0 # initialize here, updated in replace_traces()
        self.traces = {}
        self.load_traces()

        (self.IMGxMIN, self.IMGyMIN, self.IMGxMAX, self.IMGyMAX) = get_bounding_box_h1000(self.traces)
        #self.dummySample.re_calculate_IMG_MINMAX()


    def load_traces(self):
        '''
        replace the traces in dummySample with the one generated from scg_content
        :return:
        '''
        strokes = scginkparser.parse_scg_ink_file(self.content, self.id)

        #for st in strokes:
            #print st

        traces = self.traces

        trace_id_int = 0
        for st in strokes:
            coords = np.zeros((2, len(st)))
            idx = 0
            for x_y in st:
                coords[:, idx] = [float(x_y[0]), float(x_y[1])]
                idx += 1
            traces[trace_id_int] = Stroke(trace_id_int, coords)
            trace_id_int += 1

        # //Compute bounding box of the input expression
        x_min, y_min, x_max, y_max = get_bounding_box(traces)  # bounding box for the whole math expression

        # Just in case there is only one point or a sequence of	points perfectly aligned with the x or y axis
        if x_max == x_min: x_max = x_min + 1;
        if y_max == y_min: y_max = y_min + 1;

        self.w_h_ratio = float(x_max - x_min) / (y_max - y_min)
        # Renormalize to height [0,10000] keeping the aspect ratio
        H = 10000.0
        W = H * (x_max - x_min) / (y_max - y_min)
        for trace_key, trace_v in traces.iteritems():
            trace_v.calc_coords_h10000(H, W, x_min, y_min, x_max, y_max)

        #self.dummySample.traces = traces

    def save_image(self, path):
        img, W, H = self.render()
        print 'save image to: ', path
        misc.imsave(path, img)

    def render(self, pW=0, pH=0):
        (xMIN, yMIN, xMAX, yMAX) = (self.IMGxMIN, self.IMGyMIN, self.IMGxMAX, self.IMGyMAX)
        # Image dimensions
        W = xMAX - xMIN + 1
        H = yMAX - yMIN + 1

        R = float(W*1.0/H)
        #//Keeping the aspect ratio (R), scale to 256 pixels height
        H = 80 #256
        W = int(H * R)
        if W <= 0: W = 1

        #Give some margin to the image
        W += 10
        H += 10

        #initialize X, Y
        self.X = W
        self.Y = H

        #Create image
        img = np.ones((H, W), dtype = int)
        img *= 255

        #Create the structure that stores info of to which stroke each pixel belongs
        self.pix_stk = np.ones((H, W), dtype = int)
        self.pix_stk *= -1

        #Render image
        for key, trace in self.traces.iteritems():
            coords_tmp = np.array(trace.coords_h10000)
            coords_tmp[0, :] = 5 + (coords_tmp[0, :] - xMIN) * (W - 10) / (xMAX - xMIN + 1)
            coords_tmp[1, :] = 5 + (coords_tmp[1, :] - yMIN) * (H - 10) / (yMAX - yMIN + 1)

            int_coords = np.round(coords_tmp).astype(int)
            img[int_coords[1, :], int_coords[0, :]] = 0
            self.pix_stk[int_coords[1, :], int_coords[0, :]] = key

            #Draw a line between last point and current point
            #get length of coordinates
            (axis0, axis1) = int_coords.shape
            for idx in range(0, (axis1 - 1)):
                self.linea(img, int_coords[:,idx], int_coords[:, idx+1], key)

        #self.dataoff = img
        return img, W, H

    def linea(self, img, pa, pb, stkid):
        '''

        :param img: 2-d array created in render function
        :param pa: coord point a
        :param pb: coord point b
        :param stkid:
        :return:
        '''
        dl = 3.125e-3
        l_arr = np.arange(0, 1, dl)
        pa_x, pa_y = int(pa[0]), int(pa[1])
        pb_x, pb_y = int(pb[0]), int(pb[1])

        dx = pb_x - pa_x
        dy = pb_y - pa_y

        # x = np.round(pa_x + l_arr*dx + 0.5).astype(int)
        x = int(pa_x) + (l_arr * dx + 0.5).astype(int)
        y = int(pa_y) + (l_arr * dy + 0.5).astype(int)
        for idx_y in range(-1, 2):
            for idx_x in range(-1, 2):
                img[y + idx_y, x + idx_x] = 0
                self.pix_stk[y + idx_y, x + idx_x] = stkid

        return img


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

