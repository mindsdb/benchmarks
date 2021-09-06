**Got from**: https://www.brentozar.com/archive/2020/01/the-2020-data-professional-salary-survey-results-are-in/

# How i get data.csv:
1) download file from link above
2) save it as csv
3) remove first 3 rows
4) run script below. 

**Note**: initially i removed only first group of columns (from 'timestamp' to 'counter'), but when i tried learn predictor on resulted data i got torch error. So i assumed reason is long text columns, therefore removed additional columns from 'OtherDatabases' to 'KindsOfTasksPerformed'.

```
import pandas as pd
import csv

PATH = '2020_Data_Professional_Salary_Survey_Responses.csv'

df = pd.read_csv(PATH, sep='\t', dtype=str)
df = df.drop(columns=['Timestamp', 'PostalCode', 'TelecommuteDaysPerWeek', 'LookingForAnotherJob', 'CareerPlansThisYear', 'Counter', ])
df = df.drop(columns=['OtherDatabases', 'NewestVersionInProduction', 'OldestVersionInProduction', 'OtherJobDuties', 'KindsOfTasksPerformed'])
for column in df.columns:
    df.loc[df[column] == 'Not Asked', column] = ''
    df = df.rename(columns={column: column.strip(' ')})
df['SalaryUSD'] = df['SalaryUSD'].apply(lambda x: x.strip(' ').replace(',',''))
df['Survey Year'] = df['Survey Year'].apply(lambda x: str(int(x)))

df.to_csv('data.csv', index=False)
```
