# Smart Data Analytics, Gruppe 3: Kinemic – Klassifikation von Bewegungsdaten

This repository contains all documents and programs created by group 4 for 
Praktikum Smart Data Analystics, Assignement 3 in Sommersemester 2020.

All scripts are provided in the form of Juypter Notebooks.
Python requirements are listed in requitements.txt. Data is *by each notebook* expected at the relative location ./Csv_data/all.csv.

An overview is given in the presentation slides in this repository as well 
as listed below.

## Contents


### Data Pre-Processing:

Dataframe_preparation.ipynb: Data preprocessing (as provided by TECO/Kinemic)

### Data Exploration:

Exploration.ipynb: Basic data exploration
RTLS_Exploration.ipynb: Further exploration or RTLS sensor data.

### CNNs:

#### Simplenet
simplenet/simplenet\*.ipynb: The Simplenet CNNs based on TECO’s suggested architecture

#### Stacknet
stacknet.ipynb: The Stacknet CNN built of Simplenet layers, to improve on its performance

#### Mutinet

#### Sepnet

#### Deepnet

### RNNs:

#### LSTM

### Random Forest:

random forest/RF\*.ipynb: The Random Forest classifiers applied to the data set

### Other Experiments:

#### Hybridnet

hybridnet.ipynb: An experimental setup combining the classification results of two models, slightly improving performance

### Summary and Further Documents:

slides presentation.pdf: Main presentation slides from July 6th 2020
model performance.xlsx, model performance compact.png: Overview of model performance
