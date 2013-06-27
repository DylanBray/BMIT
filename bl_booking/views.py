from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime, time
from bl_booking.models import bl_booking
from bl_booking.models import contact
import icalendar
import urllib
from icalendar import Calendar, Event
from django.views.decorators.cache import cache_page


# returns an HTML class definition used for colouring the schedule table for each event in the calendar
# needed - throw exception when timeslot != 0, 8, or 16
def tdColour( events, weekday, timeSlot):
    
    if timeSlot == 16:
        dayincrement = 1
        endTime = 0
    else:
        dayincrement = 0
        endTime = timeSlot + 8

    def yellowCategory():
        return 'class="yellow"'

    def redCategory():
        return 'class="red"'

    def blueCategory():
        return 'class="blue"'

    def orangeCategory():
        return 'class="orange"'

    def purpleCategory():
        return 'class="purple"'
      
    def greenCategory():
        return 'class="green"'

    def none():
        return ''

    categories = { 'Yellow Category' : yellowCategory,
                   'Blue Category' :blueCategory,
                   'Red Category' : redCategory,
                   'Orange Category' : orangeCategory,
                   'Purple Category' : purpleCategory,
                   'Green Category' : greenCategory
                   }
    

    for event in events:
        if (event['start'] <= datetime.combine(weekday,time(timeSlot)) and event['end'] >= datetime.combine(weekday + timedelta(days = dayincrement), time(endTime))):
            try:
                return categories[event['category']]()
            except KeyError:
                return ''
    return ''
    
    
# return calendar info
def ical(url):
    #ics = urllib.urlopen(url).read()
    ics = open(url,'rb').read()
    events = []

    cal = Calendar.from_ical(ics)
    
    for event in cal.walk('vevent'):
       # to_zone = tz.gettz('America/Regina')
        category = event.get('categories')
        start = event.get('dtstart').dt
        end = event.get('dtend').dt
        if type(start) is date:
            start = datetime.combine(start, time(0,0,0))
        if type(end) is date:
            end = datetime.combine(end, time(0,0,0))
        subject = event.get('summary')
        events.append({
                'start': start,
                'end': end,
                'subject': subject,
                'category': category,
                })

    return events

# returns an array of the days of the current week beginning with Monday
def getWeek(currentDate):
    weekDay = currentDate.isoweekday()
    return  [( currentDate - timedelta(days =  weekDay - 1)),
            ( currentDate - timedelta(days =  weekDay - 2)),
            ( currentDate- timedelta(days =  weekDay - 3)),
            ( currentDate - timedelta(days =  weekDay - 4)),
            ( currentDate - timedelta(days =  weekDay - 5)),
            ( currentDate - timedelta(days =  weekDay - 6)),
            ( currentDate - timedelta(days =  weekDay - 7))]
 
# returns the schedule table
def buildTable(week):
   
    bmEvents = ical("/webroot/bmit/static/calendar.ics")
    table =  '<table id="bl-table">'
    table += '<caption><a id="prevWeek" href="/schedule/' + (week[0] - timedelta(days = 7)).strftime("%Y-%m-%d") + '">'
    table += '<img src="/static/cms/img/leftarrow.png" alt="Previous" title="Previous Week">'
    table +='</a><a href="/schedule">Current Week</a><a id="nextWeek" href="/schedule/' + (week[0] + timedelta(days = 7)).strftime("%Y-%m-%d") + '">'
    table += '<img src="/static/cms/img/rightarrow.png" alt="Next" title="Next Week"></a></caption>'
    table += '<thead>'
    table += '<tr>'
    table += '<th>Date</th><th>shift</th><th>05B1-1</th><th>05ID-2</th><th>local contact</th>'
    table += '</tr>'
    table += '</thead>'
    table += '<tbody>'
    
    for weekday in week:
        contacts = contact.objects.filter(day__exact=weekday).values()
        table += '<tr>'
        table += '<td rowspan="3">' + weekday.strftime("%a %b %d/%y") +'</td><td>00:00-08:00</td><td '
        table +=  tdColour(bmEvents, weekday, 0)+ ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(0)) and event['end'] >= datetime.combine(weekday,time(8))):
                table += event['subject']
        table += '</td><td>'
        #ID 0 - 8 goes here
        table += '</td><td rowspan="3">'
        for cont in contacts:
            if weekday == cont['day']:
                table += cont['name']
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
	table += '<td>08:00-16:00</td><td '
        table += tdColour(bmEvents, weekday, 8) + ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(8)) and event['end'] >= datetime.combine(weekday, time(16))):
                table += event['subject']
        table += '</td><td>'
        #ID 8 - 16 goes here
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
        table += '<td>16:00-24:00</td><td '
        table +=  tdColour(bmEvents, weekday, 16) + ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(16)) and event['end'] >= datetime.combine(weekday + timedelta(days = 1), time(0))):
                table += event['subject']
        table += '</td><td>'
        #ID 16 - 24 goes here
        table += '</td></tr>'
      
    table += '</tbody></table>'
    return table

@cache_page(60 * 15)   
def index(request):
    currentDate =  date.today()
    context = {'table': buildTable(getWeek(currentDate))}
    return render(request, 'bl_booking/base.html', context)
@cache_page(60 * 15)
def week(request, year, month, day):
    currentDate = getWeek(date(int(year), int(month), int(day)))
    context = {'table': buildTable(currentDate)}
    return render(request, 'bl_booking/base.html', context)
    
