f = open('demo.txt', mode='a')
f.write('Hello, World!\n')
f.close()
# f = open('demo.txt', mode='r')
# print(f.read())

# file_content = f.readlines()
# f.close()
# for line in file_content:
#     print(line[:-1])

# line = f.readline()
# while line:
#     print(line[:-1])
#     line = f.readline()
# f.close()

with open('demo.txt', mode='r') as f:
    for line in f:
        print(line[:-1])