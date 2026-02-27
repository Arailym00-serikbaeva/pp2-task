#1
import datetime
a = datetime.datetime.now()
print(a)

#2
import datetime
a = datetime.datetime.now()
print(a.year)
print(a.strftime("%A"))

#3
import datetime
x = datetime.datetime(2026, 2, 27)
print(x.strftime('%d'))

#4
import datetime
x = datetime.datetime(2026, 2, 27)
print(x.strftime("%B"))

#5
import datetime
a = datetime.datetime.now()
print(a.strftime("%G"))

