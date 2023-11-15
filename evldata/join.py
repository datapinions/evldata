import logging
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

import evldata.variables as var
from evldata.vendor import read_vendor_file

logger = logging.getLogger(__name__)


YEAR_TO_2018_DOLLARS = {
    2009: 1.17322335,
    2010: 1.15418227,
    2011: 1.11891074,
    2012: 1.09570370,
    2013: 1.07970803,
    2014: 1.06172840,
    2015: 1.05990255,
    2016: 1.04640634,
    2017: 1.02437673,
    2018: 1.00000000,
}
"""
Map from year dollars to 2018 dollars.

For example, One dollar in 2009 buys the same
amount as $1.17 in 2018.

Data derived from https://www2.census.gov/programs-surveys/demo/tables/p60/276/R_CPI_U_RS.xlsx
"""


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        default="WARNING",
    )

    parser.add_argument("--census", required=True, help="Census data file.")
    parser.add_argument("--vendor", required=True, help="Vendor data file.")

    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    output_path = Path(args.output)

    logger.info(f"Reading census file `{args.census}`")
    df_census = pd.read_csv(
        args.census, header=0, dtype={"STATE": str, "COUNTY": str, "TRACT": str}
    )

    logger.info(f"Reading vendor file `{args.vendor}`")

    df_vendor = read_vendor_file(args.vendor)

    # Split up the fips in the vendor file.
    df_vendor["STATE"] = df_vendor["fips"].apply(lambda fips: fips[:2])
    df_vendor["COUNTY"] = df_vendor["fips"].apply(lambda fips: fips[2:5])
    df_vendor["TRACT"] = df_vendor["fips"].apply(lambda fips: fips[5:])

    # Merge the two.
    df_merged = df_vendor.merge(
        df_census,
        on=["year", "STATE", "COUNTY", "TRACT"],
    )

    df_merged = df_merged[
        ["STATE", "COUNTY", "TRACT", "year"]
        + [
            col
            for col in df_merged.columns
            if col not in ["STATE", "COUNTY", "TRACT", "year"]
        ]
    ]

    # Adjust income for inflation.
    df_merged[f"{var.MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS}_2018"] = df_merged[
        ["year", var.MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS]
    ].apply(
        lambda row: row[var.MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS]
        * YEAR_TO_2018_DOLLARS[row["year"]],
        axis=1,
    )

    # Now construct the fractions.

    for variable in df_census.columns:
        if (
            variable.startswith(var.GROUP_POPULATION)
            and variable != var.VARIABLE_TOTAL_POPULATION
        ):
            df_merged[f"frac_{variable}"] = (
                df_merged[variable] / df_merged[var.VARIABLE_TOTAL_POPULATION]
            )
        elif variable in var.VARIABLES_FOR_RENTERS:
            df_merged[f"frac_{variable}"] = (
                df_merged[variable] / df_merged[var.VARIABLE_TOTAL_RENTERS]
            )

    output_path.parent.mkdir(exist_ok=True)
    df_merged.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
