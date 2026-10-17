from datetime import date

from django.shortcuts import render


def index(request):
    # All personal information is passed to the template through this dictionary, my info is not 100% corect to protect my data Online as much as posipole .
    context = {
        'first_name': 'ahmed',  # Lowercase so capfirst visibly changes it.
        'last_name': 'Wael',
        'student_id': 120230395,
        'address': 'Gaza',
        'email': '',  # Empty on purpose to demonstrate the default filter.
        'date_of_birth': date(2004, 6, 12),  # year, month, day: 12 June 2004.
    }
    return render(request, 'pages/index.html', context)
