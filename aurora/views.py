from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime, time
from ical.utils import icalParse, tdColour, getWeek
from django.views.decorators.cache import cache_page

calendarFile = '/webroot/bmit/bmit/static/aurora.ics'

def buildTimes(week):
    zero = []
    one = []
    two = []
    three = []
    four = []
    five = []
    six = []
    seven = []
    eight = []
    nine = []
    ten =[]
    eleven = []
    twelve = []
    thirteen = []
    fourteen = []
    fifteen = []
    sixteen = []
    seventeen = []
    eighteen = []
    nineteen =[]
    twenty = []
    twentyone = []
    twentytwo = []
    twentythree = []

  
    
    for i in range(0,7):
        zero.append(datetime.combine(week[i], time(0)))
        one.append(datetime.combine(week[i], time(1)))
        two.append(datetime.combine(week[i], time(2)))
        three.append(datetime.combine(week[i], time(3)))
        four.append(datetime.combine(week[i], time(4)))
        five.append(datetime.combine(week[i], time(5)))
        six.append(datetime.combine(week[i], time(6)))
        seven.append(datetime.combine(week[i], time(7)))
        eight.append(datetime.combine(week[i], time(8)))
        nine.append(datetime.combine(week[i], time(9)))
        ten.append(datetime.combine(week[i], time(10)))
        eleven.append(datetime.combine(week[i], time(11)))
        twelve.append(datetime.combine(week[i], time(12)))
        thirteen.append(datetime.combine(week[i], time(13)))
        fourteen.append(datetime.combine(week[i], time(14)))
        fifteen.append(datetime.combine(week[i], time(15)))
        sixteen.append(datetime.combine(week[i], time(16)))
        seventeen.append(datetime.combine(week[i], time(17)))
        eighteen.append(datetime.combine(week[i], time(18)))
        nineteen.append(datetime.combine(week[i], time(19)))
        twenty.append(datetime.combine(week[i], time(20)))
        twentyone.append(datetime.combine(week[i], time(21)))
        twentytwo.append(datetime.combine(week[i], time(22)))
        twentythree.append(datetime.combine(week[i], time(23)))
       

    return {'zero': zero,
            'one': one,
            'two': two,
            'three': three,
            'four': four,
            'five': five,
            'six' : six,
            'seven': seven,
            'eight': eight,
            'nine': nine,
            'ten': ten,
            'eleven': eleven,
            'twelve': twelve,
            'thirteen': thirteen,
            'fourteen': fourteen,
            'fifteen': fifteen,
            'sixteen': sixteen,
            'seventeen': seventeen,
            'eighteen': eighteen,
            'nineteen': nineteen,
            'twenty': twenty,
            'twentyone': twentyone,
            'twentytwo': twentytwo,
            'twentythree': twentythree,
            }

#@cache_page(60 * 15)   
def index(request):
    currentDate =  getWeek(date.today())
    previousWeek = currentDate[0] - timedelta(days=7)
    nextWeek = currentDate[0] + timedelta(days=7)
    context = {'weektime': buildTimes(currentDate),
               'events': icalParse(calendarFile),
               'previousWeek': previousWeek,
               'nextWeek': nextWeek}
    #return render(request, 'aurora/base.html', context)
    return 'aurora/base.html',context

#cache_page(60 * 15)
def week(request, year, month, day):
    currentDate = getWeek(date(int(year), int(month), int(day)))
    previousWeek = currentDate[0] - timedelta(days=7)
    nextWeek = currentDate[0] + timedelta(days=7)
    context = {'weektime': buildTimes(currentDate),
               'events': icalParse(calendarFile),
               'previousWeek': previousWeek,
               'nextWeek': nextWeek}
    return 'aurora/base.html', context
