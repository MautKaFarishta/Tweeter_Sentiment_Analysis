import path as p
import pandas as pd

data = pd.read_csv(p.URL_path, sep=" ", header=None)
data.reset_index(drop=True, inplace=True)
print(str(data[0]))

with open (p.URL_path, "r") as myfile:
    dta = myfile.read()
print('data_',dta.strip(),'_')
print(dta == 'https://twitter.com/MSGKiJaan1/status/1399540025562255365')