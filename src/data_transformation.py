import pandas as pd

from fastlogging import LogInit

logger = LogInit(pathName='logs/data_transformation.log')

def load_ingested_components_data() -> pd.DataFrame:
    df = pd.read_pickle('./data/df_components.pkl')
    return df

def load_ingested_orders_data() -> pd.DataFrame:
    df = pd.read_pickle('./data/df_orders.pkl')
    return df

def expand_orders_data(df: pd.DataFrame) -> pd.DataFrame:
    '''A function to separate each order item into it's own row and separate the
    units column into 2 columns: component_id and quantity. Essentially this 
    turns the orders dataframe into a dataframe representing each line of each 
    order. '''
    
    df.loc[:, 'units'] = df['units'].apply(lambda x: list(x.items()))
    df = df.explode('units')
    df.loc[:, 'component_id'] = df['units'].apply(lambda x: x[0])
    df.loc[:, 'quantity'] = df['units'].apply(lambda x: x[1])
    df.pop('units')

    return df

def join_components_to_orderlines(df_components: pd.DataFrame, 
                                  df_orderlines: pd.DataFrame
) -> pd.DataFrame:
    'A function to join the components information to the orderlines data'

    df = df_orderlines.merge(
        df_components, left_on='component_id', right_on='componentId'
    )
    df.pop('componentId')

    return df

def create_orderlines_df(df_components: pd.DataFrame, df_orders: pd.DataFrame): 
    '''A function to create an orderlines dataframe, enriched with component
    data from the components dataframe and orders dataframe'''

    df = expand_orders_data(df_orders)
    df = join_components_to_orderlines(df_components, df)
    df.to_pickle('./src/data/df_orderlines')

def main():
    'Load the data and transform to create the orderline dataframe'

    logger.info("STARTING DATA TRANSFORMATION")

    df_components = load_ingested_components_data()
    df_orders = load_ingested_orders_data()
    create_orderlines_df(df_components, df_orders)

    logger.info("FINISHED DATA TRANSFORMATION")

if __name__ == '__main__':
    
    try:
        main()
    except Exception as e:
        logger.exception(e)