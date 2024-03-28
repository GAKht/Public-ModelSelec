# Model-Selec

The *modelselec* package is designed to facilitate model development and selection.

## Components

- db: includes a class which imports a historical database (saved as a .parquet or .csv file), stores it as a pandas dataframe, stores descriptive summaries by variable type as attributes and provides useful methods useful for dataframe manipulation
- eda: includes several functions useful for exploratory data analysis
- util: includes several function useful for data processing and the reporting of performance metrics

## Unit-tests

Unit tests for each function is included in the *tests* folder.