class Book():
    id=None
    name=None
    price=None

    def __str__(self):
        return "id:%s  name:%s  price:%s" %(self.id , self.name , self.price)