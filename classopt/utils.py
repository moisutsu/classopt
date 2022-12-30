import typing
from typing import Any, Union

GENERIC_ALIASES = {typing._GenericAlias}
try:
    from types import GenericAlias

    GENERIC_ALIASES.add(GenericAlias)
except ImportError:
    pass


PRIMITIVE_TYPES = {
    int,
    float,
    complex,
    bool,
    str,
    list,
    tuple,
    set,
    dict,
    type(None),
}


def revert_type_from_generic(type_: type) -> type:
    if type(type_) in GENERIC_ALIASES:
        return type_.__origin__
    else:
        return type_


def convert_non_primitives_to_string(value: Any) -> Union[Any, str]:
    if revert_type_from_generic(type(value)) in PRIMITIVE_TYPES:
        return value
    else:
        return str(value)


def revert_non_primitives_from_string(value: Any, original_type: type):
    if revert_type_from_generic(original_type) in PRIMITIVE_TYPES:
        return value
    else:
        return original_type(value)
