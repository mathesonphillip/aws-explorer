"""This module is used to manage a collection of AWS accounts.
Mainly used so that i could export multiple accounts to a single export.
"""

from datetime import datetime

from collections.abc import Iterator

import pandas as pd
from deepmerge import always_merger  # type: ignore

from .session import Session
from .utils import remove_timezones_from_object


class Sessions:

    """This class is used to manage a collection of AWS accounts."""

    def __init__(self, accounts: list[Session]) -> None:
        self.accounts = accounts

    def __iter__(self) -> Iterator[Session]:
        self.index: int = 0  # pylint: disable=attribute-defined-outside-init
        return self

    def __next__(self) -> Session:
        if self.index < len(self.accounts):
            result = self.accounts[self.index]
            self.index += 1
            return result
        raise StopIteration

    # ---------------------------------------------------------------------------- #

    def export(self, export_path=".") -> None:  # pylint: disable=too-many-locals
        """This method is used to export the accounts to a file.
        All the accounts are merged into a single dictionary and then exported to Excel.

        """
        data_dict: dict | list = {}
        for a in self.accounts:
            # Get the data as a dictionary
            account_data = remove_timezones_from_object(a.to_dict())
            data_dict = always_merger.merge(data_dict, account_data)

        # pylint: disable=abstract-class-instantiated
        with pd.ExcelWriter(path=export_path) as writer:
            # iterate over the top-level keys in the dictionary
            for service_key in data_dict:
                for key, data in data_dict[service_key].items():
                    sheet_name = f"{service_key}.{key}"
                    df = pd.DataFrame(data)
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=1,
                        header=False,
                        index=False,
                    )

                    column_settings: list[dict[str, str]] = [{"header": column} for column in df.columns]
                    print(column_settings)

                    # Add the Excel table structure. Pandas will add the data.
                    worksheet = writer.sheets[sheet_name]
                    worksheet.add_table(
                        0,
                        0,
                        len(df),
                        len(df.columns) - 1,
                        {"name": sheet_name, "columns": column_settings},
                    )

                    # Set the column width to the max length of the column header
                    for column in df:
                        column_length = max(df[column].astype(str).map(len).max(), len(column))  # type: ignore
                        col_idx = df.columns.get_loc(column)
                        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    def get_filename(self, prefix: str, extension: str) -> str:
        """This function is used to get the filename."""
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{prefix}_aws_inventory_{timestamp}.{extension}"
