import pandas as pd
import requests
import os

def gulde_site_pull():
    """ 
        Queries and stores information from Zach Gulde's website located here:
        https://python.zgulde.net
    """
    # Check local directory for file existence, run code if not found
    if not os.path.isfile('gulde_all.csv'):
        # Set URL
        base_url = 'https://python.zgulde.net'
        # Get first page's data for each directory
        item_data = requests.get(base_url + '/api/v1/items').json()
        store_data = requests.get(base_url + '/api/v1/stores').json()
        sales_data = requests.get(base_url + '/api/v1/sales').json()
        # Store each directory's first page data to dataframes
        item_df = pd.DataFrame(item_data['payload']['items'])
        store_df = pd.DataFrame(store_data['payload']['stores'])
        sales_df = pd.DataFrame(sales_data['payload']['sales'])
        # Iterate through item pages
        page = item_data['payload']['next_page']
        while page != None:
            item_data = requests.get(base_url + page).json()
            new_items = pd.DataFrame(item_data['payload']['items'])
            item_df = pd.concat([item_df, new_items]).reset_index(drop=True)
            page = item_data['payload']['next_page']
        # Iterate through sales pages (only one page for stores, no iteration)
        page = sales_data['payload']['next_page']
        while page != None:
            sales_data = requests.get(base_url + page).json()
            new_sales = pd.DataFrame(sales_data['payload']['sales'])
            sales_df = pd.concat([sales_df, new_sales]).reset_index(drop=True)
            page = sales_data['payload']['next_page']
        # Combine data into one dataframe
        full_df = pd.merge(left=sales_df, right=item_df, left_on='item', right_on='item_id')
        full_df = pd.merge(left=full_df, right=store_df, left_on='store', right_on='store_id')
        # Drop a couple columns then organize columns
        full_df = full_df.drop(columns=['item','store'])
        full_df = full_df[['sale_id','sale_date','sale_amount',
                   'item_id','item_brand','item_name','item_price','item_upc12','item_upc14',
                   'store_id','store_state','store_city','store_zipcode','store_address']]
        # Store dataframe locally
        full_df.to_csv('gulde_all.csv')
    else:
        # Read dataframe from local directory
        full_df = pd.read_csv('gulde_all.csv', index_col=0)
    
    return full_df