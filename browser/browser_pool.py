import threading

contexts = []
shutdown_event = threading.Event()


def register_context(context):

    contexts.append(context)


def is_shutdown():
    return shutdown_event.is_set()


def close_all():

    shutdown_event.set()
    contexts.clear()