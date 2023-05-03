from unittest.mock import Mock,patch
import pytest
from app import *

#HP = Happy Path
#UHP = Unhappy Path

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------

#HP
def test_extract_data_HP():
    filename = "csvfile_for_testing.csv"
    expected = [{'date_time': '25/08/2021 09:00', 'location': 'Chesterfield', 'name': 'Richard Copeland', 'orders': 'Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45', 'total_price': '5.2', 'payment_method': 'CARD', 'card_number': '5494173772652516'}, 
                {'date_time': '25/08/2021 09:02', 'location': 'Chesterfield', 'name': 'Scott Owens', 'orders': 'Large Flavoured iced latte - Caramel - 3.25, Regular Flavoured iced latte - Hazelnut - 2.75, Regular Flavoured iced latte - Caramel - 2.75, Large Flavoured iced latte - Hazelnut - 3.25, Regular Flavoured latte - Hazelnut - 2.55, Regular Flavoured iced latte - Hazelnut - 2.75', 'total_price': '17.3', 'payment_method': 'CARD', 'card_number': '6844802140812058'}, 
                {'date_time': '25/08/2021 09:04', 'location': 'Chesterfield', 'name': 'Francis Strayhorn', 'orders': 'Large Flat white - 2.45, Regular Latte - 2.15', 'total_price': '4.6', 'payment_method': 'CARD', 'card_number': '9557104128182483'}]
    result = extract_data(filename)
    assert expected == result
    
#UHP (file not found)
# @patch("builtins.print")
# def test_extract_data_UHP(mock_print):
#     filename = "csvfile_for_tes.csv"
#     expected = "An error occurred: file not found!"
#     extract_data(filename)
#     mock_print.assert_called_with(expected)
    
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
    cleaned_sales_d = {'location': 'Chesterfield', 'orders': 'Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45', 'total_price': 5.2, 'payment_method': 'CARD', 'date': '08-25-2021', 'time': '09:00'}
    expected = {'location': 'Chesterfield', 'orders': 'Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45', 'total_price': 5.2, 'payment_method': 'CARD', 'date': '08-25-2021', 'time': '09:00'}
    result = split_products(cleaned_sales_d)
    assert expected == result    

#UHP    
def test_split_products_UHP():
    cleaned_sales_d = {}
    expected = []
    result = split_products(cleaned_sales_d)
    assert expected == result 
    
#HP
def test_unique_products_HP():
    products_split_l = ['Large Chai latte - 2.60', 'Large Chai latte - 2.60']
    expected = ['Large Chai latte - 2.60']
    result = unique_products(products_split_l)
    assert expected == result
    
#UHP
def test_unique_products_UHP():
    products_split_l = []
    expected = []
    result = unique_products(products_split_l)
    assert expected == result

#HP
def test_split_unique_products_HP():
    unique_product_l = ['Regular Flavoured iced latte - Hazelnut - 2.75']
    expected = [{'name': 'Flavoured iced latte Hazelnut', 'size': 'Regular', 'price': 2.75},{'name': 'Flavoured iced latte Hazelnut', 'size': 'Regular', 'price': 2.75}]
    result = unique_products(unique_product_l)
    assert expected == result
    
#UHP
def test_split_unique_products_UHP():
    unique_product_l = []
    expected = []
    result = unique_products(unique_product_l)
    assert expected == result

#------------------------------- Branch(table) functions ------------------------------------------------------------

#HP
def test_branch_location_HP():
    raw_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},
                   {'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},
                   {'date_time': '01-01-2020 09:01', 'location': 'London','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    expected = ["Leeds", "London" ]
    result = branch_location(raw_sales_d)
    assert expected == result

# #UHP
# def test_extract_dat_UHP():
#     expected = {}
#     result = clean_sensitive_data()
#     assert expected == result

#------------------------------------Main App ----------------------------------------------------------------------------------------------
# test_clean_sensitive_data_HP()
# #test_clean_sensitive_data_UHP()

# #calling Product(table) functions------------------------------------------------------------
# test_split_products_HP()
# #test_split_products_UHP()
# test_unique_products_HP()
# #test_unique_products_UHP()
# test_split_unique_products_HP()
# #test_split_unique_products_UHP()

# # calling Transaction(table) functions-------------------------------------------------------
# test_split_date_time_HP()
# #test_split_date_time_UHP()
# test_remove_orders_data_HP()
# #test_remove_orders_data_UHP()
# test_change_type_total_prize_HP()
# #test_change_type_total_prize_UHP()

# #calling Branch(table) functions--------------------------------------------------------------
# test_branch_location_HP()
# #test_branch_location_UHP()