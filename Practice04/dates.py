#1
import datetime
a = datetime.datetime.now()
print(a)

import datetime
x=datetime.datetime.now()
<<<<<<< HEAD
n=x-datetime.timedelta(days=5)
=======
n=x-datetime.timedelta(days=1)
>>>>>>> 1249109 (Add Practice5 - Python RegEx and receipt parsing examples)
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

<<<<<<< HEAD
=======

>>>>>>> 1249109 (Add Practice5 - Python RegEx and receipt parsing examples)
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
<<<<<<< HEAD
x = datetime.datetime(2026, 2, 27,14,58,45)
y= datetime.datetime(2026, 3, 29,11,40,23)
a=y-x
print(a.total_seconds())
=======
x = datetime.datetime(2026, 2, 27)
y= datetime.datetime(2026, 3, 24)
a=x-y
print(a)

>>>>>>> 1249109 (Add Practice5 - Python RegEx and receipt parsing examples)

#5
import datetime
a = datetime.datetime.now()
print(a.strftime("%G"))

