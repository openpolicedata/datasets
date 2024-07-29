import glob
import pandas as pd
import re

years = []
for t in ['INCIDENTS', 'OFFICERS', 'SUBJECTS']:
    df = []
    cur_years = set()
    for f in glob.glob(rf'.\raw\Texas_Austin_OFFICER-INVOLVED_SHOOTINGS_-_{t}_20*.csv'):
        df.append(pd.read_csv(f))
        cur_years.add(int(re.search('_(20\d\d)\.csv', f).group(1)))

    years.append(cur_years)

    df = pd.concat(df)
    df.to_csv(rf'.\data\Texas_Austin_OFFICER-INVOLVED_SHOOTINGS-{t}.csv')

# Ensure all years read in for each case
for y in years:
    assert y==years[0]