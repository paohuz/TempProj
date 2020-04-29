class Singleton:
    instance = None

    @classmethod
    def Instance(cls):
        if cls.instance == None:
            cls.instance = Singleton()
        return cls.instance

    def __init__(self):
        if self.instance != None:
            raise ValueError('A Singleton instance is already existing')

    def setData(self, num):
        self.data = num

    def getData(self):
        return self.data


obj = Singleton.Instance().setData(10)
print(f'data = {Singleton.Instance().getData()}')
