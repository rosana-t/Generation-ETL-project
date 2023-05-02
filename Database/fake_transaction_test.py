from unittest.mock import Mock
import pytest
from app import *

#----------------------------------------- Transaction(table) test_functions ------------------------------------------------------------------------------------

#HP    
def test_split_date_time_HP():
    cleaned_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = split_date_time(cleaned_sales_d)
    assert expected == result

#UHP - Test when date_time key is not in the dictionary, therefore split_date_time() function will not be able to split the date and time from the date_time     
def test_split_date_time_UHP():
    missing_date_time_key = [{'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    with pytest.raises(KeyError):
        split_date_time(missing_date_time_key)

#HP
def test_remove_orders_data_HP():
    second_step_d = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','orders': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','orders': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = remove_orders_data(second_step_d)
    assert expected == result
    
#UHP - Test when no argument is passed to the function and raises a TypeError, second_step_d parameter is needed for the function to work
def test_remove_orders_data_UHP():
    with pytest.raises(TypeError):
        remove_orders_data()
    
#HP
def test_change_type_total_prize_HP():
    third_step_l = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'}]
    expected = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = change_type_total_prize(third_step_l)
    assert expected == result
    
#UHP - test the total_price function tries to convert a value to a float, rasies a ValueError as there is no valid number in the data
def test_change_type_total_prize_UHP():
    third_step_1 = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 'invalid', 'payment_method': 'CARD'}]
    with pytest.raises(ValueError):
        change_type_total_prize(third_step_1)

#HP
def test_convert_all_dates_HP():
    data = [{'date': '05-11-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'},{'date': '05-11-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'}]
    date_cols = ['date']
    expected = [{'date': '11-05-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'},{'date': '11-05-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'}]
    result = convert_all_dates(data, date_cols, current_format= '%d-%m-%Y', expected_format='%m-%d-%Y')
    assert result == expected

#UHP - Test when passing a string instead of a list to date_cols which causes a KeyError
def test_convert_all_dates_UHP():
    data = [{'date': '05-11-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'},{'date': '05-11-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': '4.1', 'payment_method': 'CARD'}]
    date_cols = 'date'
    with pytest.raises(KeyError):
        convert_all_dates(data, date_cols=date_cols, current_format= '%d-%m-%Y', expected_format='%m-%d-%Y')

    
