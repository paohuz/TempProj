class AbstractProduct:
    def use_product(self):
        raise NotImplementedError('use_product() must be defined in subclass')


class ConcreteProduct(AbstractProduct):
    def use_product(self):
        print('Inside ConcreteProduct:use_product()')


class AbstractCreator:
    def factory_method(self):
        raise NotImplementedError(
            'factory_method() must be defined in subclass')

    def operation(self):
        self.product = self.factory_method()
        return self.product


class ConcreteCreator(AbstractCreator):
    def factory_method(self):
        return ConcreteProduct()


prodCreator = ConcreteCreator()
prod = prodCreator.operation()
prod.use_product()
