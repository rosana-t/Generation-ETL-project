from unittest.mock import Mock,patch
import pytest
from app import *

#HP = Happy Path
#UHP = Unhappy Path

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------

#HP
def test_extract_data_HP():
    filename = "csvfile_for_testing.csv"
    expected = [{'date_time': '25/08/2021 09:00', 'location': 'Chesterfield', 'name': 'Richard Copeland', 'orders': 'Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45', 'total_price': '5.2', 'payment_method': 'CARD', 'card_number': '123456789'}, 
                {'date_time': '25/08/2021 09:00', 'location': 'Chesterfield', 'name': 'Richard Copeland', 'orders': 'Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45', 'total_price': '5.2', 'payment_method': 'CASH', 'card_number': ''},
                {'date_time': '25/08/2021 09:04', 'location': 'Chesterfield', 'name': 'Francis Strayhorn', 'orders': 'Large Flat white - 2.45, Regular Latte - 2.15', 'total_price': '4.6', 'payment_method': 'CARD', 'card_number': '123456789'}]
    result = extract_data(filename)
    assert expected == result
    
#UHP (file not found)
def test_extract_data_UHP():
    with pytest.raises(TypeError):
       extract_data()
    
#---------------------------TRANSFORM data test_functions --------------------------------------------------------------------------------------------------------

#HP
def test_clean_sensitive_data_HP():
    raw_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    expected = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = clean_sensitive_data(raw_sales_d)
    assert expected == result

#UHP - Test when name key is not in the dictionary, therefore clean_sensitive_data() function will not be able to delete the name key.     
def test_clean_sensitive_data_UHP():
    missing_name_key = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    with pytest.raises(KeyError):
        clean_sensitive_data(missing_name_key)

#-------------------------------- Transaction(table) test_functions ------------------------------------------------------------------------------------

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

#-------------------------------- Product(table) test_functions ---------------------------------------------------------------------------------------

#HP
def test_split_products_HP():
    cleaned_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','orders': 'Large Chai latte - 2.60, Large Chai latte - 2.60', 'total_price': 4.1, 'payment_method': 'CARD'}, {'date_time': '01-01-2020 09:01', 'location': 'Leeds','orders': 'Large Chai latte - 2.60, Large Chai latte - 2.60', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = [['Large Chai latte - 2.60', ' Large Chai latte - 2.60'], ['Large Chai latte - 2.60', ' Large Chai latte - 2.60']]
    result = split_products(cleaned_sales_d)
    assert expected == result   

