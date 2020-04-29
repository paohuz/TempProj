import pandas as pd
from guppy import hpy
h = hpy()

students = [('jack', 34, 'Sydeny', 'Australia'),
            ('Riti', 30, 'Delhi', 'India'),
            ('Vikas', 31, 'Mumbai', 'India'),
            ('Neelu', 32, 'Bangalore', 'India'),
            ('John', 16, 'New York', 'US'),
            ('Mike', 17, 'las vegas', 'US')]
data = pd.DataFrame(students, columns=[
    'Name', 'Age', 'City', 'Country'], index=['a', 'b', 'c', 'd', 'e', 'f'])
print(h.heap())

data = data.append({'Name': 'jacky', 'Age': 34,
                    'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)
print(h.heap())
