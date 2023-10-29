import logging
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        default="WARNING",
    )

    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")
    parser.add_argument("vendor", help="Vendor data file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    output_path = Path(args.output)

    logger.info(f"Reading vendor file `{args.vendor}`")
    df_vendor = pd.read_csv(args.vendor, header=0, dtype={"fips": str, "cofips": str})

    # Note that we are not using any weights here. These probably should
    # be population weighted and use statsmodels.stats.weightstats.DescrStatsW
    # or similar. We should make that change if we want to use these numbers
    # for anything but the coarsest of manual examination.
    df_summary = (
        df_vendor.groupby("cofips")[
            ["filing_rate", "threatened_rate", "judgement_rate"]
        ]
        .describe()
        .stack()
        .reset_index()
        .rename(columns={"level_1": "statistic"})
    )

    output_path.parent.mkdir(exist_ok=True)
    df_summary.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
