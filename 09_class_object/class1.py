#class
#class is the blueprint of the object

#Object
#Object is the instance of the class


#attribute

#class attribute # Common characteristic of a entity

#instance attribute - Unique for each object


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


obj1 = Student('matt','matt@gmail.com', 55)
obj2 = Student('sam','sam@gmail.com',66)

print(obj1.name)
print(obj2.name)