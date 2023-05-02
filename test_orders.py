from data_functions import item_quantity
from data_functions import product_dict_in_order

def test_item_quantity_one_qty_per_item_in_order():

    data = [{'branch': 'Leeds', 'order': ["Regular Chai latte - 2.30", "Regular Speciality Tea - English breakfast - 1.30"], \
             'total_price': '3.60', 'payment_method': 'CASH'}, \
             {'branch': 'Leeds', 'order': ["Large Chai latte - 2.60", "Regular Filter coffee - 1.50"], \
             'total_price': '3.60', 'payment_method': 'CASH'}]
    
    expected = [{'branch': 'Leeds', 'order': ["Regular Chai latte - 2.30, 1", "Regular Speciality Tea - English breakfast - 1.30, 1"], \
             'total_price': '3.60', 'payment_method': 'CASH'}, \
             {'branch': 'Leeds', 'order': ["Large Chai latte - 2.60, 1", "Regular Filter coffee - 1.50, 1"], \
             'total_price': '3.60', 'payment_method': 'CASH'}]
    
    result = item_quantity(data)
    assert expected == result

def test_item_quantity_2_qty_per_item_in_order():
    data = [{'branch': 'Leeds', 'order': ["Regular Chai latte - 2.30", "Regular Chai latte - 2.30", "Regular Speciality Tea - English breakfast - 1.30"], \
             'total_price': '3.60', 'payment_method': 'CASH'}, \
             {'branch': 'Leeds', 'order': ["Large Chai latte - 2.60", "Regular Filter coffee - 1.50", "Regular Filter coffee - 1.50"], \
             'total_price': '3.60', 'payment_method': 'CASH'}]
    
    expected = [{'branch': 'Leeds', 'order': ["Regular Chai latte - 2.30, 2", "Regular Speciality Tea - English breakfast - 1.30, 1"], \
             'total_price': '3.60', 'payment_method': 'CASH'}, \
             {'branch': 'Leeds', 'order': ["Large Chai latte - 2.60, 1", "Regular Filter coffee - 1.50, 2"], \
             'total_price': '3.60', 'payment_method': 'CASH'}]
    
    result = item_quantity(data)
    assert expected == result

def test_product_dict_in_order_qty_1():
    data = [{'branch': 'Leeds', 'order': ["Regular Chai latte - 2.30", "Regular Speciality Tea - English breakfast - 1.30"], \
             'total_price': '3.60', 'payment_method': 'CASH'}, \
             {'branch': 'Leeds', 'order': ["Large Chai latte - 2.60", "Regular Filter coffee - 1.50"], \
             'total_price': '3.60', 'payment_method': 'CASH'}]
    
    expected = [{'branch': 'Leeds', 'order': [{'product_size': 'Regular', 'product_name': 'Chai latte', 'product_qty': 1, 'product_price': 2.3}, \
                {'product_size': 'Regular', 'product_name': 'Speciality Tea English breakfast', 'product_qty': 1, 'product_price': 1.3}], 'total_price': '3.60', 'payment_method': 'CASH'}, \
               {'branch': 'Leeds', 'order': [{'product_size': 'Regular', 'product_name': 'Filter coffee', 'product_qty': 1, 'product_price': 1.5}, \
               {'product_size': 'Large', 'product_name': 'Chai latte', 'product_qty': 1, 'product_price': 2.6}], 'total_price': '3.60', 'payment_method': 'CASH'}]
    
    result = product_dict_in_order(data)
    assert expected == result