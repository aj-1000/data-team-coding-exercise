import pytest
import pandas as pd

from unittest.mock import patch

from src.data_transformation import (create_orderlines_df, expand_orders_data, 
                                     join_components_to_orderlines)

@pytest.fixture(scope='class')
def dummy_orders_df() -> pd.DataFrame:
    test_data = {
        'timestamp': [pd.to_datetime('2021-06-03', utc=True)] * 2,
        'orderId': ['1000a-1000b-1000c', '1001a-1001b-1001c'],
        'units': [{'BKRED01': 1, 'BKONG13': 1}, {'BKYLW88': 2, 'BKGRN02': 2}]
    }
    dummy_orders_df = pd.DataFrame.from_dict(test_data)
    return dummy_orders_df

@pytest.fixture(scope='class')
def dummy_components_df() -> pd.DataFrame:
    test_data = {
        'componentId': ['BKRED01', 'BKONG13',  'BKYLW88', 'BKGRN02'],
        'colour': ['Red', 'Orange', 'Yellow', 'Green'],
        'costPrice': [0.021, 0.022, 0.033, 0.024]
    }
    dummy_components_df = pd.DataFrame.from_dict(test_data)
    return dummy_components_df

@pytest.fixture(scope='class')
def dummy_expanded_orders_df() -> pd.DataFrame:
    test_data = {
        'timestamp': [pd.to_datetime('2021-06-03', utc=True)] * 4,
        'orderId': ['1000a-1000b-1000c', '1000a-1000b-1000c', 
                    '1001a-1001b-1001c', '1001a-1001b-1001c'],
        'component_id': ['BKRED01', 'BKONG13', 'BKYLW88', 'BKGRN02'],
        'quantity': [1, 1, 2, 2]
    } 
    dummy_expanded_orders_df = pd.DataFrame.from_dict(test_data)
    return dummy_expanded_orders_df

@pytest.fixture(scope='class')
def dummy_orderline_df() -> pd.DataFrame:
    test_data = {
        'timestamp': [pd.to_datetime('2021-06-03', utc=True)] * 4,
        'orderId': ['1000a-1000b-1000c', '1000a-1000b-1000c', 
                    '1001a-1001b-1001c', '1001a-1001b-1001c'],
        'component_id': ['BKRED01', 'BKONG13', 'BKYLW88', 'BKGRN02'],
        'quantity': [1, 1, 2, 2],
        'colour': ['Red', 'Orange', 'Yellow', 'Green'],
        'costPrice': [0.021, 0.022, 0.033, 0.024]
    } 
    dummy_orderline_df = pd.DataFrame.from_dict(test_data)
    return dummy_orderline_df

def test_expand_orders_data(dummy_orders_df: pd.DataFrame, 
                            dummy_expanded_orders_df: pd.DataFrame) -> None:
    
    expected = dummy_expanded_orders_df
    actual = expand_orders_data(dummy_orders_df)
    pd.testing.assert_frame_equal(actual, expected)

def test_join_components_to_orderline(dummy_expanded_orders_df: pd.DataFrame, 
                                      dummy_components_df: pd.DataFrame,
                                      dummy_orderline_df: pd.DataFrame) -> None:
    
    expected = dummy_orderline_df
    actual = join_components_to_orderlines(dummy_components_df, 
                                           dummy_expanded_orders_df)
    pd.testing.assert_frame_equal(actual, expected)

@patch('src.data_transformation.expand_orders_data')
@patch('src.data_transformation.join_components_to_orderlines')
@patch('src.data_transformation.save_orderlines_data')
def test_create_orderlines_df(mock_save_data, mock_join_components, 
                              mock_expand_data) -> None:
    
    create_orderlines_df('argument_1', 'argument_2')

    mock_save_data.assert_called()
    mock_join_components.assert_called()
    mock_expand_data.assert_called()