class test:
    public = 0
    def __init__(self):
        self.a=100
    def time(self):
        while True:
            self.a-=1
            if self.a==0:
                self.public+=1
                print(test.public)
                self.a=100

t1=test()
t1.time()

