# AUTOGENERATED! DO NOT EDIT! File to edit: 60_assemble.ipynb (unless otherwise specified).

__all__ = ['merge_deleted', 'flatten_columns_names', 'parquet_amenable', 'stack']

# Cell
import pathlib

import pandas as pd
import yaml

import dlsproc.structure
import dlsproc.bundle
import dlsproc.hier
import dlsproc.io

# Cell
def merge_deleted(data_df: pd.DataFrame, deleted_series: pd.Series) -> pd.DataFrame:

    # duplicates are dropped; in order to do so it is convenient to turn the `pd.Series` into a `pd.DataFrame` by calling
    # `reset_index`, which turns the *multiindex* into columns
    deduplicated_deleted_df = deleted_series.reset_index().drop_duplicates('id').set_index(['file name', 'id'])

    # in order to merge this new `pd.DataFrame` with `data_df` we need a *multiindex* for the former with the same number of levels as in the latter
    deduplicated_deleted_df.columns = col_multiindex = pd.MultiIndex.from_tuples([dlsproc.hier.pad_col_levels(data_df, ['deleted_on'])])

    # the `data_df` is (*left*-)joined with the new one yielding deleted entries; the result is a *stateful* `pd.DataFrame` in the sense that,
    # for every entry, we know its state: deleted or not; notice that `data_df`'s index is reset for easying the merge (assuming every contract
    # shows only once in `data_df`, *file name* and *id* should still provide a unique index...though it probably doesn't matter anyway)
    res = data_df.reset_index().set_index(['file name', 'id']).merge(deduplicated_deleted_df, how='left', on=['file name', 'id'])

    return res

# Cell
def flatten_columns_names(df: pd.DataFrame, data_scheme: dict, inplace: bool = False) -> None | pd.DataFrame:

    # the inverse of the above mapping (turning nan's into empty strings, and concatenating all the levels together)
    inv_data_scheme = {''.join([e if pd.notna(e) else '' for e in v]): k for k, v in data_scheme.items()}

    new_names = []
    # unmapped_names = []

    for c in df.columns:

        # print(c)

        stitched_c = ''.join(c)

        # if the columns is found in the inverse mapping...
        if stitched_c in inv_data_scheme:

            # ...the given name is used
            new_names.append(inv_data_scheme[stitched_c])

        # if the columns is NOT found in the inverse mapping...
        else:

            # ...the new name is obtained by contatenating the individual components
            new_names.append(dlsproc.structure.nested_tags_separator.join([e for e in c if e != '']))

            # # it is also recorded in its own list
            # unmapped_names.append(new_names[-1])

    if inplace:

       res = df

    else:

        res = df.copy()

    res.columns = new_names

    # print(f'Unmapped columns:\n{unmapped_names}')

    return res

# Cell
def parquet_amenable(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:

    if inplace:

        res = df

    else:

        res = df.copy()

    # 1: every element in a multivalued column must be a list (maybe with a single element)
    res = dlsproc.io.homogenize_multivalued(res)

    # a list with the names of columns that are *multivalued*
    multivalued_columns = dlsproc.structure.multivalued_columns(res)

    # 2: the same type is enforced in all the `list`s (across rows and columns) in *multivalued* columns
    res[multivalued_columns] = res[multivalued_columns].applymap(dlsproc.io.cast_list_to_floats_or_strs)

    # 3: the same type for the elements in the list is enforced across every **individual** multivalued column
    res[multivalued_columns] = res[multivalued_columns].apply(dlsproc.io.cast_multivalued_series_to_common_type, axis='index')

    return res

# Cell
def stack(top_df: pd.DataFrame, bottom_df: pd.DataFrame) -> pd.DataFrame:

    assert top_df.index.names == bottom_df.index.names, 'dataframes are expected to have indexes with the same names'

    # if we have different number of levels in the dataframes...
    if top_df.columns.nlevels != bottom_df.columns.nlevels:

        if top_df.columns.nlevels < bottom_df.columns.nlevels:

            to_be_fixed_df = top_df

            res_n_levels = bottom_df.columns.nlevels

        else:

            to_be_fixed_df = bottom_df

            res_n_levels = top_df.columns.nlevels

        new_names = []

        for c in to_be_fixed_df.columns:

            new_names.append(c + ('',) * (res_n_levels - to_be_fixed_df.columns.nlevels))

        to_be_fixed_df.columns = pd.MultiIndex.from_tuples(new_names)

    return pd.concat((top_df, bottom_df), axis=0)