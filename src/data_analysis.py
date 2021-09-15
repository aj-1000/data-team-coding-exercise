from numpy import datetime64
import pandas as pd

from fastlogging import LogInit

logger = LogInit(pathName='logs/data_analysis.log')

def load_orderlines_data() -> pd.DataFrame:
    df = pd.read_pickle('./data/df_orderlines.pkl')
    return df

def filter_data_by_date(df: pd.DataFrame, 
                        start_date: pd.Timestamp, 
                        end_date: pd.Timestamp) -> pd.DataFrame:
    '''Function to select only those rows where timestamp is greater than or 
    equal to the start_date AND less than the end_date'''

    df = df.loc[(df['timestamp'] >= start_date) 
                & (df['timestamp'] < end_date)]

    return df

def sum_components_by_colour(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby('colour').sum()
    return df

def output_colour_analysis(df: pd.DataFrame, 
                           start_date: str, 
                           end_date: str) -> None:
    '''A function to perform the required colour analysis and output the 
    results. The analysis performs a count of the number of components sold of
    each colour between the start date and the end date
    '''

    df = filter_data_by_date(df, pd.to_datetime(start_date, utc=True), 
                             pd.to_datetime(end_date, utc=True))
    df = sum_components_by_colour(df)
    df.pop('costPrice')
    df.to_csv(f'./output/colour_output_{start_date}.txt', sep=':')

def main(start_date: str, end_date: str) -> None:
    'Load the orderlines data and analyse'

    logger.info("STARTING DATA ANALYSIS")
    
    df = load_orderlines_data()
    output_colour_analysis(df, start_date, end_date)
    
    logger.info("FINISHED DATA ANALYSIS")

if __name__ == '__main__':
    
    try:
        main('2021-06-03', '2021-06-04')
    except Exception as e:
        logger.exception(e)