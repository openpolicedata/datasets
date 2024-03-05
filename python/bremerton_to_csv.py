import pandas as pd
import os
import re

# April 2017 (PDF) file from http://www.bremertonwa.gov/DocumentCenter/Index/380 converted from PDF to CSV using online tool
file = os.path.join('raw','Bremerton-April-2017-Stats.csv')
df = pd.read_csv(file)
tables = ['ARRESTS','CITATIONS','INCIDENTS']
columns = [['DATE','TIME','CHARGE','RACE','SEX','STREET'],
            ['DATE','CHARGE','RACE','SEX','STREET'],
            ['DATE','TIME','INCIDENT','OFFENSE','STREET']]

p = [r'^\s*(?P<DATE>\d{1,2}/\d{1,2}/\d{2})' +\
        r'\s+(?P<TIME>\d{4})' +\
        r'\s+(?P<CHARGE>.+)' +\
        r'\s+(?P<RACE>[WBAUI])' +\
        r'\s+(?P<SEX>[MF])' +\
        r'\s+(?P<STREET>.+)$',
     r'^\s*(?P<DATE>\d{1,2}/\d{1,2}/\d{2})' +\
        r'\s+(?P<CHARGE>.+)' +\
        r'\s+(?P<RACE>[WBAUI])' +\
        r'\s+(?P<SEX>[MF])' +\
        r'\s+(?P<STREET>.+)$',
    r'^\s*(?P<DATE>\d{1,2}/\d{1,2}/\d{2})' +\
        r'\s+(?P<TIME>\d{4})' +\
        r'\s+(?P<INCIDENT>B17\d+)' +\
        r'\s+(?P<OFFENSE>.+)' +\
        r'\s{3,}(?P<STREET>.+)$']

p_incident2 = r'^\s*(?P<DATE>\d{1,2}/\d{1,2}/\d{2})' +\
        r'\s+(?P<TIME>\d{4})' +\
        r'\s+(?P<INCIDENT>B17\d+)' +\
        r'\s+(?P<OFFENSE>.+)$'

ptable = 'APRIL 2017 (?P<table>[A-Z]+)'
data = {}
for j,t in enumerate(tables):
    data[t] = {k:[] for k in columns[j]}
p = {k:v for k,v in zip(tables,p)}
table = 'ARRESTS'
for x in df.iloc[:,0]:
    if pd.isnull(x) or re.search('^\s+$',x):
        continue
    if m:=re.search(ptable, x):
        table = m.group('table')
    elif not x.startswith('DATE') and not 'APRIL 2017 ARRESTS' in x and not x.isdigit():
        if m:=re.search(p[table], x, re.IGNORECASE):
            for c in data[table].keys():
                data[table][c].append(m.group(c).strip())
        elif table=='INCIDENTS' and (m:=re.search(p_incident2, x)) and x.endswith('VEHICLE'):
            for c in data[table].keys():
                if c!='STREET':
                    data[table][c].append(m.group(c).strip())
                else:
                    data[table][c].append("")
        else:
            raise ValueError(f"Unknown pattern {x}")

for t in tables:
    out_file = os.path.join('.','data',f"Washington_Bremerton_{t}_April_2017.csv")
    df = pd.DataFrame(data[t])
    df.to_csv(out_file, index=False)