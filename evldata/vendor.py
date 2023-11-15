import numpy as np
import pandas as pd


def read_vendor_file(vendor_file: str) -> pd.DataFrame:
    """
    Read and clean the vendor file.

    There are two slightly different formats, one with and `id` column
    and one with a `cofips` column. This method handles either and returns
    a dataframe with a `cofips` in either case.
    """

    df_vendor = pd.read_csv(
        vendor_file,
        header=0,
        dtype={"year": int, "fips": str, "cofips": str, "id": str},
    )

    # Does it have an `id` instead of a `cofips`? If so, extract cofips.
    if "id" in df_vendor.columns and "cofips" not in df_vendor.columns:
        # The two downloads have slightly different columns. In the
        # file with all observed data, fips is id and cofips is encoded
        # in id.
        df_vendor["fips"] = df_vendor["id"]
        df_vendor["cofips"] = df_vendor["id"].str[:5]

        # There are some Inf's in the input.
        df_vendor.replace([np.inf, -np.inf], np.nan, inplace=True)

    # There are some rows in the vendor file where there is no useful
    # information for us.
    df_vendor.dropna(
        subset=["filing_rate", "threatened_rate", "judgement_rate"], inplace=True
    )

    return df_vendor
