from datetime import datetime
from calendar import month_abbr

current_month = datetime.now().month
current_year = datetime.now().year

# def get_forward_month_list():
#     month = datetime.now().month   # current month number
#     return month_abbr[month:] + month_abbr[1:month]
#
# print(get_forward_month_list())

print(current_year)
print(current_month)

print(month_abbr[current_month])
