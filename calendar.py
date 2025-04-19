import time
import re


# Everything technically lines up correctly
# The only thing wrong is that sometimes something gets off with the Fill out the first week bit
#   where blank calendar spaces will be weird, as well as having non dates filled in (-2, -1, 0)
# The actual start dates and end dates line up correctly with a real calendar (:

from math import ceil

calendar = {
    "January": 31,
    "February": 28,  # 29 for leap years
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31
}
month_start_day = 3
days = ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa']
pad_size = 5

for month in calendar:
    print(f"\n\n{month.center(100)}", sep='')
    for day in days:
        print(str('|'.ljust(pad_size) + day + '|'.rjust(pad_size)).center(pad_size * 3), end='')
    print()

    # Fill in the blank days at the start of the month
    for i in range(month_start_day):
        print(str('|' + str('').center(pad_size * 2) + '|').center(pad_size * 3), end='')

    # Fill out first week
    for i in range(7 - month_start_day):
        print(str('|' + str(i + 1).center(pad_size * 2) + '|').center(pad_size * 3), end='')
    print()

    # Fill out the rest of the month
    for i in range(7 - month_start_day, calendar[month]):
        print(str('|' + str(i + 1).center(pad_size * 2) + '|').center(pad_size * 3), end='')
        if (i + month_start_day + 1) % 7 == 0:
            print()

    # if > 7, loop back to 0
    if month_start_day > 7:
        month_start_day = (calendar[month] % 7 + month_start_day) % 7
    else:
        month_start_day = calendar[month] % 7 + month_start_day

# Next section gets local time and user to input a date in 2025 to output how many months and days til that date

while True:
    # dumb 1 liner. Gets the current date [mm, dd] as a list of ints to use for the comparison
    current_date = [int(x) for x in time.strftime("%m %d", time.localtime()).split(' ')]
    current_date = {'month': current_date[0], 'day': current_date[1]}

    # split on '/' or space(' ')
    search_date = []
    while not search_date:
        search_date = re.split('/|\s',input("\n\nEnter future date from 2025 to see how long til its that date? (mm/dd/yy)"))
        if (len(search_date[0]) > 2 or len(search_date[1]) > 2 or int(search_date[0]) > 12 or int(search_date[1]) > 31
                or len(search_date) > 3):
            print("Not a valid date")
            search_date = []
            continue
        try:
            search_date = [int(x) for x in search_date]
            search_date = {'month': search_date[0], 'day': search_date[1]}
        except ValueError:
            print("Not a valid date")
            search_date = []
    til_date = {'month': '', 'months': 0, 'days': 0, 'total_days': 0}

    # Dictionary with number of month as key, month name as item ie 1: January, 2: February, etc
    calendar_month_with_number = {i + 1: month for i, month in enumerate(calendar.keys())}

    remainder_month = 0
    remainder_days = 0
    if current_date['day'] > search_date['day']:
        remainder_month = 1
        month_before_search = calendar_month_with_number[search_date['month'] - 1]
        remainder_days = calendar[month_before_search] - current_date['day'] + search_date['day']

    til_date['month'] = calendar_month_with_number[search_date['month']]
    til_date['months'] = search_date['month'] - current_date['month'] - remainder_month
    if remainder_days:
        til_date['days'] = remainder_days
    else:
        til_date['days'] = (calendar[til_date['month']] - current_date['day']) - (calendar[til_date['month']] - search_date['day'])
    print(f"It will be {til_date['months']} months and {til_date['days']} days until {til_date['month']} {search_date['day']}")


    local_time = time.strftime("%m/%d/%Y")
    local_time = local_time.split('/')
    local_time[0] = local_time[0].replace('0', '') if local_time[0][0] == '0' else local_time[0]
    local_time[1] = local_time[1].replace('0', '') if local_time[1][0] == '0' else local_time[1]
    local_time[0] += '/'
    local_time[1] += '/'
    local_time = ''.join(local_time)

    print(local_time)
