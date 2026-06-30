names = ['alice', 'bob', 'charlie', 'dave', 'natasha', 'Norman']

print('The for loop')
for name in names:
    if (len(name) > 5) and (('n' in name) or ('N' in name)):
        print(f"{name} is {len(name)} long")

print('\nThe while loop')
while len(names) > 0:
    name = names.pop()
    print(f"Goodbye {name}")