#UHP    
def test_split_products_UHP():
    missing_orders_key = [{'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'},{'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}]
    with pytest.raises(KeyError):
        split_date_time(missing_orders_key) 
    
#HP
def test_unique_products_HP():
    products_split_l = [['Regular Flavoured iced latte - Hazelnut - 2.75', ' Large Latte - 2.45'], ['Regular Flavoured iced latte - Hazelnut - 2.75', ' Large Latte - 2.45'], ['Large Flat white - 2.45', ' Regular Latte - 2.15']]
    expected = ['Regular Flavoured iced latte - Hazelnut - 2.75', 'Large Latte - 2.45', 'Large Flat white - 2.45', 'Regular Latte - 2.15']
    result = unique_products(products_split_l)
    assert expected == result
    
#UHP
def test_unique_products_UHP():
    with pytest.raises(TypeError):
        unique_products()

# HP
def test_split_unique_products_HP():
    unique_product_l = ['Regular Flavoured iced latte - Hazelnut - 2.75', 'Large Latte - 2.45', 'Large Flat white - 2.45', 'Regular Latte - 2.15']
    expected = [
        {'name': 'Flavoured iced latte Hazelnut', 'size': 'Regular', 'price': 2.75},
        {'name': 'Latte', 'size': 'Large', 'price': 2.45},
        {'name': 'Flat white', 'size': 'Large', 'price': 2.45},
        {'name': 'Latte', 'size': 'Regular', 'price': 2.15}
    ]
    result = split_unique_products(unique_product_l)
    assert expected == result
    
#UHP
def test_split_unique_products_UHP():
    with pytest.raises(TypeError):
        split_unique_products() 

#------------------------------- Branch(table) functions ------------------------------------------------------------

#HP
def test_branch_location_HP():
    raw_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},
                   {'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},
                   {'date_time': '01-01-2020 09:01', 'location': 'London','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    expected = ["Leeds", "London" ]
    result = branch_location(raw_sales_d)
    assert expected == result

#UHP - Test when location key is not in the dictionary, therefore branch_location() function will not be able to add the location into the list_of_locations.     
def test_branch_location_UHP():
    missing_location_key = [{'date_time': '01-01-2020 09:01', 'order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},{'date_time': '01-01-2020 09:01','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    with pytest.raises(KeyError):
        branch_location(missing_location_key)

#---------------------------------------Orders(table) functions-----------------------------------------------------------------------------------
def test_split_items_for_transaction():
    data = [{'orders': "Regular Chai latte - 2.30, Regular Iced Americano - 1.30"}, 
        {'orders': "Large Chai latte - 2.60, Regular Filter coffee - 1.50"}]
    
    expected = [{'orders': ["Regular Chai latte - 2.30", " Regular Iced Americano - 1.30"]}, 
    {'orders': ["Large Chai latte - 2.60", " Regular Filter coffee - 1.50"]}]

    
    result = split_items_for_transactions(data)
    assert expected == result

def test_item_quantity_one_qty_per_item_in_order():

    data = [
        {'orders': ["Regular Chai latte - 2.30"]},
        {'orders': ["Regular Filter coffee - 1.50"]}
        ]
    
    
    expected = [
        {'orders': ["Regular Chai latte - 2.30, 1"]}, 
        {'orders': ["Regular Filter coffee - 1.50, 1"]}
     ]

    
    result = item_quantity(data)
    assert expected == result

def test_item_quantity_2_qty_per_item_in_order():
    data = [
        {'orders': ["Regular Chai latte - 2.30", "Regular Chai latte - 2.30"]},
        {'orders': ["Regular Filter coffee - 1.50", "Regular Filter coffee - 1.50"]}
        ]
    
    expected = [
        {'orders': ["Regular Chai latte - 2.30, 2"]},
        {'orders': ["Regular Filter coffee - 1.50, 2"]}
        ]
    
    result = item_quantity(data)
    assert expected == result

def test_product_dict_in_order_qty_1():
    data = [
        {'orders': ["Regular Chai latte - 2.30, 1", "Regular Speciality Tea - English breakfast - 1.30, 1"]},
        {'orders': ["Large Chai latte - 2.60, 1", "Regular Filter coffee - 1.50, 1"]}
            ]
    
    expected = [
        {'orders': [{'product_size': 'Regular', 'product_name': 'Chai latte', 'product_qty': 1, 'product_price': 2.3}, {'product_size': 'Regular', 'product_name': 'Speciality Tea English breakfast', 'product_qty': 1, 'product_price': 1.3}]},
        {'orders': [{'product_size': 'Large', 'product_name': 'Chai latte', 'product_qty': 1, 'product_price': 2.6}, {'product_size': 'Regular', 'product_name': 'Filter coffee', 'product_qty': 1, 'product_price': 1.5}]}
        ]
    
    result = product_dict_in_order(data)
    assert expected == result


def test_product_dict_in_order_qty_2():
    data = [
        {'orders': ["Regular Chai latte - 2.30, 2", "Regular Speciality Tea - English breakfast - 1.30, 1", ]},
        {'orders': ["Large Chai latte - 2.60, 1", "Regular Filter coffee - 1.50, 2"]}
            ]
    
    expected = [
        {'orders': [{'product_size': 'Regular', 'product_name': 'Chai latte', 'product_qty': 2, 'product_price': 2.3}, {'product_size': 'Regular', 'product_name': 'Speciality Tea English breakfast', 'product_qty': 1, 'product_price': 1.3}]},
        {'orders': [{'product_size': 'Large', 'product_name': 'Chai latte', 'product_qty': 1, 'product_price': 2.6}, {'product_size': 'Regular', 'product_name': 'Filter coffee', 'product_qty': 2, 'product_price': 1.5}]}
        ]
    
    result = product_dict_in_order(data)
    assert expected == result