# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
from . import myjson
import socketio

async_mode = "eventlet"

sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    json=myjson,
)
