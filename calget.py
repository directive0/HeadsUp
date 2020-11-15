from ics import *
import requests

# Change this URL to the URL of your desired Calendar!
url = "https://google.com/calendar/ical/students.uu.nl_plp5j8bh2qsjfloqi6qifsis28%40group.calendar.google.com/public/basic.ics"

# this class should act as a container for your calender
# you instantiate it once and then it loads the calendar into an object, parsed as individual events.
# the calendar then needs to be queried for updates


class CalendarPull(object):
    def __init__(self):
        try:
            self.cal = Calendar(requests.get(url).text)
        except:
            pass
    
    def SortEvents(self):
        self.eventstrings = []
        size = len(self.eventstoday)
        
        if size == 0:
            self.eventstrings = ["No Events Found"]
        else:
            for i in range(size):
                event = self.eventstoday[i]
                eventtime = event.begin
                eventtime = eventtime.to('est')
                self.eventstrings.append("'{}' at {}".format(event.name, eventtime.format('h:mm:ss A')))

            
            
    def GetTodaysEvents(self):
        # pull the events object out of cal and send them to SortEvents to produce a nice list with each event formatted for text display.
    
        self.events = self.cal.events
        
        self.eventstoday = self.events.today(True)
        
        self.SortEvents()
        
        return self.eventstrings
