#1
import datetime
a = datetime.datetime.now()
print(a)

import datetime
x=datetime.datetime.now()
n=x-datetime.timedelta(days=1)
print(n)

#2
import datetime
a = datetime.datetime.now()
print(a.year)
print(a.strftime("%A"))

import datetime
x=datetime.datetime.now()
n=x-datetime.timedelta(days=1)
print(n)
a=x+datetime.timedelta(days=1)
print(a)


#3
import datetime
x = datetime.datetime(2026, 2, 27)
print(x.strftime('%d'))

import datetime
a = datetime.datetime.now()
print(a.replace(microsecond=0))


#4
import datetime
x = datetime.datetime(2026, 2, 27)
print(x.strftime("%B"))

import datetime
x = datetime.datetime(2026, 2, 27)
y= datetime.datetime(2026, 3, 24)
a=x-y
print(a)


#5
import datetime
a = datetime.datetime.now()
print(a.strftime("%G"))

