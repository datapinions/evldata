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

    parser.add_argument("-n", type=int, default=50, help="Output the top n for this n.")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")
    parser.add_argument("data", type=str, help="Input data file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    n = args.n
    input_path = Path(args.data)
    output_path = Path(args.output)

    logger.info(f"Reading input file `{input_path}`")
    logger.info(f"Writing output file `{output_path}`")

    df = pd.read_csv(
        input_path, header=0, dtype={"STATE": str, "COUNTY": str, "TRACT": str}
    ).rename({"cofips": "COFIPS"}, axis="columns")

    # We don't have ACS5 data to merge with before this,
    # so don't count them.
    df = df[df["year"] >= 2009]

    counts = (
        df.groupby(["COFIPS", "STATE", "COUNTY"])["TRACT"]
        .count()
        .rename("TRACT_COUNT")
        .nlargest(n)
    )

    output_path.parent.mkdir(exist_ok=True)
    counts.to_csv(output_path, index=True)


if __name__ == "__main__":
    main()
