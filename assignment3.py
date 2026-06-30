# create a list of "person" dictionaries with name, age, and list of hobbies
people = [
    {
        'name': 'John',
        'age': 30,
        'hobbies': ['reading', 'hiking', 'cooking']
    },
    {
        'name': 'Sue',
        'age': 25,
        'hobbies': ['gaming', 'cycling']
    },
    {
        'name': 'Charlie',
        'age': 35,
        'hobbies': ['swimming', 'traveling']
    }
]
# print list of names
print("2)", [person['name'] for person in people])

# check if all are over 20
print("3)", all([person['age'] > 20 for person in people]), "All are over 20")

# copy such that you can change the name
copy = [person.copy() for person in people]
copy[0]['name'] = 'Mike'
print("4)", [person['name'] for person in copy])
print("4) Original list:", [person['name'] for person in people])

# unpack people into individual variables
person1, person2, person3 = people
print("5)\n", person1['name'], '\n', person2['name'], '\n', person3['name'])