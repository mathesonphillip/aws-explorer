from datetime import datetime
from typing import Any, Dict, Iterator, List

import pandas as pd
from deepmerge import always_merger  # type: ignore

from .account import Account
from .utils import remove_timezones_from_object


class Accounts:
    """This class is used to manage a collection of AWS accounts."""

    def __init__(self, accounts: List[Account]) -> None:
        self.accounts = accounts

    def __iter__(self) -> Iterator[Account]:
        self.index: int = 0
        return self

    def __next__(self) -> Account:
        if self.index < len(self.accounts):
            result = self.accounts[self.index]
            self.index += 1
            return result
        raise StopIteration

    # ---------------------------------------------------------------------------- #

    def export(self, export_path="."):
        data_dict: Dict | List = {}
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

                    column_settings = [{"header": column} for column in df.columns]
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
                    # for column in df:
                    #     column_length = max(df[column].astype(str).map(len).max(), len(column))
                    #     col_idx = df.columns.get_loc(column)
                    #     writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    def get_filename(self, prefix: str, extension: str) -> str:
        """This function is used to get the filename."""
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{prefix}_aws_inventory_{timestamp}.{extension}"
