#! /usr/bin/env python
from rich import print
from rich.columns import Columns
from rich.panel import Panel


items = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

columns = Columns(
    [Panel(item) for item in items],
    equal=True,
    expand=True,
)

print(columns)
