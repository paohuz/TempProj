class parent:
    def __init__(self, a):
        self.a = a

    def action1(self):
        raise NotImplementedError('action1() must be defined in subclass')


class child(parent):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

    def action1(self, act):
        print(f'a: {self.a} b: {self.b} act:{act}')


c1 = child(1, 2)
c1.action1('hello')
