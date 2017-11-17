import json
from net.wyun.mer.ink.sample import Sample
from net.wyun.mer.ink.stroke import Stroke
from net.wyun.mer.ink import scginkparser
import numpy as np
from net.wyun.mer.ink.stroke import get_bounding_box
from scipy import misc

class Scg(object):

    def __init__(self, scg_id, scg_content, truth):
        self.id = scg_id
        self.content = scg_content
        self.truth_obj = Payload(truth)
        self.dummySample = Sample('data/inkml/65_alfonso.inkml')
        self.w_h_ratio = 1.0 # initialize here, updated in replace_traces()
        self.replace_traces()
        self.dummySample.re_calculate_IMG_MINMAX()


    def get_latex(self):
        return self.truth_obj.latex

    def replace_traces(self):
        '''
        replace the traces in dummySample with the one generated from scg_content
        :return:
        '''
        strokes = scginkparser.parse_scg_ink_file(self.content, self.id)

        #for st in strokes:
            #print st

        traces = {}

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

        self.dummySample.traces = traces

    def save_image(self, path):
        img, W, H = self.dummySample.render()
        print 'save image to: ', path
        misc.imsave(path, img)


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
