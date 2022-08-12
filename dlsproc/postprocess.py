# AUTOGENERATED! DO NOT EDIT! File to edit: 15_postprocess.ipynb (unless otherwise specified).

__all__ = ['str_columns', 'assembled_str_columns', 'typecast_columns', 'keep_updates_only',
           'deduplicate_deleted_series']

# Cell
import pathlib

import pandas as pd

import dlsproc.structure

# Cell
str_columns = [['ContractFolderStatus', 'LocatedContractingParty', 'Party', 'PostalAddress', 'PostalZone']]

# Cell
assembled_str_columns = [dlsproc.structure.assemble_name(c) for c in str_columns]

# Cell
def typecast_columns(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Tidy up the `pd.DataFrame` returned by `to_df`.

    **Parameters**

    - input_df: pd.DataFrame

        Input DataFrame as ready by `to_df`.

    **Returns**

    - out: pd.DataFrame

        Post-processed DataFrame.

    """

    res = input_df.copy()

    processed_columns = []

    # ------------ ContractFolderStatus - TenderingProcess - TenderSubmissionDeadlinePeriod ------------

    new_column = dlsproc.structure.assemble_name(['ContractFolderStatus', 'TenderingProcess', 'TenderSubmissionDeadlinePeriod'])

    # we don't want to inadvertently overwrite an existing column
    assert new_column not in res

    res[new_column] = pd.to_datetime(
        input_df[dlsproc.structure.assemble_name(['ContractFolderStatus', 'TenderingProcess','TenderSubmissionDeadlinePeriod','EndDate'])]
        + 'T' +
        input_df[dlsproc.structure.assemble_name(['ContractFolderStatus', 'TenderingProcess','TenderSubmissionDeadlinePeriod','EndTime'])],
        format='%Y-%m-%dT%H:%M:%S', utc=True, errors='coerce'
    )

    processed_columns.append(new_column)

    # NOTE: one could also delete the original columns being parsed, but they might be useful if errors happen during conversion (`errors=coerce`)

    # -------------------------------------------- updated ---------------------------------------------

    res['updated'] = pd.to_datetime(input_df['updated'], format='%Y-%m-%dT%H:%M:%S.%f%z', utc=True)

    processed_columns.append('updated')

    # ---------------------------------------- string columns ------------------------------------------

    for c in assembled_str_columns:

        if c in res:

            res[c] = res[c].astype(pd.StringDtype())

            processed_columns.append(c)

    # --------------------------------------- everything else ------------------------------------------

    for c in res.columns:

        # if this column has already been processed...
        if c in processed_columns:

            continue

        # if this column is *multivalued*...
        if dlsproc.structure.is_multivalued(res[c]):

            continue

        # an attempt is made...
        try:

            # to interpret every column as a (float) number
            res[c] = res[c].astype(float)


        # if conversion to float is not feasible...
        except (TypeError, ValueError):

            # ...the column is taken to be one of strings
            res[c] = res[c].astype(pd.StringDtype())

    return res

# Cell
def keep_updates_only(df: pd.DataFrame) -> pd.DataFrame:

    grouped = df.sort_values('updated').groupby('id')

    return grouped.tail(1)
    # return grouped.last()

# Cell
def deduplicate_deleted_series(series: pd.Series) -> pd.Series:

    # return series.sort_values().groupby(axis=0, level='id', group_keys=False).nlargest(1)
    return series.sort_values().groupby(axis=0, level='id', group_keys=False).nsmallest(1)