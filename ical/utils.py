from datetime import date, timedelta, datetime, time, tzinfo
from icalendar import Calendar, Event


# return calendar info
def icalParse(url):
    #ics = urllib.urlopen(url).read()
    ics = open(url,'rb').read()
    events = []

    cal = Calendar.from_ical(ics)
    
    for event in cal.walk('vevent'):
        category = event.get('categories')
        start = event.get('dtstart').dt
        end = event.get('dtend').dt
        try:
            start = start.replace(tzinfo=None)
            end = end.replace(tzinfo=None)
        except:
            start = start
            end = end
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
