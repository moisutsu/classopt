from dataclasses import field


def option(**kwargs):
    return field(metadata=kwargs)
