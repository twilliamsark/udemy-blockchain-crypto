# 1) Write a function that accepts an other function as an argument
def call_function(func):
    print(f"Calling function {func}")
    func()

def say_hello():
    print("\tHello!")

call_function(say_hello)

# 2) Call your normal function by passing a lambda function
call_function(lambda: print("\tHello from lambda!"))

# 3) tweak your normal function to accept arguments and pass them along
def call_function_with_args(func, *args, **kwargs):
    print(f"Calling function {func} with arguments {args} and keyword arguments {kwargs}")
    func(*args, **kwargs)

def say_hello_to(name):
    print(f"\tHello, {name}!")

call_function_with_args(say_hello_to, "Alice")
call_function_with_args(say_hello_to, name="Bob")

# 4) center the name in a 20 character wide field

def say_hello_to(name):
    print(f"\tHello, {name:^20}!")

call_function_with_args(say_hello_to, "Alice")
call_function_with_args(say_hello_to, name="Bob")