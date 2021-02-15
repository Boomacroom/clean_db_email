'''
A client had an email field and didn't do much in the way of sanitizing data in the past
They also didn't do any data validation on the field.
Returning a DB query for COMPANY and with EMAIL, the following would return

COMPANY         EMAIL
Test Company    1@abc.com; 2@abc.com;
Test Company 2  2@abc.com/3@abc.com/person@company.com

Employees in the past used whatever delimeter they liked sometimes a / sometimes //
and sometimes just a space. I wrote this to help separate out the emails while retaining
the COMPANY name for each email.

Adapted from an answer on Stack Overflow that I can't seem to locate anymore.
'''

import pandas as pd
import os, glob
import numpy as np

def extractEmails(df, lst_cols, fill_value='', preserve_index=False):
    # make sure `lst_cols` is list-alike
    if (lst_cols is not None
        and len(lst_cols) > 0
        and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series))):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    # preserve original index values
    idx = np.repeat(df.index.values, lens)
    # create "exploded" DF
    res = (pd.DataFrame({
                col:np.repeat(df[col].values, lens)
                for col in idx_cols},
                index=idx)
             .assign(**{col:np.concatenate(df.loc[lens>0, col].values)
                            for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens==0, idx_cols], sort=False)
                  .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:        
        res = res.reset_index(drop=True)
    return res

# read in csv
df = pd.read_csv("themall.csv")
# Set all possible delimiters - Each one of these was found to have
# been found used in the actual database.
delimiters = ['; ', ';', ':', '/////', '////', '///', '//', '/', ' ']

for delimiter in delimiters:
    df = extractEmails(df.assign(EMAIL=df.EMAIL.str.split(delimiter)), 'EMAIL')
df.to_csv('themall.csv', index=False)
