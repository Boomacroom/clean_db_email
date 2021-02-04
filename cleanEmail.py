'''
A client had an email field and didn't do much in the way of sanitizing data in the past
They also didn't do any data validation on the field.
Returning a DB query for COMPANY and with EMAIL, variations of the following
would be returned.

COMPANY         EMAIL
Test Company    1@abc.com; 2@abc.com; 3@abc.com
Test Company 2  1@cba.com/2@cba.com/3@cba.com
Test Company 3  1@bcd.com//2@bcd.com//3@bcd.com


Employees in the past used whatever delimiter they liked sometimes a / sometimes //
and sometimes just a space. I wrote this to help separate out the emails while retaining
the COMPANY name for each email.
'''
import pandas as pd

# creating a data frame from CSV where the CSV
# is a result of a db query returning COMPANY and EMAIL
df = pd.read_csv("themall.csv") 

# Split all by ;
df2 = pd.concat([pd.Series(row['COMPANY'], row['EMAIL'].split(';'))
    for _, row in df.iterrows()]).reset_index()

# Split by /// We start with the largest amount of /// and work our way down
# to prevent it splitting where it shouldn't turning // into / for example

df2 = pd.concat([pd.Series(row['COMPANY'], row['EMAIL'].split('///'))
    for _, row in df.iterrows()]).reset_index()

# Split all by //
df2 = pd.concat([pd.Series(row['COMPANY'], row['EMAIL'].split('//'))
    for _, row in df.iterrows()]).reset_index()

# Split all by '/'
df2 = pd.concat([pd.Series(row['COMPANY'], row['EMAIL'].split('/'))
    for _, row in df.iterrows()]).reset_index()

# Split all by SPACE
df2 = pd.concat([pd.Series(row['COMPANY'], row['EMAIL'].split(' '))
    for _, row in df.iterrows()]).reset_index()
    
#Write everything back to a CSV as export.
df2.to_csv('themallall.csv', index=False)
