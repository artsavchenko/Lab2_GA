# Data Analysis from client side

The data was obtained from the [Google Analytics](https://analytics.google.com/) test account.

For the parameters was chosen the average session duration from new users, from users using tablet computers and PC's, from users who use mobile phones. Data was selected for the period from March 1 to April 30, 2019.

To process the data needed such libraries as **csv** and **pandas**.

## Results

We are looking for anomalies that exceeds 98% or was inferior than 2% of values of the other two segments. 

**Conclusions from analysis**
* There are 19 cases for the users who use tablets and PC's with extremely low duration of session in night time (1 a.m - 4 a.m) and extremely high average session duration in the evening time (when people usually came home).
* There are 29 cases for the new users average session duration. Usually that segment of users have their peak activity in the evening, but there are some cases with extremely high average session duration in the night time.  
* There are 211 cases for the users who use mobile phones. Most of that cases shows low users activity at night and evening time. This can be explained by the fact that users coming home are starting to use their PC's instead of phones.

All results for each users segment saved in files: *pc_outliers.csv*, *new_users_outliers.csv*, *mobile_outliers.csv*