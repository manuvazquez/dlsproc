# AUTOGENERATED! DO NOT EDIT! File to edit: 50_parse.ipynb (unless otherwise specified).

__all__ = ['domain_discriminative_columns_paths', 'domain']

# Cell
import pathlib
import urllib.parse

import pandas as pd

import dlsproc.xml
import dlsproc.hier

# Cell
domain_discriminative_columns_paths = [
    ['ContractFolderStatus', 'LocatedContractingParty', 'BuyerProfileURIID'],
    ['ContractFolderStatus', 'LegalDocumentReference', 'Attachment', 'ExternalReference', 'URI']
]

# Cell
def domain(df: pd.DataFrame) -> pd.Series:

    # columns names from "path"s
    columns = [dlsproc.hier.pad_col_levels(df, p) for p in domain_discriminative_columns_paths]

    domains = df[columns].applymap(lambda x: urllib.parse.urlparse(x).netloc if pd.notna(x) else pd.NA)

    # the result is initialized with the first column of domains...
    res = domains[columns[0]]

    # ...and  the remaining...
    for c in columns[1:]:

        # ...are used to update it
        res = res.combine_first(domains[c])

    return res