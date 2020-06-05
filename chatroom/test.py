import random

list1=[random.randint(0,10) for i in range(50)]

for i in range(5):
    print(list1[10*i:(i+1)*10])

for i in range(10):
    number=list1.count(i)
    print(f"{i}的次数是{number}")