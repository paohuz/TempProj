class AbstractFactory:
    def CreateProduct1(self):
        raise NotImplementedError(
            'CreateProduct1() must be defined in subclass')

    def CreateProduct2(self):
        raise NotImplementedError(
            'CreateProduct2() must be defined in subclass')


class ConcreteFactory1(AbstractFactory):
    def CreateProduct1(self):
        return Product1_1()

    def CreateProduct2(self):
        return Product2_1()


class ConcreteFactory2(AbstractFactory):
    def CreateProduct1(self):
        return Product1_2()

    def CreateProduct2(self):
        return Product2_2()


class AbstractProduct1:
    def display(self):
        raise NotImplementedError('Display() must be defined in subclass')


class Product1_1(AbstractProduct1):
    def display(self):
        print('Inside Prodict1_1: Display()')


class Product1_2(AbstractProduct1):
    def display(self):
        print('Inside Prodict1_2: Display()')


class AbstractProduct2:
    def display(self):
        raise NotImplementedError('Display() must be defined in subclass')


class Product2_1(AbstractProduct2):
    def display(self):
        print('Inside Prodict2_1: Display()')


class Product2_2(AbstractProduct2):
    def display(self):
        print('Inside Prodict2_2: Display()')


factory1 = ConcreteFactory1()
prod1 = factory1.CreateProduct1()
prod1.display()
prod2 = factory1.CreateProduct2()
prod2.display()

factory2 = ConcreteFactory2()
prod1 = factory2.CreateProduct1()
prod1.display()
prod2 = factory2.CreateProduct2()
prod2.display()
