def unlimited_arguments(*args):
    print(f"Arguments received: {args}")
    for argument in args:
        print(argument)

unlimited_arguments(*["Hello", "World", 123])