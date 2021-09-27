import pandas as pd
import pandera as pa
import numpy as np

from fastlogging import LogInit

logger = LogInit(pathName='logs/data_ingestion.log')

def check_dataframe_schema(df: pd.DataFrame, schema: pa.DataFrameSchema) -> None:
    """A function to assert that the dataframe has the types expected in the 
    schema"""
    validate_df = schema.validate(df)

def ingest_components_file(file: str) -> None:
    "A function to load, type check and save the components data from a file"
    schema = pa.DataFrameSchema({
        "componentId": pa.Column(str),
        "colour": pa.Column(str),
        "costPrice": pa.Column(float) 
    })

    df = pd.read_csv(file)
    check_dataframe_schema(df, schema)
    df.to_pickle('./data/df_components.pkl')

def ingest_orders_file(file: str):
    "A function to load, type check and save the orders data from a file"
    schema = pa.DataFrameSchema({
        "timestamp": pa.Column(np.datetime64),
        "orderId": pa.Column(str),
        "units": pa.Column(object) 
    })
    
    df = pd.read_json(file, lines=True)
    check_dataframe_schema(df, schema)
    df.to_pickle('./data/df_orders.pkl')

def main(components_file: str, orders_file: str) -> None:
    "Call the data ingestion functions"

    logger.info("STARTING DATA INGESTION")

    ingest_components_file(components_file)
    ingest_orders_file(orders_file)

    logger.info("FINISHED DATA INGESTION")


if __name__ == '__main__':

    try:
        main('./data/components.csv', './data/orders.json.txt')
    except Exception as e:
        logger.exception(e)