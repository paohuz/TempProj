class AbstractComponent:
    def Operation(self):
        raise NotImplementedError('Operation() must be defined in subclass')


class ConcreteComponent(AbstractComponent):
    def Operation(self):
        print('ConcreteComponent: Operation()')


class Decorator(AbstractComponent):
    def __init__(self, obj):
        self.comp = obj

    def Operation(self):
        print('Decorator:: Operation()')
        self.comp.Operation()


class ConcreteDecoratorA(Decorator):
    def __init__(self, obj):
        Decorator.__init__(self, obj)
        self.addedState = None

    def Operation(self):
        Decorator.Operation(self)
        self.addedState = 1
        print('ConcreteDecoratorA: Operation()')
        print(f'ConcreteDecoratorA: addedState = {self.addedState}')


class ConcreteDecoratorB(Decorator):
    def __init__(self, obj):
        Decorator.__init__(self, obj)

    def Operation(self):
        Decorator.Operation(self)
        print('ConcreteDecoratorB: Operation()')
        self.AddedBehavior()

    def AddedBehavior(self):
        print('ConcreteDecoratorB: AddedBehavior()')


myComponent = ConcreteDecoratorA(ConcreteDecoratorB(ConcreteComponent()))
myComponent.Operation()
