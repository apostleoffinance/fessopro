#class
#class is the blueprint of the object

#Object
#Object is the instance of the class


#attribute

#class attribute # Common characteristic of a entity

#instance attribute - Unique for each object

#method - Any function that you create inside a class is called method

# __init__ method->constructor
# it is executed automatically when you create an object
#  __init__ function don't have to be called. 


class Student:
    #class attribute
    dress_code = 'black_white'
    school_name = 'xaviers' 
    subject = 'pcm'

    #instance attribute
    def __init__(self,name,gmail,roll_no): 
        self.name=name
        self.gmail=gmail
        self.roll_no=roll_no

    def about_me(self):
        return f'my name is {self.name}'


obj1 = Student('matt','matt@gmail.com', 55)
obj2 = Student('sam','sam@gmail.com',66)

print(obj1.name)
print(obj2.name)

print(obj1.about_me())
print(obj2.about_me())




class Book:

    def __init__(self, title, author, price, quantity):
        self.title=title
        self.author=author
        self.price=price
        self.quantity=quantity

    def get_price(self):
        return f'The book cost ${self.price}'
    
    def set_price(self, new_price):
        self.price=new_price

    def get_quantity(self):
        return self.quantity
    
    def set_quantity(self, new_quantity):
        self.quantity=new_quantity

    def sell(self, number_sold):
        self.quantity=self.quantity-number_sold

    def restock(self, number_added):
        self.quantity=self.quantity+number_added

    
p1 = Book(title='Java with Project', author='Dr.Sean', price=100.0, quantity= 3 )
p2 = Book(title='Calculus',author = 'Schaum',price = 30.0,quantity=1)

print(p1.price)
p1.set_price(30.0)
print(p1.price)







class BankAccount:
    bank_name='jpmorgan'

    def __init__(self, account_number, initial_balance):
        self.account_number=account_number
        self.balance=initial_balance

    def deposit(self, amount):
        if amount<0:
            print('invalid amount')
        else:
            self.balance=self.balance+amount

    def withdraw(self, amount):
        if amount<self.balance:
            self.balance=self.balance-amount
    
    def get_balance(self):
        return self.balance
    
my_account = BankAccount(account_number='12345678', initial_balance=1000)

# Deposit and Withdraw
my_account.deposit(500)
my_account.withdraw(200)
print(my_account.get_balance()) #Output: 1300

    