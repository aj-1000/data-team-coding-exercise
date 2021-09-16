import pytest
import pandas as pd

from unittest.mock import patch

from src.data_analysis import (filter_data_by_date, output_colour_analysis, sum_components_by_colour)

@pytest.fixture(scope='class')
def dummy_orderline_df() -> pd.DataFrame:
    test_data = {
        'timestamp': [pd.to_datetime('2021-06-02', utc=True)] + 
                     [pd.to_datetime('2021-06-03', utc=True)] * 4,
        'orderId': ['1000a-1000b-1000c', '1000a-1000b-1000c', 
                    '1001d-1001e-1001f', '1001a-1001b-1001c', 
                    '1001a-1001b-1001c'],
        'component_id': ['BKRED01', 'BKONG13', 'BKONG13', 'BKGRN02', 
                         'XXBLU99'],
        'quantity': [1, 1, 2, 2, 3],
        'colour': ['Red', 'Orange', 'Orange', 'Green', 'Blue'],
        'costPrice': [0.021, 0.022, 0.022, 0.024, 0.04]
    } 
    dummy_orderline_df = pd.DataFrame.from_dict(test_data)
    return dummy_orderline_df

@pytest.fixture(scope='class')
def dummy_date_filtered_orderline_df() -> pd.DataFrame:
    test_data = {
        'timestamp': [pd.to_datetime('2021-06-03', utc=True)] * 4,
        'orderId': ['1000a-1000b-1000c', '1001d-1001e-1001f', 
                    '1001a-1001b-1001c', '1001a-1001b-1001c'],
        'component_id': ['BKONG13', 'BKONG13', 'BKGRN02', 'XXBLU99'],
        'quantity': [1, 2, 2, 3],
        'colour': ['Orange', 'Orange', 'Green', 'Blue'],
        'costPrice': [0.022, 0.022, 0.024, 0.04]
    } 
    dummy_date_filtered_orderline_df = pd.DataFrame.from_dict(test_data)
    return dummy_date_filtered_orderline_df

def test_filter_data_by_date(dummy_date_filtered_orderline_df: pd.DataFrame,
                             dummy_orderline_df: pd.DataFrame) -> None:

    expected = dummy_date_filtered_orderline_df
    actual = filter_data_by_date(dummy_orderline_df, '2021-06-03', 
                                 '2021-06-04')
    pd.testing.assert_frame_equal(actual, expected)

def test_sum_components_by_colour(
    dummy_date_filtered_orderline_df: pd.DataFrame
) -> None:
    
    data = {
        'colour': ['Blue', 'Green', 'Orange'],
        'quantity': [3, 2, 3]
    }
    expected = pd.DataFrame.from_dict(data).set_index('colour')

    df = dummy_date_filtered_orderline_df.loc[
        :, dummy_date_filtered_orderline_df.columns != 'costPrice'
    ]
    actual = sum_components_by_colour(df)
    pd.testing.assert_frame_equal(actual, expected)

@patch('src.data_analysis.save_colour_analysis')
@patch('src.data_analysis.sum_components_by_colour')
@patch('src.data_analysis.filter_data_by_date')
def test_output_colour_analysis(mock_filter_data, mock_sum_components, 
                                mock_save_analysis) -> None:
    
    output_colour_analysis('arg1', 'arg2', 'arg3')
    mock_filter_data.assert_called()
    mock_sum_components.assert_called()
    mock_save_analysis.assert_called()