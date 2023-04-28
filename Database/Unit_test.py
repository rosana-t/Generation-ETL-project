from unittest.mock import Mock
import pytest
from app import *

#HP = Happy Path
#UHP = Unhappy Path

#---------------------------TRANSFORM data test_functions --------------------------------------------------------------------------------------------------------

#HP
def test_clean_sensitive_data_HP():
    raw_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','name': 'Matthew Palmer','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD', 'card_number': '12345678'}]
    expected = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = clean_sensitive_data(raw_sales_d)
    assert expected == result

#UHP
def test_clean_sensitive_data_UHP():
    expected = {}
    result = clean_sensitive_data()
    assert expected == result

#-------------------------------- Transaction(table) test_functions ------------------------------------------------------------------------------------

#HP    
def test_split_date_time_HP():
    cleaned_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = split_date_time(cleaned_sales_d)
    assert expected == result

#UHP    
def test_split_date_time_UHP():
    expected = {}
    result = split_date_time()
    assert expected == result

#HP
def test_remove_orders_data_HP():
    second_step_d = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = [{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'},{'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}]
    result = remove_orders_data(second_step_d)
    assert expected == result
    
#UHP
def test_remove_orders_data_UHP():
    expected = {}
    result = remove_orders_data()
    assert expected == result
    
#HP
def test_change_type_total_prize_HP():
    third_step_l = {'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}
    expected = {'date': '01-01-2020', 'time': '09:01', 'location': 'Leeds', 'total_price': 4.1, 'payment_method': 'CARD'}
    result = change_type_total_prize(third_step_l)
    assert expected == result
    
#UHP
def test_change_type_total_prize_UHP():
    expected = {}
    result = change_type_total_prize()
    assert expected == result

#-------------------------------- Product(table) test_functions ---------------------------------------------------------------------------------------

#HP
def test_split_products_HP():
    cleaned_sales_d = [{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'},{'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}]
    expected = ['Large Chai latte - 2.60, Regular Filter coffee - 1.50']
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
    products_split_l = ['Large Chai latte - 2.60, Regular Filter coffee - 1.50']
    expected = []
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
    unique_product_l = []
    expected = []
    result = unique_products(unique_product_l)
    assert expected == result
    
#UHP
def test_split_unique_products_UHP():
    unique_product_l = []
    expected = []
    result = unique_products(unique_product_l)
    assert expected == result

#-------------------------------- Branch(table) test_functions ---------------------------------------------------------------------------------------

#HP
def test_branch_location_HP():
    cleaned_sales_d = {'date_time': '01-01-2020 09:01', 'location': 'Leeds','order': 'Large Chai latte - 2.60, Regular Filter coffee - 1.50', 'total_price': 4.1, 'payment_method': 'CARD'}
    expected = ['Leeds']
    result = branch_location(cleaned_sales_d)
    assert expected == result
    
#UHP
def test_branch_location_UHP():
    cleaned_sales_d = {}
    expected = []
    result = branch_location(cleaned_sales_d)
    assert expected == result

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