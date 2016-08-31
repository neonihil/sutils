
from .primitives import qlist, qdict
__all__ = qlist()

# ---------------------------------------------------
# setup_logging()
# ---------------------------------------------------

logging = None

LOG_FORMATS = qdict(
    short = "%(asctime)s\t%(levelname)s\t%(name)s:\t%(message)s",
    thread = "%(asctime)s\t%(levelname)s\t[tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
    process = "%(asctime)s\t%(levelname)s\t[pid:%(process)d]\t%(name)s:\t%(message)s",
    full = "%(asctime)s\t%(levelname)s\t[pid:%(process)d tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
)

def setup_logging( level = 'INFO', format_ = LOG_FORMATS.short):
    global logging
    if not logging:
        import logging as logging_
        logging = logging_
    logging.basicConfig( format = format_, level = level )


# ---------------------------------------------------
# logged()
# ---------------------------------------------------

def _add_logger(obj, channel = None, root_channel = None, attr_name = "__logger" ):
    setup_logging()
    cls = obj
    channel = channel or cls.__name__
    root_channel = root_channel if root_channel is not None else cls.__module__
    if root_channel:
        channel = root_channel + '.' + channel
    if attr_name.startswith( '__' ): 
        attr_name = '_' + cls.__name__ + '__logger'
    setattr( obj, attr_name, logging.getLogger(channel) )

@__all__.register
def logged(obj):
    _add_logger(obj, root_channel = '')
    return obj

