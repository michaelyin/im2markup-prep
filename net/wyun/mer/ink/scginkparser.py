#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read and parse data from the lanking project."""

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def remove_matching_braces(latex):
    """
    If `latex` is surrounded by matching braces, remove them. They are not
    necessary.

    Parameters
    ----------
    latex : string

    Returns
    -------
    string

    Examples
    --------
    >>> remove_matching_braces('{2+2}')
    '2+2'
    >>> remove_matching_braces('{2+2')
    '{2+2'
    """
    if latex.startswith('{') and latex.endswith('}'):
        opened = 1
        matches = True
        for char in latex[1:-1]:
            if char == '{':
                opened += 1
            elif char == '}':
                opened -= 1
            if opened == 0:
                matches = False
        if matches:
            latex = latex[1:-1]
    return latex


def parse_scg_ink_file(contents, scg_id):
    """Parse a SCG INK contents.

    Parameters
    ----------
    scg_id : string
        The path to a SCG INK file.

    Returns
    -------
    HandwrittenData
        The recording as a HandwrittenData object.
    """
    stroke_count = 0
    stroke_point_count = -1
    recording = []
    current_stroke = []
    time = 0
    got_annotations = False
    annotations = []

    lines = contents.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0 and line != 'SCG_INK':
            raise ValueError(("%s: SCG Ink files have to start with 'SCG_INK'."
                              " The file started with %s.") %
                             (scg_id, line))
        elif i == 1:
            try:
                stroke_count = int(line)
            except ValueError:
                raise ValueError(("%s: Second line has to be the number of "
                                  "strokeswhich has to be an integer, but "
                                  "was '%s'") % (scg_id, line))
            if stroke_count <= 0:
                raise ValueError(("%s: Stroke count was %i, but should be "
                                  "> 0.") % (scg_id, stroke_count))
        elif i == 2:
            try:
                stroke_point_count = int(line)
            except ValueError:
                raise ValueError("%s: Third line has to be the number of "
                                 "points which has to be an integer, but was "
                                 "'%s'" % (scg_id, line))
            if stroke_point_count <= 0:
                raise ValueError(("%s: Stroke point count was %i, but should "
                                  "be > 0.") % (scg_id, stroke_count))
        elif i > 2:
            if stroke_point_count > 0:
                x, y = [int(el) for el in line.strip().split(" ")]
                current_stroke.append((x, y))
                time += 20
                stroke_point_count -= 1
            elif line == 'ANNOTATIONS' or got_annotations:
                got_annotations = True
                annotations.append(line)
            elif stroke_count > 0:
                try:
                    stroke_point_count = int(line)
                except ValueError:
                    raise ValueError(("%s: Line %i has to be the number of "
                                      "points which has to be an integer, "
                                      " but was '%s'") %
                                     (scg_id, i + 1, line))
                if stroke_point_count <= 0:
                    raise ValueError(("%s: Stroke point count was %i, but "
                                      "should be > 0.") %
                                     (scg_id, stroke_count))
            if stroke_point_count == 0 and len(current_stroke) > 0:
                time += 200
                recording.append(current_stroke)
                stroke_count -= 1
                current_stroke = []
    return recording

'''
def main(directory):
    user_dirs = natsorted(list(next(os.walk(directory))[1]))
    recordings = []
    for user_dir in user_dirs:
        user_dir = os.path.join(directory, user_dir)
        logging.info("Start getting data from %s...", user_dir)
        recordings += read_folder(user_dir)
    logging.info("Got %i recordings.", len(recordings))
    logging.info("Double segmented strokes: %i (%0.2f%%)",
                 len(double_segmentation),
                 float(len(double_segmentation)) / len(recordings))
    logging.info("Missing segmented strokes: %i (%0.2f%%)",
                 len(missing_stroke_segmentation),
                 float(len(missing_stroke_segmentation)) / len(recordings))
    for recording in recordings:
        datasets.insert_recording(recording)
'''
