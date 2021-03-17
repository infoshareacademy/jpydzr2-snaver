"""File that starts the program

Induces controller.py
"""

from controllers.user_controller import login

def reading_ascii(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)

print("\nWelcome to Snaver!")
login()


