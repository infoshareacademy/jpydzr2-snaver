"""File that starts the program

Induces controller.py
"""

from controllers.user_controller import login


def reading_ascii(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)


reading_ascii('docs/images/ascii_image_2.txt')

print("\nWelcome to Snaver!")

login = login()
global_user_id = login[0]
global_user_name = login[1]

# Run the file "controller.py"
import controller
controller

