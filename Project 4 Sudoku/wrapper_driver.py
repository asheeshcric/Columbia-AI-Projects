import os

path_for_script = os.path.abspath('driver_3.py')
file = open('sudokus_start.txt', 'r')
for line in file:
    os.system("python3 driver_3.py " + line)
