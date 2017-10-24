from scipy import misc
import numpy as np
from skimage.draw._draw import line


__author__ = 'michael'

DEBUG = False

class Symbol(object):
    def __init__(self, ref, truth, traces, debug=DEBUG):
        """
        ref, its reference in Inkml file
        truth, ground truth of the symbol
        traces, a dict of traces which this symbol contains
        """
        self.ref = ref
        self.truth = truth
        self.traces = traces
        self.image = self.get_local_image(traces)

    def img2file(self):
        misc.imsave('temp/test_' + self.ref + '.png', self.image)

    def get_local_image(self, trace_dict):
        """
        generate a binary image of this symbol
        """
        coords = None
        trace_id_map = []

        counter = 0
        for trace in self.traces:
            if coords is None:
                coords = np.array(trace.coords)
            else:
                coords = np.concatenate((coords, trace.coords), axis=1)
            trace_id_map += [counter for i in range(trace.coords.shape[1])]
            counter += 1

        #self.calc_cmy_asc_des()

        max_width = np.max(coords[0, :]) - np.min(coords[0, :])
        max_height = np.max(coords[1, :]) - np.min(coords[1, :])
        max_length = max(max_width, max_height)
        coords[0, :] = (coords[0, :] - np.min(coords[0, :])) * 25.0 // (max_length + 1e-12)
        coords[1, :] = (coords[1, :] - np.min(coords[1, :])) * 25.0 // (max_length + 1e-12)
        center_x = (np.max(coords[0, :]) - np.min(coords[0, :])) // 2
        center_y = (np.max(coords[1, :]) - np.min(coords[1, :])) // 2
        coords[0, :] = coords[0, :] - center_x + 16
        coords[1, :] = coords[1, :] - center_y + 16
        coords = coords.astype(np.int)
        prev_id = -1
        image = np.zeros((32, 32), dtype=np.uint8)
        for idx in range(coords.shape[1]):
            if prev_id == trace_id_map[idx]:
                rr, cc = line(prev_x, prev_y, coords[0, idx], coords[1, idx])
                image[cc, rr] = 255
            prev_id = trace_id_map[idx]
            prev_x = coords[0, idx]
            prev_y = coords[1, idx]

        return image

    def calc_cmy_asc_des(self):
        '''
        compute the vertical centroid and ascendant/descendant centroid (as/ds)
        :return:
        '''
        coords = None
        for trace in self.traces:
            if coords is None:
                coords = np.array(trace.coords_h10000)
            else:
                coords = np.concatenate((coords, trace.coords_h10000), axis=1)
        coords_h10000 = coords
        #self.cmy = np.mean(coords[1, :], axis=0) #vertical centroid of the Symbol
        self.cmy = np.mean(coords[1, :], axis=0)  # vertical centroid of the Symbol
        self.bbox_h10000 = np.min(coords_h10000[0, :]), np.min(coords_h10000[1, :]), np.max(coords_h10000[0, :]), np.max(coords_h10000[1, :])
        self.asc = (self.cmy + self.bbox_h10000[3])/2
        self.des = (self.cmy + self.bbox_h10000[1])/2
        return (int(self.cmy), int(self.asc), int(self.des))

    def get_bounding_box(self):
        x_min, y_min, x_max, y_max = None, None, None, None
        for trace in self.traces:
            curr_x_min, curr_y_min, curr_x_max, curr_y_max = trace.get_bounding_box()
            if x_min is None:
                x_min, y_min, x_max, y_max = curr_x_min, curr_y_min, curr_x_max, curr_y_max
            else:
                x_min, y_min, x_max, y_max = np.min([x_min, curr_x_min]), np.min([y_min, curr_y_min]), \
                                             np.max([x_max, curr_x_max]), np.max([y_max, curr_y_max])
        return x_min, y_min, x_max, y_max


    def predict_symbol(self):
        return self.truth


class SymbolType(object):
    def __init__(self, file_path='config/symbol.types'):
        self.symbol_list = []
        self.symbol2type_dict = dict()

        with open(file_path, 'r') as fin:
            for line in fin:
                self.symbol_list.append(line.strip())
        self.totalClass = int(self.symbol_list[0])
        print 'total classes: ', self.totalClass, '\n'

        for ind, line in enumerate(self.symbol_list):
            if ind == 0:
                continue
            else:
                splitted = line.split()
                self.symbol2type_dict[splitted[0]] = splitted[1]

    def get_type(self, symbol):
        if symbol not in self.symbol2type_dict:
            raise ValueError('symbol not in SymbolType dictionary: ' + symbol)
            #return 'n'
        return self.symbol2type_dict[symbol]

    def checkClase(self, outStr):  #sym_rec->checkClase(pd->get_outstr())
        return outStr in self.symbol2type_dict

    def get_type_digit(self, symbol):
        tipo = self.get_type(symbol)

        if tipo == 'n':
            return 0
        elif tipo == 'a':
            return 1
        elif tipo == 'd':
            return 2
        elif tipo == 'm':
            return 3
        else:
            raise ValueError('wrong parameter for T: ' + tipo)

    def printLine(self):
        for symbol in self.symbol_list:
            print symbol


