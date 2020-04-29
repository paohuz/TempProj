import numpy as np
import pandas as pd

a = [1, 2, 3]
b = [4, 4, 4]
c = np.stack([a, b], axis=1)
print(c)

d = np.concatenate((a, b), axis=1)
print('d')
print(d)

z = []
w = [5, 5, 5]
x = [1, 2, 3]
y = [4, 4, 4]

z.append(w)
z.append(x)
z.append(y)
print(z)
z = np.swapaxes(z, 0, 1)
print(z)

names = ['a1', 'a2', 'a3']
names = []
names.append('a1')
names.append('a2')
names.append('a3')
for name in names:
    print(name)

# List of Tuples
students = [('jack', 34, 'Sydeny', 'Australia'),
            ('Riti', 30, 'Delhi', 'India'),
            ('Vikas', 31, 'Mumbai', 'India'),
            ('Neelu', 32, 'Bangalore', 'India'),
            ('John', 16, 'New York', 'US'),
            ('Mike', 17, 'las vegas', 'US')]

# Create a DataFrame object
dfObj = pd.DataFrame(students, columns=['Name', 'Age', 'City', 'Country'], index=[
                     'a', 'b', 'c', 'd', 'e', 'f'])
print(dfObj)

lst = []
first = dfObj[['Name', 'Age']]
second = dfObj[['City', 'Country']]
first = 'f'
second = 's'
third = 't'
# first = [1, 1, 1]
# second = [2, 2, 2]
# print('first')
# print(first.values)
# print('second')
# print(second.values)
# lst.append({first.values, second.values})
# print(lst)
lst.append({first, second, third, first})
print(lst)
