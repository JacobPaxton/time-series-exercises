import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import acquire

# --------------------- Store Items --------------------- #
def wrangle_gulde():
    """ acquire and prepare Zach Gulde's site data, return df """
    # acquire
    df = acquire.gulde_site_pull()
    # datetime
    df = gulde_datetime_fix(df)
    # month and day_name columns
    df = gulde_datetime_fix(df)
    # calculate total sale cost for each transaction
    df = calc_gulde_total_sales(df)
    return df

def gulde_datetime_fix(df):
    """ convert sale_date to datetime64, set it as index, return df """
    df['sale_date'] = df['sale_date'].astype('datetime64')
    df.index = df.sale_date
    return df

def add_month_dayname_cols(df):
    """ add month and day_name columns from a datetime64 index, return df """
    df['month'] = df.index.month
    df['day_name'] = df.index.dayname
    return df

def calc_gulde_total_sales(df):
    """ calculate sales_total column from # sold and price """
    df['sales_total'] = df['sale_amount'] * df['item_price']
    return df

def plot_date_price_changes():
    """ plot changes in price over time (in months) """
    # acquire
    df = acquire.gulde_site_pull()
    # month column
    df['month'] = df['sale_date'].dt.month
    # new dataframe with a groupby
    df_monthly = df.groupby(['month','item_name']).item_price.mean().reset_index()
    # x, y, and hue plot
    sns.lineplot(x=df_monthly.month, 
                y=df_monthly.item_price, 
                hue=df_monthly.item_name, 
                legend=None)
    plt.show()

# ---------------------- OPS Data ---------------------- #
def prepare_ops():
    """ prepares locally-saved OPS data from opsd_germany_daily.csv """
    # acquire
    ops = pd.read_csv('opsd_germany_daily.csv', index_col=0)
    # datetime fix
    ops = ops_datetime_fix(ops)
    # add month and year columns
    ops = add_month_year_cols(ops)
    # fill nulls
    ops = fill_ops_nulls(ops)
    return df


def ops_datetime_fix(ops):
    """ changes data dtype to datetime64 and makes it the index """
    # cast as datetime64
    ops['Date'] = ops['Date'].astype('datetime64')
    # set index
    ops.index = ops.Date
    return ops

def add_month_year_cols(ops):
    """ adds columns for month and year from a datetime64 index """
    ops['month'] = ops.index.month
    ops['year'] = ops.index.year
    return ops

def fill_ops_nulls(ops):
    """ columnwise-fills nulls in OPS data with mean """
    # set fill values
    values = {"Wind": ops.Wind.mean(), 
          "Solar": ops.Solar.mean(), 
          "Wind+Solar": ops['Wind+Solar'].mean()}
    # fills values
    ops = ops.fillna(value=values)
    return ops

def plot_ops(ops):
    """ plots distribution of each column in OPS data """
    for col in ops.columns:
        sns.histplot(ops[col])
        plt.title(col + ' distribution')
        plt.show()