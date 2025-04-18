from typing import List, Dict, Union

''' The typing module in Python is used to add type hints to your variables, function parameters, and return values.
'''
# def add(a , b) : simple code as in python we dont have to define anything 
#     return a+b

# even we use typing this code will still work for string or any data type until we use mypy to check
# it shows that a, b must be int and return int 
def add(a : int, b : int) -> int :
    return a+b

# to check the error that we put a,b according to their data type or not we use "python -m mypy file_name.py" in terminal 

print( add("hello", "world"))