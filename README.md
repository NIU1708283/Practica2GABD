# GABD Practical 2 - Massive Data Management and Query Optimization

This repository contains the practical materials for a database assignment focused on large-scale data import, Oracle database management, and query optimization. The objective is to import datasets from the UCI repository, store their results in a database, and analyze the impact of indexes on query performance.

## Overview

The assignment focuses on the following topics:

- bulk import of machine learning datasets into Oracle using Python
- storage of experiment results in a relational database
- creation and evaluation of indexes
- query performance analysis and optimization
- comparison of query execution plans with and without indexes

The repository includes notebooks, SQL scripts, and support files for performing the required work.

## Repository structure

```text
Practica2GABD/
├── LICENSE
├── README.md
├── UCIExperimentDB.sql
├── scripts/
│   ├── Creacio_usuaris_ex1.sql
│   └── README.md
├── src/
│   ├── environment.yml
│   ├── insertData.ipynb
│   ├── requirements.txt
│   └── testUCI.ipynb
├── test/
│   ├── __init__.py
│   ├── reporting.py
│   ├── test_db.py
│   ├── utils.py
│   └── ...
└── ...
```

## Main objective

The project aims to teach how to:

- import large datasets into a relational database
- organize experiment metadata and model metrics in tables
- create and remove indexes according to query patterns
- measure the effect of indexes on execution time and efficiency
- decide when indexing is useful and when it may be unnecessary or harmful

## Data loading workflow

The notebook `src/insertData.ipynb` is used to import data from the UCI Machine Learning Repository, including datasets such as:

- Iris
- Ionosphere
- Breast Cancer
- Letter Recognition

The required insertion function is intended to be implemented as:

```python
insertVectorDataset(dbConn, nameDataset: str, *args, **kwargs) -> bool
```

This function is responsible for loading the dataset into the database and preparing the information needed for future analysis.

## Experiment storage

The notebook `src/testUCI.ipynb` is used to test and validate experiment result insertion. The assignment expects the implementation of a procedure that stores experiment metadata and evaluation metrics in the database, such as:

```python
resultat = cursor.callfunc("insertExperiment", bool, [dataset,
                                                      nom_curt,
                                                      nom_classificador,
                                                      iteracio,
                                                      var,
                                                      data_experiment,
                                                      f1_score,
                                                      accuracy])
```

This allows the project to store repeated experimental runs and compare different models or configurations.

## Database schema

The file `UCIExperimentDB.sql` contains the SQL definitions required to create the database structure used by the assignment. It defines the tables necessary for storing imported data and experiment results.

## Scripts and support files

The `scripts/` folder includes SQL helper scripts used during the practical, such as user creation and environment setup. The accompanying `scripts/README.md` summarizes the role of each script.

## Testing and validation

The `test/` folder contains Python utilities that help validate the correctness of the database operations and report execution results. These include:

- `test_db.py`
- `utils.py`
- `reporting.py`

These files support the verification of the database state and provide a simple reporting layer for execution outcomes.

## Technologies used

- Python
- Oracle Database
- SQL
- Jupyter Notebook
- UCI dataset package (`ucimlrepo`)
- pytest-style validation utilities

## Environment requirements

To run the project correctly, you need:

- Oracle database access
- Python environment configured with the dependencies from `src/requirements.yml` / `requirements.txt`
- SQL Developer or another SQL client
- SSH access to the lab environment if using the course infrastructure
- an IDE such as PyCharm for editing notebooks and Python scripts

## Summary

This repository is a practical exercise in large-scale database management and query optimization. It combines Python-based data ingestion, Oracle relational storage, experiment tracking, and index evaluation to teach how database performance changes with data volume and query patterns.
