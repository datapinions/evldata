import logging
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

import censusdis.data as ced
from censusdis.datasets import ACS5
from censusdis.states import ALL_STATES_AND_DC

import evldata.variables as var

logger = logging.getLogger(__name__)


dataset = ACS5


def data_for_year(year: int):
    logger.info(f"Loading {year}")

    # Get all the leaf populations from the race and
    # ethnicity table and also get the total variable.
    leaves_of_group = var.GROUP_HISPANIC_OR_LATINO_ORIGIN_BY_RACE
    variables = [
                    var.MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS,
                    var.VARIABLE_TOTAL_POPULATION,
                    var.TOTAL_HISPANIC_OR_LATINO,
                    var.VARIABLE_TOTAL_RENTERS,
                ] + var.VARIABLES_FOR_RENTERS

    df = ced.download(
        dataset,
        year,
        download_variables=variables,
        leaves_of_group=leaves_of_group,
        state=ALL_STATES_AND_DC,
        county="*",
        tract="*",
    )

    df['year'] = year

    # Filter out the individual race counts under
    # the Hispanic and Latino side of the tree.
    df = df[
        ["year", "STATE", "COUNTY", "TRACT", var.MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS]
        + [col for col in df.columns if col <= var.TOTAL_HISPANIC_OR_LATINO]
        + [var.VARIABLE_TOTAL_RENTERS]
        + var.VARIABLES_FOR_RENTERS
        ]

    return df


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        default="WARNING",
    )

    parser.add_argument("--vendor", required=True, help="Vendor data file.")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    output_path = Path(args.output)

    logger.info(f"Reading vendor file `{args.vendor}`")
    df_vendor = pd.read_csv(args.vendor, header=0, dtype={"fips": str, "cofips": str})

    # Data only goes back to 2009.
    min_year = max(2009, df_vendor['year'].min())
    max_year = df_vendor['year'].max()

    logger.info(f"Loading census data from {min_year} to {max_year}")

    df = pd.concat(
        data_for_year(year) for year in range(min_year, max_year + 1)
    )

    output_path.parent.mkdir(exist_ok=True)

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
