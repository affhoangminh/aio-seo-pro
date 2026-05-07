contexts = []


def register_context(context):

    contexts.append(context)


def close_all():

    for c in contexts:

        try:
            c.close()
        except:
            pass

    contexts.clear()