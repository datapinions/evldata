
PYTHON = python3.11
LOGLEVEL = INFO

# The data directory
DATA_DIR := ./data

# A working directory
WORKING_DIR := ./working

# The vendor data published by the Eviction Lab at Princeton.
# See details at https://data-downloads.evictionlab.org/#data-for-analysis/.
EVL_TRACT_PROP_ONLY_DATA := $(DATA_DIR)/tract_proprietary_valid_2000_2018.csv
EVL_TRACT_PROP_ONLY_DATA_URL := https://eviction-lab-data-downloads.s3.amazonaws.com/data-for-analysis/tract_proprietary_valid_2000_2018.csv

EVL_TRACT_DATA := $(DATA_DIR)/tract_proprietary_2000_2018.csv
EVL_TRACT_DATA_URL := https://eviction-lab-data-downloads.s3.amazonaws.com/estimating-eviction-prevalance-across-us/tract_proprietary_2000_2018.csv

# The census data we want to join with the Eviction Lab data.
CENSUS_DATA := $(DATA_DIR)/acs5-data.csv

# Summary stats for the EVL data.
EVL_PROPRIETARY_SUMMARY := $(WORKING_DIR)/evl-proprietary-summary.csv
EVL_OBSERVED_SUMMARY := $(WORKING_DIR)/evl-observed-summary.csv

# Dataset of vendor data joined with census data.
JOINED_DATA := $(DATA_DIR)/evl_census.csv

# List of the counties with the most data.
MOST_DATA := $(DATA_DIR)/most_data.csv

TOP_N := 500

.PHONY: all clean monthly

all: $(EVL_PROPRIETARY_SUMMARY) $(EVL_OBSERVED_SUMMARY) $(JOINED_DATA) $(MOST_DATA)

clean:
	rm -rf $(DATA_DIR)

$(EVL_TRACT_PROP_ONLY_DATA):
	mkdir -p $(@D)
	curl -s -o $@ $(EVL_TRACT_PROP_ONLY_DATA_URL)

$(EVL_TRACT_DATA):
	mkdir -p $(@D)
	curl -s -o $@ $(EVL_TRACT_DATA_URL)

$(CENSUS_DATA): $(EVL_TRACT_PROP_ONLY_DATA)
	$(PYTHON) -m evldata.getcensus --log $(LOGLEVEL) --vendor $(EVL_TRACT_PROP_ONLY_DATA) -o $@

$(EVL_PROPRIETARY_SUMMARY): $(EVL_TRACT_PROP_ONLY_DATA)
	$(PYTHON) -m evldata.summarize -o $@ $^

$(EVL_OBSERVED_SUMMARY): $(EVL_TRACT_DATA)
	$(PYTHON) -m evldata.summarize -o $@ $^

$(JOINED_DATA): $(EVL_TRACT_DATA) $(CENSUS_DATA)
	$(PYTHON) -m evldata.join --vendor $(EVL_TRACT_DATA) --census $(CENSUS_DATA) -o $@

$(MOST_DATA): $(JOINED_DATA)
	$(PYTHON) -m evldata.top -n $(TOP_N) -o $@ $<

# A rule to make requirements.txt. Not part of the normal data build
# process, but useful for maintenance if we add or update dependencies.
requirements.txt: pyproject.toml poetry.lock
	poetry export --without-hashes --format=requirements.txt > $@
