# definition of classes(Trace,Symbol,InkData)
from __future__ import division

from collections import Counter
from xml.etree import ElementTree as ET

import numpy as np
from scipy import misc
from scipy.spatial import distance
import math

from net.wyun.mer.symbol.symbol import Symbol
from stroke import Stroke
from stroke import get_bounding_box
from stroke import get_bounding_box_h1000

DEBUG = False
rel_dict = Counter()


'''

'''
FLT_MAX = float('inf')
INF_DIST = FLT_MAX

class Sample(object):
    def __init__(self, file_path, debug=DEBUG):
        self.file_path = file_path
        tree = ET.parse(file_path, ET.XMLParser(encoding='utf-8'))
        root = tree.getroot()
        self.id_count = ID_Count()
        self.traces = self.loading_traces(root, debug=debug) # scale coords to h10000
        # calculate ox, oy, os, ot, and IMGxMIN, IMGyMIN, IMGxMAX, IMGyMAX
        (self.ox, self.oy, self.os, self.ot) = get_bounding_box_h1000(self.traces)
        (self.IMGxMIN, self.IMGyMIN, self.IMGxMAX, self.IMGyMAX) = (self.ox, self.oy, self.os, self.ot)

        self.truth_list = self.get_truth(root)
        self.norm_w, self.norm_h = self.calculate_stroke_norm()
        self.symbols = self.get_symbols(root)
        self.spatial_rel = None
        self.image = self.draw_image(debug)
        self.trace_map = self.draw_trace_map()
        self.INF_DIST = FLT_MAX
        if debug:
            print(self.norm_w, self.norm_h)

    def re_calculate_IMG_MINMAX(self):
        (self.ox, self.oy, self.os, self.ot) = get_bounding_box_h1000(self.traces)
        (self.IMGxMIN, self.IMGyMIN, self.IMGxMAX, self.IMGyMAX) = (self.ox, self.oy, self.os, self.ot)

    def nStrokes(self):
        return len(self.traces)

    def detRefSymbol(self):

        vmedx = np.zeros((1, self.nStrokes()))
        vmedy = np.zeros((1, self.nStrokes()))
        RX = 0
        RY = 0
        nregs = 0
        mAr = 0.0
        #Compute reference symbol for normalization
        for i in range(0, self.nStrokes()):
            ancho, alto, aspectratio, area = self.stroke_aspect_area(i)
            vmedx[0,i] = ancho
            vmedy[0,i] = alto

            mAr += area
            if aspectratio >= 0.25 and aspectratio <= 4.0:
                RX += ancho
                RY += alto
                nregs += 1
        #Average area
        #vmedx: Name : vmedx, Details:std::vector of length 10, capacity 16 = {9623, 6039, 7360, 7360, 6982, 4152, 3586, 3586, 6793, 5284}
        mAr /= self.nStrokes()
        lAr = int(math.sqrt(mAr) + 0.5)
        lAr *= 0.9

        if nregs > 0:
            RX /= nregs
            RY /= nregs
        else:
            for i in range(0, self.nStrokes()):
                ancho, alto, aspectratio, area = self.stroke_aspect_area(i)

                RX += ancho
                RY += alto
                nregs += 1
            RX /= nregs
            RY /= nregs
        #Compute median
        #medx = np.median(vmedx) #TODO: try to use median to see if it improves accuracy
        #medy = np.median(vmedy)
        vmedx.sort()
        half = int(self.nStrokes()/2)
        medx = vmedx[0, half]
        vmedy.sort()
        medy = vmedy[0, half]

        RX = (RX + medx + lAr)/3.0
        RY = (RY + medy + lAr)/3.0

        self.RX, self.RY = int(RX), int(RY)

        return self.RX, self.RY

    def stroke_aspect_area(self, i):
        '''

        :param i: id (index) of the stroke in traces
        :return: (ancho, alto, aspectratio, area)
        '''
        stroke = self.traces[i]
        rx, ry, rs, rt = stroke.get_bounding_box_h10000()
        ancho = rs - rx + 1
        alto = rt - ry + 1
        aspectratio = ancho * 1.0 / alto
        area = ancho * alto
        return ancho, alto, aspectratio, area


    def draw_image(self, debug=False):
        """
        generate the normalized image of whole math expression contained in this
        Inkml File
        """
        zoom_x = 10.0 / self.norm_w
        zoom_y = 10.0 / self.norm_h
        if debug:
            print('zoom_x: %f,zoom_y: %f\n' % (zoom_x, zoom_y))
        all_coords = []
        for _, trace in self.traces.iteritems():
            all_coords.append(trace.normed_connected_coords)
        all_coords = np.concatenate(all_coords, axis=1)
        # all_coords[0,:] = all_coords[0,:] * zoom_x
        all_coords[0, :] = all_coords[0, :] - np.min(all_coords[0, :])
        # all_coords[1,:] = all_coords[1,:] * zoom_y
        all_coords[1, :] = all_coords[1, :] - np.min(all_coords[1, :])
        if debug:
            print(all_coords)
        all_coords = np.round(all_coords).astype(int)
        if debug:
            print(all_coords)
        max_x, max_y = np.max(all_coords, axis=1)
        if debug:
            print(max_x, max_y)
        image = np.zeros((max_x + 1, max_y + 1))
        for i in range(all_coords.shape[1]):
            image[all_coords[0, i], all_coords[1, i]] = 255
        #misc.imsave('temp/all.png', image.T)
        return image

    def draw_trace_map(self):
        """
        draw the image and mark each trace with different value
        """
        min_x, min_y = None, None
        max_x, max_y = None, None
        for _, trace in self.traces.iteritems():
            if min_x is None:
                min_x, min_y = np.min(trace.normed_connected_coords, axis=1)
                max_x, max_y = np.max(trace.normed_connected_coords, axis=1)
            else:
                min_x = min(min_x, np.min(trace.normed_connected_coords[0, :]))
                min_y = min(min_y, np.min(trace.normed_connected_coords[1, :]))
                max_x = max(max_x, np.max(trace.normed_connected_coords[0, :]))
                max_y = max(max_y, np.max(trace.normed_connected_coords[1, :]))
        trace_map = np.zeros((max_x - min_x + 1, max_y - min_y + 1))
        trace_map -= 1
        for _, trace in self.traces.iteritems():
            trace_map[
                trace.normed_connected_coords[0, :] - min_x, trace.normed_connected_coords[1, :] - min_y] = trace.id
            trace.normed_connected_coords[0, :] -= min_x
            trace.normed_connected_coords[1, :] -= min_y
        #misc.imsave('temp/map.png', trace_map.T)
        return trace_map

    def loading_traces(self, root, debug=False):
        """
        extract all traces from Inkml File
        generate scaled coordinates with H is maxed up to 10000
        """
        traces = dict()
        for child in root:
            tag = child.tag
            attrib = child.attrib
            #print child.tag, child.attrib
            if tag.endswith('annotation') and attrib and attrib['type'] == 'truth':
                self.latex = child.text.strip()
            if child.tag[-5:] == 'trace':
                trace_id = child.attrib['id']
                coords = child.text
                splitted = coords.split(',')
                coords = np.zeros((2, len(splitted)))
                idx = 0
                for x_y in splitted:
                    x_y = x_y.strip().split(' ')
                    coords[:, idx] = [float(x_y[0]), float(x_y[1])]
                    idx += 1
                trace_id_int = int(trace_id)
                self.id_count.next_id = trace_id_int
                traces[trace_id_int] = Stroke(trace_id_int, coords)
        if debug:
            print('trace dict:\n', traces)

        # //Compute bounding box of the input expression
        x_min, y_min, x_max, y_max = get_bounding_box(traces)  # bounding box for the whole math expression

        # Just in case there is only one point or a sequence of	points perfectly aligned with the x or y axis
        if x_max == x_min: x_max = x_min + 1;
        if y_max == y_min: y_max = y_min + 1;

        # Renormalize to height [0,10000] keeping the aspect ratio
        H = 10000.0
        W = H * (x_max - x_min) / (y_max - y_min)
        for trace_key, trace_v in traces.iteritems():
            trace_v.calc_coords_h10000(H, W, x_min, y_min, x_max, y_max)

        return traces

    def getAVGstroke_size(self):
        avgw = 0.0
        avgh = 0.0
        for trace_key, trace_v in self.traces.iteritems():
            rx, ry, rs, rt = trace_v.get_bounding_box_h10000()
            avgw += rs - rx
            avgh += rt - ry

        avgw /= len(self.traces)
        avgh /= len(self.traces)
        return avgw, avgh

    def traverse_truth(self, node, truth_list):
        """
        node, node of the parsed tree
        recursively extract the truth of math expression from Inkml file
        """
        for child in node:
            tag = self.remove_prefix(child.tag, '{http://www.w3.org/1998/Math/MathML}')
            if 'mi' == tag or 'mn' == tag or 'mo' == tag:
                # print 'child.text: ', child.text, 'child.tag: ', child.tag
                if child.text != None:
                    truth_list.append((child.text, child.attrib['{http://www.w3.org/XML/1998/namespace}id']))
            else:
                self.traverse_truth(child, truth_list)

    def remove_prefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    def get_truth(self, root, debug=False):
        """
        root, root of the xml in Inkml file
        extract the truth of math expression from Inkml file
        """
        truth_list = []
        for child in root:
            if 'annotationXML' in child.tag:
                self.traverse_truth(child, truth_list)
        return truth_list

    def get_symbols(self, root, debug=False):
        """
        root, root of the xml in Inkml file
        extrace symbols from Inkml file
        """
        symbols = dict()
        for child in root:
            if 'traceGroup' in child.tag:
                for node in child:
                    if 'traceGroup' in node.tag:
                        self.process_symbol(node, symbols)
        return symbols

    def process_symbol(self, node, symbols):
        """
        generate a dictionary of symbols to stores symbol information from
        Inkml file
        """
        curr_truth = None
        curr_traces = []
        curr_ref = None
        for child in node:
            if 'annotation' == child.tag[-10:]:
                curr_truth = child.text
            elif 'annotationXML' in child.tag:
                curr_ref = child.attrib['href']
            elif 'traceView' in child.tag:
                curr_traces.append(self.traces[int(child.attrib['traceDataRef'])])
        symbols[curr_ref] = Symbol(curr_ref, curr_truth, curr_traces)  # (curr_truth,curr_traces)
        for trace in curr_traces:
            trace.set_ref(curr_ref)
            trace.set_truth(curr_truth)

            # return symbols

    def calculate_stroke_norm(self):
        """
        calculate normalized width and height of strokes (traces)
        It is the same value passed to Trace and PCFG_Cell classes
        """
        widths = []
        heights = []
        for _, trace in self.traces.iteritems():
            widths.append(trace.get_width())
            heights.append(trace.get_height())
        norm_w, norm_h = max(np.median(widths), np.mean(widths)), max(np.median(heights), np.mean(heights))
        for _, trace in self.traces.iteritems():
            trace.set_norm(norm_w, norm_h)
        return norm_w, norm_h

    def read_lg(self, file_path):
        """
        read corresponding lg file
        """
        self.spatial_rel = dict()
        with open(file_path, 'r') as fin:
            for line in fin:
                if '# Relations from SRT:' in line:
                    break
            for line in fin:
                splitted = line.split(',')
                ref1 = splitted[1].strip()
                ref2 = splitted[2].strip()
                relation = splitted[3].strip()
                self.spatial_rel[(ref1, ref2)] = relation
                if DEBUG:
                    rel_dict[relation] += 1

    def cal_visible_matrix(self):
        """
        calculate the visible matrix
        """
        dim = len(self.traces)
        mat = np.zeros((dim, dim), dtype=bool)
        for i in range(dim):
            for j in range(i + 1):
                if i == j:
                    mat[i, j] = True
                else:
                    mat[i, j] = self.traces[i].visible(self.traces[j], self.trace_map)
                    mat[j, i] = mat[i, j]
        return mat

    def cal_dist_matrix(self):
        """
        calculate the distance matrix
        """
        dim = len(self.traces)
        mat = np.zeros((dim, dim), dtype=bool)
        for i in range(dim):
            for j in range(i + 1):
                if i == j:
                    mat[i, j] = True
                else:
                    mat[i, j] = self.traces[i].distance(self.traces[j])
                    mat[j, i] = mat[i, j]
        return mat

    ###################
    #seshat
    ###################
    def group_penalty(self, A, B):
        '''
        get the min distance between two cells
        :param A: CellCYK
        :param B: CellCYK
        :return: min. distance
        '''
        dmin = INF_DIST
        for i in A.strokes:
            for j in B.strokes:
                if self.getDist(i, j) < dmin:
                    dmin = self.getDist(i, j)
        return dmin

    def setRegion(self, c, stkc1):
        '''

        :param c, CellCYK
        :param stkc1: integer, number of the trace
        :return:
        '''
        c.add_to_strokes(stkc1)
        c.x, c.y, c.s, c.t = self.traces[stkc1].get_bounding_box()

    def getDist(self, si, sj):
        '''
        distance between si and sj from the distance matrix
        :param si: int, stroke index
        :param sj: int
        :return:
        '''
        return self.stk_dis[si][sj];

    def get_close_strokes(self, id, L, dist_th):
        '''
        get list of valid neighbor strokes
        :param id: stroke id
        :param L: list<int>
        :param dist_th: distance threshold, segmentsTH
        :return:
        '''
        added = [False] * id
        for i in range(0, id):
            if self.getDist(id, i) < dist_th:
                L.append(i)
                added[i] = True

        #Add second degree distance < dist_th
        auxlist = []
        for item in L:
            for i in range(0, id):
                if not added[i] and self.getDist(item, i) < dist_th:
                    auxlist.append(i)
                    added[i] = True

        for item in auxlist:
            L.append(item)


    def compute_strokes_distances(self, rx, ry):
        #Create distances matrix NxN (strokes)
        dim = len(self.traces)
        stk_dis = np.zeros((dim, dim), dtype=float)

        NORMF = math.sqrt(rx*rx + ry*ry)
        INF_DIST = float('inf') / NORMF

        #Compute distance among every stroke
        for i in range(dim):
            stk_dis[i][i] = 0.0
            for j in range(i + 1, dim):
                    stk_dis[i, j] = self.stroke_distance(i, j)/NORMF
                    stk_dis[j, i] = stk_dis[i, j]
        self.stk_dis = stk_dis
        return stk_dis

    def stroke_distance(self, si, sj):
        '''
        find the min distance between traces[si] and traces[sj]. also consider visibility between si and sj
        :param si: stroke with index si in self.traces
        :param sj: stroke with index sj in self.traces
        :return: min distance between points from trace si to trace sj
        '''
        dmin, pi, pj = self.find_closest_pair(si, sj)
        if self.not_visible(si, sj, pi, pj):
            dmin = FLT_MAX

        return dmin

    def find_closest_pair(self, si, sj):
        '''
        find the min distance between traces[si] and traces[sj], and also the pair of points generates the min dist.
        :param si: same as in stroke_distance()
        :param sj:
        :return: dmin, (xi, yi), (xj, yj)
        '''
        trace1 = self.traces[si]
        trace2 = self.traces[sj]
        dist = distance.cdist(trace1.coords_h10000.T, trace2.coords_h10000.T, 'euclidean')

        (pi_lst, pj_lst) = np.where(dist == dist.min())
        pi, pj = pi_lst[0], pj_lst[0]
        point_i = trace1.coords_h10000[:, pi]
        point_j = trace2.coords_h10000[:, pj]

        dmin = np.min(dist)
        #print 'stroke pair: ', si, sj, dmin, tuple(point_i), tuple(point_j)
        return dmin, tuple(point_i), tuple(point_j)

    def not_visible(self, si, sj, min_pi, min_pj):
        '''
        //Go through the pixels from pi to pj checking that there is not a pixel that belongs
        //to a stroke that is not either si or sj. If so, then sj is not visible from si
        :param si:
        :param sj:
        :param min_pi:
        :param min_pj:
        :return:
        '''
        pi_x, pi_y = min_pi
        pj_x, pj_y = min_pj

        pa_x = 5 + (self.X - 10) * float((pi_x - self.IMGxMIN) / (self.IMGxMAX - self.IMGxMIN + 1))
        pa_y = 5 + (self.Y - 10) * float((pi_y - self.IMGyMIN) / (self.IMGyMAX - self.IMGyMIN + 1))
        pb_x = 5 + (self.X - 10) * float((pj_x - self.IMGxMIN) / (self.IMGxMAX - self.IMGxMIN + 1))
        pb_y = 5 + (self.Y - 10) * float((pj_y - self.IMGyMIN) / (self.IMGyMAX - self.IMGyMIN + 1))

        dl = 3.125e-3
        dx = int(pb_x) - int(pa_x)
        dy = int(pb_y) - int(pa_y)

        l_arr = np.arange(0, 1, dl)
        x_arr = int(pa_x) + (l_arr * dx + 0.5).astype(int)
        y_arr = int(pa_y) + (l_arr * dy + 0.5).astype(int)

        #if (self.dataoff[y, x] == 0).any and (self.pix_stk[y, x] != si).a and (self.pix_stk[y, x] != sj).all:
        #    return False
        for idx in range(0, len(l_arr)):
            x, y = x_arr[idx], y_arr[idx]
            if self.dataoff[y, x] == 0 and self.pix_stk[y, x] != si and self.pix_stk[y, x] != sj:
                return True
        return False

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

        self.dataoff = img
        return img, W, H


    #############################################################

    def inkml_part_1(self, pcfg_cell, inkml_out):
        latex = pcfg_cell.get_latex()
        inkml = '''<ink xmlns="http://www.w3.org/2003/InkML">
		<traceFormat>
			<channel name="X" type="decimal"/>
			<channel name="Y" type="decimal"/>
		</traceFormat>
		<annotation type="category">Arithmetic</annotation>
		<annotation type="writer">python</annotation>\n '''
        inkml += '    <annotation type="truth">$' + latex + '$</annotation>\n'

        inkml += '<annotationXML type="truth" encoding="Content-MathML">\n'
        inkml += "<math xmlns='http://www.w3.org/1998/Math/MathML'>\n"
        inkml_out.write(inkml)

    def inkml_stokes(self, inkml_out):
        inkml = ''
        # traces here
        for t_id, trace in self.traces.iteritems():
            inkml = inkml + '<trace id="' + str(trace.id) + '">\n'

            tc_coor = trace.coords.astype(int)
            print 'data types: ', tc_coor.dtype
            (xl, yl) = np.shape(trace.coords)
            for y_idx in range(0, yl):
                po = tc_coor[:, y_idx]
                inkml = inkml + str(po[0]) + ' ' + str(po[1]) + ', '
            inkml += '\n</trace>\n'
        inkml_out.write(inkml)

    def print_inkml(self, file_out, pcfg_cell):
        next_id = 0
        self.id_count.bak()

        with open(file_out, 'w+') as inkml_out:
            self.inkml_part_1(pcfg_cell, inkml_out)
            # mathml
            if not pcfg_cell.isTerminal():
                pcfg_cell.production.print_mathml(inkml_out, pcfg_cell, self.id_count)
            else:
                # terminal
                sbl = pcfg_cell.cell1  # Symbol
                inkml_id = sbl.truth + '_' + self.id_count.get_next_id()
                sbl.inkml_id = inkml_id  # add property inkml_id to Symbol

                inkml_out.write("<mi xml:id=\"" + inkml_id + "\">" + sbl.truth + "</mi>\n")

            # Restore next_id
            self.id_count.recover()
            inkml_out.write("</math>\n")
            inkml_out.write('</annotationXML>\n\n')
            # Print the strokes
            self.inkml_stokes(inkml_out)

            inkml_out.write(
                '\n<traceGroup xml:id="' + self.id_count.get_next_id() + '">\n    <annotation type="truth">Segmentation</annotation>\n')
            inkml_sym_rec(pcfg_cell, inkml_out, self.id_count)
            inkml_out.write('</traceGroup>\n</ink>')


