from collections import defaultdict
from typing import Any, Iterable, Sequence

import sqlalchemy
from pydantic import PostgresDsn
from sqlalchemy import URL


def convert_pydantic_to_sqlalchemy_uri(value: PostgresDsn) -> URL:
    return sqlalchemy.make_url(str(value))


def format_output(
    keys: list | None, values: Sequence | None, single: bool = False, return_list: bool = False
) -> dict[str, Any] | list[dict]:
    if not values or not keys:
        return {} if single else []
    elif single:
        return {keys[i]: values[i] for i in range(len(keys))}
    elif return_list:
        return [{keys[i]: value[i] for i in range(len(keys))} for value in values]
    else:
        return {keys[i]: [value[i] for value in values] for i in range(len(keys))}


def pivot(data: list[dict], values: Iterable[str] | str, columns: Iterable[str] | str | None = None) -> list[dict]:
    if not data:
        return data
    elif not values:
        raise IndexError("Values must be defined")

    if isinstance(columns, str):
        columns = set(columns)
    if isinstance(values, str):
        values = set(values)

    if not isinstance(columns, set):
        columns = set(columns) if columns else set()
    if not isinstance(values, set):
        values = set(values) if values else set()

    total = columns.union(values)
    keys = set(data[0].keys())

    if not total.issubset(keys):
        raise IndexError("Columns & Values {0} <> {1} Data Keys".format(total, keys))

    columns.update(keys.difference(total))
    columns = list(columns)
    values = list(values)

    new_data = defaultdict(list)
    for row in data:
        new_col = []
        for col in columns:
            new_col.append(row[col])

        new_val = []
        for val in values:
            new_val.append(row[val])

        new_data[tuple(new_col)].append(new_val)

    data = []
    for row in new_data:
        new_row = {}
        for i in range(len(columns)):
            new_row[columns[i]] = row[i]

        for i in range(len(values)):
            new_row[values[i]] = new_data[row][i]

        data.append(new_row)

    return data
