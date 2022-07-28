# Monkeypox Data/Forecasting Repository

The aim of this reposutory is to collected time stamped survillance data on the 2022 monkeypox (MPX) outbreak to train computational models that generate probabilistic forecasts. 

## ./data folder
The data folder contains three files: cdc.csv, ecdc.csv, and mpx_cdc_and_ecdc.csv. 
The **cdc.csv** dataset contains

| Column      | Description |
| ----------- | ----------- |
| time_stamp      | The year, month, and day corresponding to the number of cases recorded by the CDC surveillance system |
| snap_shot       | The time that the CDC website was accessed |
| State           | The full state name |
| Abbr            | The abbreviated state name (or Non U.S. resident in the U.S.) |
| Cases           | The number of confirmed cases of MPX |
| Range           | TBD |


The **ecdc.csv** dataset contains
| Column      | Description |
| ----------- | ----------- |
| DateRep     | The year, month, and day corresponding to the number of cases recorded by the CDC surveillance system |
| snap_shot   | The time that the CDC website was accessed |
| CountryExp  | The full country name |
| CountryCode | The abbreviated country name |
| Source      | Whether the data was collected from TESSy or EI |
| ConfCases   | The number of confirmed cases of MPX |



