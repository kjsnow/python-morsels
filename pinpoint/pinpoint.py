
import pandas as pd
import numpy as np
from sklearn import preprocessing
from matplotlib import pyplot as plt


# Read in data and format into dataframe
cols = ['mpg','cylinders','displacement','horsepower','weight','acceleration','model_year','origin','car_name']
final_list=list()
with open('auto-mpg.data') as file:
    for line in file:
        line_split = line.split()
        line_split2 = line_split[0:8]
        line_split2.append(' '.join(line_split[8:]))
        line_split2[8] = line_split2[8].split('"')[1]
        final_list.append(line_split2)

df = pd.DataFrame(final_list, columns=cols)
df = df.set_index('car_name')

# Origin not encoded, seems that 1=US, 2=German 3=Japanese
# df.origin.unique() # 1,2,3


# Change missing hp values '?' to n/a
df.horsepower = df.horsepower.replace('?', np.nan)

# Convert columns to numeric
df.loc[:,cols[0]:cols[5]] = df.loc[:,cols[0]:cols[5]].apply(pd.to_numeric)

# For car score, do not include model_year, origin and car_name (use car_name as index)
# Normalize columns
x = df.loc[:,cols[0]:cols[5]].values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_norm = pd.DataFrame(data=x_scaled, columns=cols[:6])
df_norm = df_norm.set_index(df.index.values)

# Find mean score and sort to show (multiply by 100 to show score from 0 - 100 for ease of understanding)
df_norm['total_raw_score'] = df_norm.mean(axis=1) * 100
df_norm.sort_values(by='total_raw_score', ascending=False)


# If you want to standardize instead of normalize (would penalize those below the average
scaler = preprocessing.StandardScaler()
x_scaled2 = scaler.fit_transform(x)
df_scaled = pd.DataFrame(data=x_scaled2, columns=cols[:6])
df_scaled = df_scaled.set_index(df.index.values)

df_scaled['total_raw_score'] = df_scaled.mean(axis=1) * 100



# NOTES
# Cylinders are discrete

# ASSUMPTION: WEIGHT IS A POSITIVE ATTRIBUTE (THE HEAVIER THE BETTER) IT MIGHT BE DESIRABLE INSTEAD TO REWARD LIGHT CARS
# To do this, reverse weight where new_weight = (1 - old_weight)
df_reversed_weight = df_norm.iloc[:,:-1].copy()
df_reversed_weight.weight = (1 - df_reversed_weight.weight)

df_reversed_weight['total_raw_score'] = df_reversed_weight.mean(axis=1) * 100
df_reversed_weight.sort_values(by='total_raw_score', ascending=False)

# Missing HP is penalized by adding 0...alternative would be to make the HP the avg for missing values
df_norm_avg_hp = df_norm.iloc[:,:-1].copy()
df_norm_avg_hp.horsepower = df_norm_avg_hp.horsepower.fillna(df_norm_avg_hp.horsepower.mean())

df_norm_avg_hp['total_raw_score'] = df_norm_avg_hp.mean(axis=1) * 100
df_norm_avg_hp.sort_values(by='total_raw_score', ascending=False)

# Some of these attributes could be related (ie. more cylinders = more displacement = more weight = more horsepower generally speaking)
# This unfairly benefits cars with high scores of covariant attributes
cov = df_norm_avg_hp.iloc[:,:-1].cov() # SHOW THIS GRAPHIC

# I'd also argue that the number of cylinders, displacement, and weight should not necessarily be thought of as 'good' or 'bad' factors
# This version will only count mpg, horsepower and acceleration
df_norm_trimmed = df_norm[['mpg','horsepower','acceleration']].copy()

df_norm_trimmed['total_raw_score'] = df_norm_trimmed.mean(axis=1) * 100
df_norm_trimmed.sort_values(by='total_raw_score', ascending=False)


# Weighted scores
# I would assert that in this day and age mpg is a more important attribute to consider while hp and acceleration would still be weighed equally
# Under the following weights I am stating that mpg is equally as important as hp and acc combined
mpg_weight = .5
hp_weight = .25
acc_weight = .25

df_norm_trimmed['total_weighted_score'] = (df_norm_trimmed.mpg * mpg_weight\
                                          + df_norm_trimmed.horsepower * hp_weight\
                                          + df_norm_trimmed.acceleration * acc_weight)\
                                          * 100

df_norm_trimmed.sort_values(by='total_weighted_score', ascending=False)


# Final rec:
# Only using mpg, hp, acc
# fill hp with mean
# weighted
df_final_rec = df_norm[['mpg','horsepower','acceleration']].copy()
df_final_rec.horsepower = df_final_rec.horsepower.fillna(df_final_rec.horsepower.mean())

mpg_weight = .5
hp_weight = .25
acc_weight = .25

df_final_rec['total_weighted_score'] = (df_final_rec.mpg * mpg_weight\
                                        + df_final_rec.horsepower * hp_weight\
                                        + df_final_rec.acceleration * acc_weight)\
                                        * 100

df_final_rec.sort_values(by='total_weighted_score', ascending=False)

# Normalize attributes where we want to penalize being worse (mpg, standardize others...




###### Plots
# Boxplot
pyplot.boxplot(df_norm.iloc[:,:-1])
box_plt = df_norm.iloc[:,:-1].plot(kind='box') # normalized box

for col in df.iloc[:,:-2]:
    plt.figure()
    df.boxplot(col)
