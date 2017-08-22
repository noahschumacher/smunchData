# Smunch Data Analysis and Forecasting

## Getting Started

These instructions will detail the contents of this project and and its purpose. It will also explain the methodology behind some of the key files and give instructions to get running locally.

### Overview

This project contains several seperate aspects. Folders:  
* noahapi - Docker Image predicts amount of orders on any given day for a given company. (most important)
* cohorts - Contains two files that produce the retention rate and activity cohorts table
* csvPredictions - Initial trails of predictive alogrithm using the Smunch master excel sheet (no database query, messy)
* dbPredictions - Predictive files moving to database query, cleaned up and now contains time correction.
* gui_qtApp - Contains attempt at making locally running Desktop UI for predictions. (Started when pruduction to website seemed unsure)
* queries - Contains single run files that query the database (simple information).

A detailed description of the logic behind the prediction is in the overview.pdf file. This was a continuesly updated file that served as a journal for my work (written in latex). Aplogies for any spelling errors and lack of consistent direction in writing. It was a not an edited file but more free flow thinking jotted down. 

### Dependencies
Everything one needs to have in order to run files locally. 
Python Libraries:
* pandas - For data analysis
* numpy - For data analysis
* matplotlib - For presentation
* psycopg2 - For connecting to and querying database

All of these are contained in anaconda.

Other:
* Docker
* postgreSQL


## Authors

* **Noah Schumacher** - *Author* - [Noah Schumacher](https://github.com/noahschumacher)
* **Cyrille Gattiker** - *API / Docker help* - [Cyrille Gattiker](https://bitbucket.org/cyrille-88motors/)



## Acknowledgments

* Advice and collaboration with [Torsten Wetzell](https://github.com/twetzel) (Smunch wed developer)


