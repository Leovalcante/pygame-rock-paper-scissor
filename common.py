import io

import config
from model import SafeUnpickler


def deserialize(bytes_):
    return SafeUnpickler(io.BytesIO(bytes_)).load()


def printd(msg):
    if config.debug:
        print(msg)
