from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta
from bl_booking.models import bl_booking
from bl_booking.models import contact
import icalendar
import urllib
from icalendar import Calendar, Event

# return calendar info
def ical():
    ics = urllib.urlopen("http://calendars.office.microsoft.com/pubcalstorage/x2lrxl7z4630721/Dylan_Bray_Calendar.ics").read()
    events = []

    cal = Calendar.from_ical(ics)
    
    for event in cal.walk('vevent'):
       # to_zone = tz.gettz('America/Regina')

        date = event.get('dtstart').dt
        end = event.get('dtend').dt

        events.append({
                'start': date.strftime("%Y-%m-%d %H:%M"),
                'end': end.strftime("%Y-%m-%d %H:%M"),
                })

    return events

def getWeek(currentDate):
    weekDay = currentDate.isoweekday()
    return  [( currentDate - timedelta(days =  weekDay - 1)),
            ( currentDate - timedelta(days =  weekDay - 2)),
            ( currentDate- timedelta(days =  weekDay - 3)),
            ( currentDate - timedelta(days =  weekDay - 4)),
            ( currentDate - timedelta(days =  weekDay - 5)),
            ( currentDate - timedelta(days =  weekDay - 6)),
            ( currentDate - timedelta(days =  weekDay - 7))]
 
def buildTable(week):

    table = '<table id="bl-table">'
    table += '<caption><a id="prevWeek" href="/schedule/' + (week[0] - timedelta(days = 7)).strftime("%Y-%m-%d") + '">'
    table += '<img src="" alt="Previous" title="Previous Week">'
    table +='</a><a href="/schedule">Current Week</a><a id="nextWeek" href="/schedule/' + (week[0] + timedelta(days = 7)).strftime("%Y-%m-%d") + '">'
    table += '<img src="" alt="Next" title="Next Week"></a></caption>'
    table += '<thead>'
    table += '<tr>'
    table += '<th>Date</th><th>shift</th><th>05B1-1</th><th>05ID-2</th><th>local contact</th>'
    table += '</tr>'
    table += '</thead>'
    table += '<tbody>'
    
    for weekday in week:
        
        list_bookings = bl_booking.objects.filter(date__exact=weekday).values()
        contacts = contact.objects.filter(day__exact=weekday).values()
        table += '<tr>'
        table += '<td rowspan="3">' + weekday.strftime("%a %b %d/%y") +'</td><td>08:00-16:00</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '08:00-16:00' and booking['beamline'] == '05B1-1':
                table += booking['user']
        table += '</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '08:00-16:00' and booking['beamline'] == '05ID-2':
                table += booking['user']
        table += '</td><td rowspan="3">'
        for cont in contacts:
            if weekday == cont['day']:
                table += cont['name']
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
	table += '<td>16:00-24:00</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '16:00-24:00' and booking['beamline'] == '05B1-1':
                table += booking['user']
        table += '</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '16:00-24:00' and booking['beamline'] == '05ID-2':
                table += booking['user']
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
        table += '<td>00:00-08:00</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '00:00-08:00' and booking['beamline'] == '05B1-1':
                table += booking['user']
        table += '</td><td>'
        for booking in list_bookings:
            if weekday == booking['date'] and booking['time_slot'] == '00:00-08:00' and booking['beamline'] == '05ID-2':
                table += booking['user']
        table += '</td></tr>'
      
    table += '</tbody></table>'
    return table
    
def index(request):
    currentDate =  date.today()
    context = {'table': buildTable(getWeek(currentDate))}
    return render(request, 'bl_booking/base.html', context)

def week(request, year, month, day):
    currentDate = getWeek(date(int(year), int(month), int(day)))
    context = {'table': buildTable(currentDate)}
    return render(request, 'bl_booking/base.html', context)
    
