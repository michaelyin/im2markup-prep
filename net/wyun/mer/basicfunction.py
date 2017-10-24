import logging
log = logging.getLogger("mer.basicfunction")

class BasicFunction(object):
    def __init__(self):
        self.state = 0

    def increment_state(self):
        log.debug("state increases by one")
        self.state += 1

    def clear_state(self):
        self.state = 0