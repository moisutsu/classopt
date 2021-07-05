from dataclasses import field
from typing import Any, Optional, Union, Iterable, Tuple


def config(
    long: bool = False,
    short: Union[bool, str] = False,
    action: Optional[str] = None,
    nargs: Optional[Union[int, str]] = None,
    const: Any = None,
    default: Any = None,
    type: Optional[type] = None,
    choices: Optional[Iterable] = None,
    required: Optional[bool] = None,
    help: Optional[str] = None,
    metavar: Optional[Union[str, Tuple[str]]] = None,
    dest: Optional[str] = None,
    version: Optional[str] = None,
    **kwargs: Any,
):
    metadata = {}
    metadata.update(kwargs)

    metadata["long"] = long
    metadata["short"] = short
    assign_if_not_none(metadata, "action", action)
    assign_if_not_none(metadata, "nargs", nargs)
    assign_if_not_none(metadata, "const", const)
    assign_if_not_none(metadata, "default", default)
    assign_if_not_none(metadata, "type", type)
    assign_if_not_none(metadata, "choices", choices)
    assign_if_not_none(metadata, "required", required)
    assign_if_not_none(metadata, "help", help)
    assign_if_not_none(metadata, "metavar", metavar)
    assign_if_not_none(metadata, "dest", dest)
    assign_if_not_none(metadata, "version", version)

    return field(metadata=metadata)


def assign_if_not_none(d: dict, key: str, value: Any):
    if value is None:
        return
    d[key] = value
