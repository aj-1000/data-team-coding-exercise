import pandas as pd

from fastlogging import LogInit

logger = LogInit(pathName='logs/data_ingestion.log')

def ingest_components_file(file: str) -> None:
    "A function to load, type check and save the components data from a file"
    df = pd.read_csv(file)
    df.to_pickle('./data/df_components.pkl')

def ingest_orders_file(file: str):
    "A function to load, type check and save the orders data from a file"
    df = pd.read_json(file, lines=True)
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