# evldata

The repository contains code to build a dataset of eviction rates,
demographics, and income. The purpose is to demonstrate impact
charts, as implemented in the
[impactchart](https://github.com/vengroff/impactchart)
repository. The code to build impact charts using the data
this repository generates can be found in the 
[evlcharts](https://github.com/vengroff/evlcharts) repository.

## Dependencies 

The key binary requirements for this project are Python 3.11 or
higher and [GNU make](https://www.gnu.org/software/make/). We 
test with Gnu make version
4.4, but other versions may work.

The Python requirements for the project are listed in 
`requirements.txt` and should all be installable in your 
virtual environment via

```shell
pip install -r ./requirements.txt
```

During development we use [poetry](https://python-poetry.org/) to manage dependencies
but we try to always keep the `requirements.txt` up to date.

## Generating the Data Set

The work done by this project is all coordinated through a 
`Makefile`.

The entire dataset can be built with the single command

```shell
gmake
```

If you want to remove the data set and all intermediate files,

```shell
gmake clean
```

will do that for you.

The `Makefile` automates the following steps:

1. Download data on eviction rates from the 
   [Eviction Lab](https://evictionlab.org/)
   at Princeton University. Specifically, it uses what the 
   Eviction Lab calls proprietary data within their 
   [eviction-lab-data-downloads](https://data-downloads.evictionlab.org/#data-for-analysis/) repository.
2. Download demographic and income data from the [U.S. Census](https://www.census.gov/)
   for the years covered by the eviction data.
3. Join the data together at the census tract level. The final
   result has one row per census tract per year. On that row, it
   has all relevant fields from the two downloaded data sets for 
   that tract and year. In cases where data for a given tract for
   a given year is not present in both downloaded data sets, 
   that tract and year combination does not appear in the final
   dataset.
4. Compute inflation-adjusted median renter household income in
   constant 2018 dollars.   
5. Compute fractional values for each of the census demographic fields.
   For example, there is a field [`B25003B_003E`](https://api.census.gov/data/2018/acs/acs5/variables/B25003A_003E.html)
   in the census data that represents a count of the number of renters
   in a tract who identify as white and not Hispanic or Latino.
   We add a field `frac_B25003B_003E` that represents this as 
   a fraction of the total number of renter households. This new
   field is always between 0.0 and 1.0.

Once the `Makefile` has successfully run, the final data set will
be in a file `data/evl_census.csv`. From there, you can either
use it with the code in [evlcharts](https://github.com/vengroff/evlcharts)
or whatever further analysis you wish to do.

## Data Sources

### The Eviction Lab

The data we download from the eviction lab is a file called
`tract_proprietary_valid_2000_2018.csv`. The file, along with
a corresponding codebook can be found at 
https://data-downloads.evictionlab.org/#data-for-analysis/.

The Eviction Lab's preferred citation for this data is

- Gromis, Ashley, Ian Fellows, James R. Hendrickson, Lavar Edmonds, Lillian Leung, Adam Porton, and Matthew Desmond. Estimating Eviction Prevalence across the United States. Princeton University Eviction Lab. https://data-downloads.evictionlab.org/#estimating-eviction-prevalance-across-us/. Deposited May 13, 2022.

### U.S. Census

The groups of variables we use are 
[B25119](https://api.census.gov/data/2018/acs/acs5/groups/B25119.html)
for median household income for renters and 
[B25003](https://api.census.gov/data/2018/acs/acs5/groups/B25003.html) 
and 
[B25003A](https://api.census.gov/data/2018/acs/acs5/groups/B25003A.html) 
through 
[B25003I](https://api.census.gov/data/2018/acs/acs5/groups/B25003I.html) 
for the population of renters overall and renters of different racial 
and ethnic groups.

For total population, not just renters,
we used 
[B03002](https://api.census.gov/data/2018/acs/acs5/groups/B03002.html).