def inkml_sym_rec(pcfg_cell, inkml_out, id_count):
    H = pcfg_cell
    if not H.isTerminal():
        inkml_sym_rec(H.cell1, inkml_out, id_count)
        inkml_sym_rec(H.cell2, inkml_out, id_count)
    else:
        next_id = id_count.get_next_id()
        inkml_out.write('  <traceGroup xml:id="' + next_id + '">\n')
        inkml_out.write('    <annotation type="truth">' + H.cell1.truth + '</annotation>\n')
        for trace in H.cell1.traces:
            inkml_out.write('    <traceView traceDataRef="' + str(trace.id) + '" />\n')
        inkml_id = None
        print "H production latex", H.production.latex
        if hasattr(H.cell1, 'inkml_id'):
            inkml_id = H.cell1.inkml_id
        else:
            inkml_id = H.inkml_id

        inkml_out.write('    <annotationXML href="' + inkml_id + '" />\n')
        inkml_out.write('  </traceGroup>\n')


class ID_Count(object):
    def __init__(self, next_id=0, nid_bak=0):
        self.next_id = next_id
        self.nid_bak = nid_bak

    def get_next_id(self):
        self.next_id += 1
        return str(self.next_id)

    def bak(self):
        self.nid_bak = self.next_id

    def recover(self):
        self.next_id = self.nid_bak

