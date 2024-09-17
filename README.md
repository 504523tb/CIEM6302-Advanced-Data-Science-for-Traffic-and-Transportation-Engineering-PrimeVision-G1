# CIEM6302 Advanced Data Science for Traffic and Transportation Engineering PrimeVision Group 1
 
Main Question: \
How can time-series forecasting methods be used to predict future parcel volume in warehouses?

Subquestions:
1. Which time-series forecasting methods can accurately predict the parcel volume?
2. Which features significantly contribute to the prediction accuracy?

Data
- (Anonymized) parcel volume data with size (width, height, length), weight, destination (country, ZIP), and parcel product (SLA) over time. If possible, we will add anonymized shipping parties.
- Timestamps for previously announced parcels and the time they physically arrived at a facility (Site ID and Site ZIP). 
- Sorting Results at the moment parcels arrive at a physical facility (chute and working shift).

Tech stack
1. Operating systems: Windows
2. Server-Side Programming: Python
3. Cloud platform: AWS
4. Version control: Github
5. Development environment: VS Code, JupyterLab
6. Documentation: Github Wiki

![Adv  Data - Groffe Planning](https://github.com/user-attachments/assets/13ff0390-8764-4d36-8ed0-210bb4971a5c)



Meeting 2 - 17-09-2024 - 13:45-15:30

Agenda
- Meet with PrimeVision
- Revise planning

Meeting Primevision
- Objective:
  - calculate amount of volume per chute
  - chute = output belt, physical location
- Functioning of software:
  - Enter date and give prediction for next two weeks
- Split data per sorting center
- Filter on event type since we need to count them only once
- Implementation
  - First try on python
  - if we have spare time, try to implement in AWS native together with people from PrimeVision
- Data
  - Should be available today

Revise planning
- Read about machine learning techniques
- Take time series into account (trends last period)
  - Otherwise we make prediction for every day of the year
- 

Steps:
1. Import and load data
2. Clean data
3. Visualize data
4. Remove outliers + add extra features
5. Advanced data analysis
   - Predict correlations using linear regression
   - Cluster analysis
6. Split train, test and validation set
7. Normalize data
8. Simple Neural Network
9. LSTM / deep Neural Network
10. Analyze results



Meeting 1 - 10-09-2024 - 15:45-17:00

Agenda
- Discuss about backlog

Discuss about backlog
- Create research question + subquestions
- Create sprint planning
- Create backlog
- Teck stack

