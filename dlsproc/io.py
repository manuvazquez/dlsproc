# AUTOGENERATED! DO NOT EDIT! File to edit: 40_io.ipynb (unless otherwise specified).

__all__ = ['File', 'homogenize_multivalued', 'cast_list_to_floats_or_strs', 'cast_multivalued_series_to_common_type',
           'write', 'read']

# Cell
import pathlib

import pandas as pd
import numpy as np

import dlsproc.xml
import dlsproc.structure

import fastcore.foundation

# Cell
class File:

    def __init__(self, stem: str | pathlib.Path):

        self.name: pathlib.Path = pathlib.Path(stem)

        assert self.name.suffix == '', 'an extension-less file is expected'

        self.name = self.name.with_suffix('.pickle')

    def __str__(self):

        return self.name.as_posix()

    def __repr__(self):

        return self.__str__()

    def exists(self) -> bool:

        return self.name.exists()

# Cell
def _cast_to_list_if_not_already(x) -> list | np.ndarray:

    t = type(x)

    if (t == list) or (t == np.ndarray):

        return x

    else:

        return [x]

# Cell
def homogenize_multivalued(df: pd.DataFrame) -> pd.DataFrame:

    res = df.copy()

    # for every column that is multivalued...
    for col_name in dlsproc.structure.multivalued_columns(res):

        # if the type of an element (index) is list, it's left as it is, otherwise a list is wrapped around it
        # res[col_name] = res[col_name].apply(lambda x: x if type(x) == list else [x])
        res[col_name] = res[col_name].apply(_cast_to_list_if_not_already)

    return res

# Cell
def cast_list_to_floats_or_strs(l: list) -> list:

    # *scalar* Pandas' `pd.NA` are turned into Numpy's `np.nan`
    l = [np.NAN if (type(e) != list) and (pd.isna(e)) else e for e in l]

    try:
        return [float(e) for e in l]

    # `TypeError` most likely means there is (at least) one element that is a list
    except (ValueError, TypeError):
        return [str(e) for e in l]

# Cell
def cast_multivalued_series_to_common_type(s: pd.Series) -> pd.Series:

    types = set(s.apply(lambda x: type(x[0])))

    if len(types) == 1:

        return s.copy()

    elif types == set([float, str]):

        return s.apply(lambda x: [str(e )for e in x])

    else:

        raise Exception("don't know how to handle these types")

# Cell
@fastcore.foundation.patch
def write(self: File, df: pd.DataFrame):

    df.to_pickle(self.name)

# Cell
@fastcore.foundation.patch
def read(self: File) -> pd.DataFrame:

    return pd.read_pickle(self.name)