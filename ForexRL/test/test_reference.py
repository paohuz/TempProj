import pandas as pd
from pprint import pprint
from guppy import hpy
h = hpy()


class parent1:
    def __init__(self):
        students = [('jack', 34, 'Sydeny', 'Australia'),
                    ('Riti', 30, 'Delhi', 'India'),
                    ('Vikas', 31, 'Mumbai', 'India'),
                    ('Neelu', 32, 'Bangalore', 'India'),
                    ('John', 16, 'New York', 'US'),
                    ('Mike', 17, 'las vegas', 'US')]
        self.data = pd.DataFrame(students, columns=[
                                 'Name', 'Age', 'City', 'Country'], index=['a', 'b', 'c', 'd', 'e', 'f'])

        self.cnt = 0


class parent2:
    # better in any case
    def __init__(self, data):
        self.data = data
        self.cnt = 0


class child1_1(parent1):
    def print_data_ref(self):
        self.data.memory_usage()
        print(f'child1')
        print(f'data ref: {id(self.data)}')
        print(self.data)

    def add_item(self):
        # self.data.append({'Name': 'jacky', 'Age': 34,
        #                   'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)
        self.cnt += 1
        self.data[f'{self.cnt}'] = 1
        # self.data = self.data.append({'Name': 'jacky', 'Age': 34,
        #                               'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)


class child1_2(parent1):
    def print_data_ref(self):

        print(f'child2')
        print(f'data ref: {id(self.data)}')
        print(self.data)


class child2_1(parent2):
    def print_data_ref(self):
        self.data.memory_usage()
        print(f'child1')
        print(f'data ref: {id(self.data)}')
        print(self.data)

    def add_item(self):
        # self.data.append({'Name': 'jacky', 'Age': 34,
        #                   'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)
        self.cnt += 1
        self.data[f'{self.cnt}'] = 1
        # self.data = self.data.append({'Name': 'jacky', 'Age': 34,
        #                               'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)


class child2_2(parent2):
    def print_data_ref(self):

        print(f'child2')
        print(f'data ref: {id(self.data)}')
        print(self.data)


class child3:
    def __init__(self):
        students = [('jack', 34, 'Sydeny', 'Australia'),
                    ('Riti', 30, 'Delhi', 'India'),
                    ('Vikas', 31, 'Mumbai', 'India'),
                    ('Neelu', 32, 'Bangalore', 'India'),
                    ('John', 16, 'New York', 'US'),
                    ('Mike', 17, 'las vegas', 'US')]
        self.data = pd.DataFrame(students, columns=[
                                 'Name', 'Age', 'City', 'Country'], index=['a', 'b', 'c', 'd', 'e', 'f'])

        self.cnt = 0

    def add_item(self):
        # self.data.append({'Name': 'jacky', 'Age': 34,
        #                   'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)
        self.cnt += 1
        self.data[f'{self.cnt}'] = 1


for i in range(3):
    print(h.heap().size)

mode = 3
if mode == 1:
    print(h.heap().size)
    c1 = child1_1()
    print(h.heap().size)
    c2 = child1_2()
    print(h.heap().size)
    c3 = child1_1()
    print(h.heap().size)
    c4 = child1_2()
    print(h.heap().size)
    c5 = child1_1()
    print(h.heap().size)
    c6 = child1_2()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c3.add_item()
    print(h.heap().size)
    c5.add_item()
    print(h.heap().size)
    for i in range(50):
        c1.add_item()
        print(h.heap().size)
        c3.add_item()
        print(h.heap().size)
        c5.add_item()
        print(h.heap().size)


elif mode == 2:
    print(h.heap().size)

    students = [('jack', 34, 'Sydeny', 'Australia'),
                ('Riti', 30, 'Delhi', 'India'),
                ('Vikas', 31, 'Mumbai', 'India'),
                ('Neelu', 32, 'Bangalore', 'India'),
                ('John', 16, 'New York', 'US'),
                ('Mike', 17, 'las vegas', 'US')]
    data = pd.DataFrame(students, columns=['Name', 'Age', 'City', 'Country'], index=[
                        'a', 'b', 'c', 'd', 'e', 'f'])

    c1 = child2_1(data)
    print(h.heap().size)
    c2 = child2_2(data)
    print(h.heap().size)
    c3 = child2_1(data)
    print(h.heap().size)
    c4 = child2_2(data)
    print(h.heap().size)
    c5 = child2_1(data)
    print(h.heap().size)
    c6 = child2_2(data)
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c3.add_item()
    print(h.heap().size)
    c5.add_item()
    print(h.heap().size)
    for i in range(50):
        c1.add_item()
        print(h.heap().size)
        c3.add_item()
        print(h.heap().size)
        c5.add_item()
        print(h.heap().size)

elif mode == 3:
    print(h.heap().size)
    c1 = child3()
    print(h.heap().size)
    c2 = child3()
    print(h.heap().size)
    c3 = child3()
    print(h.heap().size)
    c4 = child3()
    print(h.heap().size)
    c5 = child3()
    print(h.heap().size)
    c6 = child3()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c1.add_item()
    print(h.heap().size)
    c3.add_item()
    print(h.heap().size)
    c5.add_item()
    print(h.heap().size)
    for i in range(50):
        c1.add_item()
        print(h.heap().size)
        c3.add_item()
        print(h.heap().size)
        c5.add_item()
        print(h.heap().size)


# print(h.heap().size)
# students = [('jack', 34, 'Sydeny', 'Australia'),
#             ('Riti', 30, 'Delhi', 'India'),
#             ('Vikas', 31, 'Mumbai', 'India'),
#             ('Neelu', 32, 'Bangalore', 'India'),
#             ('John', 16, 'New York', 'US'),
#             ('Mike', 17, 'las vegas', 'US')]
# data = pd.DataFrame(students, columns=[
#     'Name', 'Age', 'City', 'Country'], index=['a', 'b', 'c', 'd', 'e', 'f'])

# students2 = [('jack', 34, 'Sydeny', 'Australia'),
#              ('Riti', 30, 'Delhi', 'India'),
#              ('Vikas', 31, 'Mumbai', 'India'),
#              ('Neelu', 32, 'Bangalore', 'India'),
#              ('John', 16, 'New York', 'US'),
#              ('Mike', 17, 'las vegas', 'US')]
# data2 = pd.DataFrame(students, columns=[
#     'Name', 'Age', 'City', 'Country'], index=['a', 'b', 'c', 'd', 'e', 'f'])
# # print(f'data id: {id(data)}')

# c1 = child1(data)
# print(h.heap().size)
# c2 = child2(data)
# print(h.heap().size)
# c3 = child1(data)
# print(h.heap().size)
# c4 = child2(data)
# print(h.heap().size)
# # c1.print_attr()
# # c2.print_attr()
# # c1.print_data_ref()
# # c2.print_data_ref()
# c1.add_item()
# # print(h.heap())
# print(h.heap().size)
# # c1.print_data_ref()
# # c2.print_data_ref()
# # # c1.print_attr()
# # # c2.print_attr()
# # data = data.append({'Name': 'jerry', 'Age': 10,
# #                     'City': 'Sydeny', 'Country': 'Australia'}, ignore_index=True)
# # alldfs = [eval(var) for var in dir() if isinstance(
# #     eval(var), pd.core.frame.DataFrame)]
# # print(f'data id: {eval(id(data))}')
# # print(dir())
# # alldfs = [var for var in dir() if isinstance(
# #     eval(var), pd.core.frame.DataFrame)

# # print(alldfs)  # df1, df2
