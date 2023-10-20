
PYTHON = python3.11
LOGLEVEL = INFO

# May want to override these to run for other counties.
# Georgia
STATE := 13
# DeKalb
COUNTY := 089


# The data directory
DATA_DIR := ./data

# Working director, for e.g. params.
WORKING_DIR := ./working

# The vendor data published by the Eviction Lab at Princeton
EVL_VENDOR_DATA := $(DATA_DIR)/tract_proprietary_valid_2000_2018.csv
EVL_VENDOR_DATA_URL := https://eviction-lab-data-downloads.s3.amazonaws.com/data-for-analysis/tract_proprietary_valid_2000_2018.csv

# The census data we want to join with the Eviction Lab data.
CENSUS_DATA := $(DATA_DIR)/acs5-2018.csv

# Dataset of vendor data joined with census data.
JOINED_DATA := $(DATA_DIR)/evl_census.csv

# Just the desired county.
COUNTY_DATA := $(DATA_DIR)/$(STATE)-$(COUNTY).csv

# Parameters
PARAMS_DIR := $(WORKING_DIR)/params/xgb
PARAMS_YAML := $(PARAMS_DIR)/xgb-params-$(STATE)-$(COUNTY).yaml


.PHONY: all clean

all: $(PARAMS_YAML)

clean:
	rm -rf $(DATA_DIR)

$(EVL_VENDOR_DATA):
	mkdir -p $(@D)
	curl -s -o $@ $(EVL_VENDOR_DATA_URL)

$(CENSUS_DATA):
	$(PYTHON) -m evldata.getcensus -o $@

$(JOINED_DATA): $(EVL_VENDOR_DATA) $(CENSUS_DATA)
	$(PYTHON) -m evldata.join --vendor $(EVL_VENDOR_DATA) --census $(CENSUS_DATA) -o $@

$(COUNTY_DATA): $(JOINED_DATA)
	$(PYTHON) -m evldata.select -s $(STATE) -c $(COUNTY) -o $@ $<

$(PARAMS_YAML): $(COUNTY_DATA)
	$(PYTHON) -m evldata.optimize --log $(LOGLEVEL) -o $@ $<
