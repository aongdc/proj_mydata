import pandas as pd
import matplotlib.pyplot as plt
from datetime import time, timedelta

# load csv into dataframe `my_log`
my_log = pd.read_csv('data/my_daily_log.csv')

# view all columns
my_log.columns

# rename columns to what they represent
my_log.rename({'Timestamp': 'ts',
               'How stressed do you feel right now?': 'stress_level',
               'What time did you sleep last night?': 'bed_time',
               'What time did you wake up today?': 'wake_time',
               'Did you feel lethargic when you woke up today?': 'lethargic',
               'What activities did you do/are you doing today?': 'activities',
               'How much did you spend today?': 'spend_amt',
               'How happy do you feel overall today?': 'happy_level',
               'Overall, did you enjoy/are you enjoying today more than yesterday?': 'enjoy_more'
               }, axis=1, inplace=True)

# convert `timestamp` to datetime object for easier manipulation later on
my_log['ts'] = pd.to_datetime(my_log['ts'], format='%m/%d/%Y %H:%M:%S')

# wish to convert `bed_time`, `wake_time` to datetime object as well, but there will be a date added
my_log[['bed_time', 'wake_time']] = my_log[['bed_time', 'wake_time']].apply(pd.to_datetime, format='%I:%M:%S %p')

# for `bed_time`, the day will be the same day if before 12am, else +1 day
# for `wake_time`, the time will always be the next day
def bed_wake_to_dt(row):
    ts = row['ts']
    # `bed_time` will be next day if before 12pm, else same day
    nd = ts + timedelta(days=1) if row['bed_time'].time() < time(hour=12) else ts
    row['bed_time'] = row['bed_time'].replace(nd.year, nd.month, nd.day)
    # `wake_time` will always +1 day
    nd = ts + timedelta(days=1)
    row['wake_time'] = row['wake_time'].replace(nd.year, nd.month, nd.day)
    return row
my_log = my_log.apply(bed_wake_to_dt, axis=1)

# create new column `sleep_dur` to calculate sleep duration
my_log['sleep_dur'] = my_log['wake_time'] - my_log['bed_time']

# convert `lethargic` to boolean
my_log['lethargic'] = (my_log['lethargic'] == 'Yes')

# convert `spend_amt` to ordinal/categorical
my_log['spend_amt'] = my_log['spend_amt'].astype('category').cat.as_ordered()

# clean `activities` column
acts = my_log['activities'].unique()
acts = my_log['activities'].str.split(', ')

# hard to see if there are any free response "other" values
set([a for act in acts for a in act])

act_opts = ['Attend classes', 'Study/complete assignments', 'Go out with friends',
              'Watch shows/entertainment activities', 'Drink coffee', 'Exercise']
my_log['attend_class'] = my_log['activities'].str.contains(act_opts[0])
my_log['study_assign'] = my_log['activities'].str.contains(act_opts[1])
my_log['friends_outing'] = my_log['activities'].str.contains(act_opts[2])
my_log['shows_entertain'] = my_log['activities'].str.contains(act_opts[3])
my_log['coffee'] = my_log['activities'].str.contains(act_opts[4])
my_log['exercise'] = my_log['activities'].str.contains(act_opts[5])

def other_acts(row, act_opts):
    res = [x for x in row['activities'].split(', ') if x not in act_opts]
    return ', '.join(res) if len(res) > 0 else None
my_log['other_acts'] = my_log.apply(other_acts, act_opts=act_opts, axis=1)

my_log['other_acts'].value_counts()

my_log['bed_time'].value_counts()

my_log[my_log['ts'].dt.date.diff() > timedelta(days=1)]

######
plt.matshow(corr_mat, cmap='seismic', vmin=-1, vmax=1)
plt.xticks(range(len(corr_mat)), corr_mat.index, rotation=45, ha='left')
plt.yticks(range(len(corr_mat.columns)), corr_mat.columns)
# plt.title('Number of Daily Activities Across Time')
plt.colorbar(fraction=0.04)
plt.gca().tick_params(labelsize=8)
plt.show()