"""File that starts the program

Induces controller.py
"""

from controllers.user_controller import login
from interface_09 import *

def reading_ascii(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)

reading_ascii('docs/images/ascii_image_2.txt')

print("\nWelcome to Snaver!")
login()
menu()


