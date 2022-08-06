from dataclasses import Field, field
from typing import Any, Iterable, Optional, Tuple, Union


def config(
    long: Optional[bool] = None,
    short: Optional[Union[bool, str]] = None,
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
) -> Field:
    metadata = {}
    metadata.update(kwargs)

    assign_if_not_none(metadata, "long", long)
    assign_if_not_none(metadata, "short", short)
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

    # to avoid errors like below:
    # ValueError: mutable default <class 'list'> for field hoge is not allowed: use default_factory
    if isinstance(default, (list, dict, set)):
        return field(
            default_factory=lambda: default,
            metadata=metadata,
        )
    else:
        return field(
            default=default,
            metadata=metadata,
        )


def assign_if_not_none(d: dict, key: str, value: Any):
    if value is None:
        return
    d[key] = value
