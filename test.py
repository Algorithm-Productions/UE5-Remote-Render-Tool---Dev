import time
from datetime import datetime, timedelta, time

currtime = datetime.now()
addingtime = "20h:31m:24s"
addingtimeObj = datetime.strptime(addingtime, '%Hh:%Mm:%Ss')
a = timedelta(hours=addingtimeObj.hour, minutes=addingtimeObj.minute, seconds=addingtimeObj.second, microseconds=addingtimeObj.microsecond)
b = currtime + a

print(addingtimeObj)
print(currtime)
print(a)
print(b)


