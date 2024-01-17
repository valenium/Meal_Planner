import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render

def calendar_view(request, year=datetime.now().year, month=datetime.now().month):
    # Handling the previous and next month functionalities
    month = int(month)
    year = int(year)
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    # Use Python's calendar module to create the calendar
    my_calendar = calendar.Calendar(firstweekday=0)
    month_days = my_calendar.monthdayscalendar(year, month)

    context = {
        'month_days': month_days,
        'current_month': month,
        'current_year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'your_template.html', context)