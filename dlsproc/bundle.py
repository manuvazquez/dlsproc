# AUTOGENERATED! DO NOT EDIT! File to edit: 20_bundle.ipynb (unless otherwise specified).

__all__ = ['read_zip']

# Cell
import pathlib
import zipfile

import pandas as pd

import dlsproc.xml

# Cell
def read_zip(
    input_file: str | pathlib.Path, concatenate: bool = False, return_filenames: bool = False
) -> list | pd.DataFrame | tuple[list, list] | tuple[pd.DataFrame, list]:
    """
    Reads and parses an XML file into a `pd.DataFrame`.

    **Parameters**

    - input_file: str or Path

        Input file.

    - concatenate: bool

        Whether or not to concatenate all the files in a single `pd.DataFrame`.

    - return_filenames: bool

        Whether or not names of the files (read) within the zip are returned.

    **Returns**

    - out: pd.DataFrame

        A Pandas DataFrame with XML data.

    """

    dfs = []

    # zip file is opened
    with zipfile.ZipFile(input_file) as zip_file:

        # for the sake of convenience
        filenames = zip_file.namelist()

        # every file within it...
        for name in filenames:

            # ...is opened...
            with zip_file.open(name) as f:

                # ...and processed
                dfs.append(dlsproc.xml.to_curated_df(f))


    if concatenate:

        dfs = pd.concat(dfs, keys=filenames, names=['file name', 'entry'])

    if return_filenames:

        return dfs, filenames

    else:

        return dfs