import httpio
from io import BytesIO
import pandas as pd
from zipfile import ZipFile

url = httpio.open("https://data-openjustice.doj.ca.gov/sites/default/files/dataset/2023-12/RIPA-Stop-Data-2022.zip")
z = ZipFile(url)

df = pd.read_excel(BytesIO(z.read(z.namelist()[0])))

for a in df["AGENCY_NAME"].unique():
    df_out = df[df['AGENCY_NAME']==a]

    df.to_csv(rf'.\data\California_{}_STOPS_2022.csv')