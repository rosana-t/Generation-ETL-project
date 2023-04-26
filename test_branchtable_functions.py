# from app import branch_location
import pytest
                                


def branch_location(sales_data):
    list_of_locations = []
    for data in sales_data:
        location = data['location']
        branch_dic = {} 
        branch_dic['location'] = location
        if branch_dic not in list_of_locations:
            list_of_locations.append(branch_dic)
    return list_of_locations    



def test_branch_location():
    dummy_data = [
        {'date': '25/08/2021 09:08', 'location': 'Chesterfield', 'orders': 'Regular Latte - 2.15, Large Latte - 2.45', 'total_price': 4.6, 'payment_method': 'CASH'}
        {'date': '26/09/2022 09:08', 'location': 'Leeds', 'orders': 'Regular Latte - 2.15, Large Latte - 2.45', 'total_price': 4.6, 'payment_method': 'CASH'}
        {'date': '27/10/2023 09:08', 'location': 'Chesterfield', 'orders': 'Regular Latte - 2.15, Large Latte - 2.45', 'total_price': 4.6, 'payment_method': 'CASH'}
    ]
    
    expected = [
        {'location': 'Chesterfield'}, {'location': 'Leeds'}
    ]
    
    result = branch_location(dummy_data)
    
    assert result == expected
    
    
# def test_check_values_in_valid_list():
#     dummy_data = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': 'five', 'animal': 'dog'},
#         {'id': '3', 'animal': 'mouse'},
#     ]
    
#     expected = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': 'five', 'animal': 'dog'},
#         {'id': '3', 'animal': None}
#     ]
    
#     valid_items = ['cat', 'dog']
    
#     result = check_values_in_valid_list(dummy_data, valid_items, col_name='animal')
    
#     assert result == expected    


# def test_drop_duplicate_ids():
#     dummy_data = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': '6', 'animal': 'dog'},
#         {'id': '6', 'animal': 'cat'},
#     ]
    
#     expected = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': '6', 'animal': 'dog'}
#     ]
    
#     result = drop_duplicate_ids(dummy_data)
    
#     assert result == expected
    

# def test_drop_rows_with_null():
#     dummy_data = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': '6', 'animal': None},
#         {'id': '7', 'animal': 'cat'},
#         {'id': '8', 'animal': ''},
#     ]
    
#     expected = [
#         {'id': '5', 'animal': 'cat'}, 
#         {'id': '7', 'animal': 'cat'}
#     ]
    
#     result = drop_rows_with_null(dummy_data)
    
#     assert result == expected
