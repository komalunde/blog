from datetime import datetime, date
from jinja2 import Markup
import time
#from app import date_unicode


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = datetime.fromtimestamp(int(timestamp))

    def render(self, format):
       return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))
    """s=time.strptime("20091229050936","%Y%m%d%H%M%s")
    print s.strftime('%H:%M %d %B %y(UTC)',s)
    s = datetime.strptime("20091229050936", "%Y%m%d%H%M%S")
    print("{:%H:%M %d %B %Y (UTC)}".format(s))"""


    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)


    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")