import random
from datetime import datetime, timedelta

print('random 0 to 1')
print(random.random())
print('random 1 to 10')
print(random.randint(1, 10))

start = datetime(2000, 1, 1, 0, 0, 0)
end = datetime(2030, 12, 31, 23, 59, 59)

delta = end - start
random_seconds = random.randint(0, int(delta.total_seconds()))

random_datetime = start + timedelta(seconds=random_seconds)

print(f'random datetime between {start} and {end}')
print(random_datetime)