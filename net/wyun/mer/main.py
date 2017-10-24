#!/usr/bin/env python

''' An example using our above logging.conf '''

import logging
import logging.config

logging.config.fileConfig('logging.conf')

import net.wyun.mer.basicfunction as bf
import net.wyun.mer.grammar.inkdata as inkdata

# !!!NOTE!!! Only ever need to do this once, in one file per project,
# and it MUST be done prior to anything using the logging module.
# Therefore you must import other app level modules after this.
#logging.config.fileConfig('logging.conf')


# Instantiate our logger for use only in this file
_log = logging.getLogger('mer.main')

def some_function():
    # Print a log statement
    _log.debug('Running function "some_function"')
    basic = bf.BasicFunction()
    basic.increment_state()
    _log.info('basic function new state: ' + str(basic.state))
    data = inkdata.load_inkml("data path")
    _log.info('inkdata: ' + str(data))


