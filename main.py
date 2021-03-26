"""File that starts the program"""

from controllers.user_controller import login
from interface import *

reading_ascii('docs/images/ascii_image_2.txt')

print("\nWelcome to Snaver!")

try:
    user_id, user_name = login()
    while not user_id or not user_name:
        user_id, user_name = login()
        global_user_id = user_id
        global_user_name = user_name
    menu()
except KeyboardInterrupt as keyboard_exit:
    print('\nGood bye!')
    exit(0)
