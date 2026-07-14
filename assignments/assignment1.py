name = input("What is your name? ")
age = int(input("What is your age? "))

def say_hello():
    print(f"Hello {name}, you are {age} years old.")

def say_greetings(name, greeting='hello'):
    print(f"{greeting} {name}!")

def decades_old(age):
    return age // 10

say_hello()
say_greetings(name)
say_greetings(name, greeting='hi')
print(f"You are {decades_old(age)} decades old.")