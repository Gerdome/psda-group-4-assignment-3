# Smart Data Analytics, Gruppe 3: Kinemic – Klassifikation von Bewegungsdaten

This repository contains all documents and programs created by group 4 for 
Praktikum Smart Data Analystics, Assignement 3 in Sommersemester 2020.

All scripts are provided in the form of Juypter Notebooks.
Python requirements are listed in requitements.txt. Data is *by each notebook* expected at the relative location ./Csv_data/all.csv.

An overview is given in the presentation slides in this repository as well 
as listed below.

## Contents


### Data Pre-Processing:

- Dataframe_preparation.ipynb: Data preprocessing (as provided by TECO/Kinemic)

### Data Exploration:

- exploration/Exploration.ipynb: Basic data exploration
- exploration/RTLS_Exploration.ipynb: Further exploration or RTLS sensor data.

### CNNs:

#### Simplenet

- simplenet/simplenet\*.ipynb: The Simplenet CNNs based on TECO’s suggested architecture

#### Stacknet

- stacknet.ipynb: The Stacknet CNN built of Simplenet layers, to improve on its performance

#### Mutinet

- multinet.ipynb: The Multinet CNN seperating body sensors and RTLS. This notebook is commented and contains the best performing version (M2-25).
- M1, M2, M3: Other versions of the Multinet architecture.
- M2-25 P{1,2,3,4,5}.html: Results for different test proband split.

#### Sepnet

- S1.ipynb: The Sepnet CNN seperating the different sensors. For comments on the pipeline, please look at the multinet notebook.
- S2.ipynb, S3.ipynb: Additional versions of the sepnet architecture.

#### Deepnet

- multinet/deepnet.ipynb: The Deepnet CNN, a deep version of multinet.

### RNNs:

#### LSTM

- LSTM_SeqToOne.ipynb: Sequence to One LSTM architecture.
- LSTM_SeqToSeq.ipynb: Sequence to Sequence LSTM architecture.

### Random Forest:

- random forest/RF\*.ipynb: The Random Forest classifiers applied to the data set

### Other Experiments:

#### Hybridnet

- hybridnet.ipynb: An experimental setup combining the classification results of two models, slightly improving performance

### Summary and Further Documents:

- slides presentation.pdf: Main presentation slides from July 6th 2020
- model performance.xlsx, model performance compact.png: Overview of model performance
