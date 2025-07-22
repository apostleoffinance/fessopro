def operation(num1, num2):
    print(num1, num2)
    print(num1, num2)

# Positional Arguments
operation(4,3)

# Keyword Arguments
operation(num2=5,num1=10)


def outer():
    message = "I am outer"

    def inner():
        print(message)

    inner()

outer()


def modify_list(lst):
    lst.append(4)

my_list = [1,2,3]
modify_list(my_list)
print(my_list)


def modify_value(lst):
    x = 10

num = 5
modify_value(num)
print(num)