import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def time_delta(datetime_series, outcome_series):
    """ Takes a NumPy array or Pandas Series of date and outcome, then
        plots multiple visualizations based on date precision.
        Assumes nulls are handled, throws an error if nulls remain. """
    
    # try to convert columns, output message if fails
    try: datetime_series = np.array(datetime_series.astype('datetime64[ns]'))
    except: print('Please convert your datetime series to a standard format.\
        EX: 2020-11-01 01:01:01')
    try: outcome_series = np.array(outcome_series.astype('float'))
    except: print('Please re-check outcome_series for any non-numeric values.')
    
    # create df from two series, set index as date
    df = pd.DataFrame({'date':datetime_series, 'outcome':outcome_series}).set_index('date')

    # create columns for year, month, month_name, day, day_name, and hour
    df['year'], df['month'], df['day'] = df.index.year, df.index.month, df.index.day
    df['month_name'], df['day_name'] = df.index.month_name(), df.index.day_name()
    df['hour'] = df.index.hour

    # establish plot and font size
    plt.rc('figure', figsize=(13,6))
    plt.rc('axes.spines', top=False, right=False)
    plt.rc('font', size=13)

    # output initial plot
    df[['outcome']].plot()
    plt.title('Time and Outcome - Raw')
    plt.show()

    # output hour plot... lol
    if not np.all((df.index.hour == 0)):
        df[['outcome']].resample('D').mean().plot()
        plt.show()