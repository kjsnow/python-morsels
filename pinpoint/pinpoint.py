
import pandas as pd


with open('auto-mpg.data') as file:
    #file.read()
    for line in file:
        print(line)

cols = ['mpg','cylinders','displacement','horsepower','weight','acceleration','model_year','origin','car_name']
df = pd.read_csv('auto-mpg.data', sep='\s+', header=None, engine='python', index=False)
df = pd.read_csv('auto-mpg.csv')



with open('auto-mpg.names') as cols:
    cols.read()

MyValues = []
for line in open('auto-mpg.data'):
    row = line.split()
    MyValues.append(row[5] if len(row)>4 else None)
print(MyValues)