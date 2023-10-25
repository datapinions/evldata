
PYTHON = python3.11
LOGLEVEL = INFO

# The data directory
DATA_DIR := ./data

# The vendor data published by the Eviction Lab at Princeton
EVL_VENDOR_DATA := $(DATA_DIR)/tract_proprietary_valid_2000_2018.csv
EVL_VENDOR_DATA_URL := https://eviction-lab-data-downloads.s3.amazonaws.com/data-for-analysis/tract_proprietary_valid_2000_2018.csv

# The census data we want to join with the Eviction Lab data.
CENSUS_DATA := $(DATA_DIR)/acs5-2018.csv

# Dataset of vendor data joined with census data.
JOINED_DATA := $(DATA_DIR)/evl_census.csv

# List of the counties with the most data.
MOST_DATA := $(DATA_DIR)/most_data.csv

TOP_N := 100

.PHONY: all clean

all: $(JOINED_DATA) $(MOST_DATA)

clean:
	rm -rf $(DATA_DIR)

$(EVL_VENDOR_DATA):
	mkdir -p $(@D)
	curl -s -o $@ $(EVL_VENDOR_DATA_URL)

$(CENSUS_DATA):
	$(PYTHON) -m evldata.getcensus -o $@

$(JOINED_DATA): $(EVL_VENDOR_DATA) $(CENSUS_DATA)
	$(PYTHON) -m evldata.join --vendor $(EVL_VENDOR_DATA) --census $(CENSUS_DATA) -o $@

$(MOST_DATA): $(JOINED_DATA)
	$(PYTHON) -m evldata.top -n $(TOP_N) -o $@ $<
