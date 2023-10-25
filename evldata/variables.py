# From the population by race group https://api.census.gov/data/2018/acs/acs5/groups/B03002.html
GROUP_HISPANIC_OR_LATINO_ORIGIN_BY_RACE = "B03002"

# TODO: Consider shifting to B25003[A-I]_003E to get renter households
# by race and compute fractions from those instead of overall population.
# https://api.census.gov/data/2017/acs/acs5/groups/B25003A.html through
# https://api.census.gov/data/2017/acs/acs5/groups/B25003I.html.

TOTAL_POPULATION = "B03002_001E"
TOTAL_HISPANIC_OR_LATINO = "B03002_012E"

# From income by tenure group https://api.census.gov/data/2018/acs/acs5/groups/B25119.html
GROUP_MEDIAN_HOUSEHOLD_INCOME_BY_TENURE = "B25119"

MEDIAN_HOUSEHOLD_INCOME_FOR_RENTERS = "B25119_003E"
