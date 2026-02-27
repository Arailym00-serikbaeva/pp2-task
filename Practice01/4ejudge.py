"""401
n=int(input())
for i in range(1,n+1):
    print(i**2)"""

"""402
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i
n = int(input().strip())
first = True
for num in even_numbers(n):
    if not first:
        print(",", end="")
    print(num, end="")
    first = False
"""

"""403
def divisible_numbers(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input().strip())
first = True
for num in divisible_numbers(n):
    if not first:
        print(" ", end="")
    print(num, end="")
    first = False
"""

"""404
a,b=map(int,input().split())
for i in range(a,b+1):
    print(i**2)
"""

"""405
n=int(input())
for i in range(-n,1):
    print(-i)
"""

"""406
def fibonacci_generator(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
n = int(input().strip())
first = True
for num in fibonacci_generator(n):
    if not first:
        print(",", end="")
    print(num, end="")
    first = False
"""

"""407
n=input()
a=n[::-1]
print(a)"""

"""408
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True
def prime_generator(n):
    for i in range(2, n + 1):
        if is_prime(i):
            yield i
n = int(input().strip())
first = True
for prime in prime_generator(n):
    if not first:
        print(" ", end="")
    print(prime, end="")
    first = False"""

"""409
n=int(input())
for i in range(0,n+1):
  print(2**i,end=" ")"""

"""410
a=input()
b=int(input())
for i in range(b):
  print(a,end=" ")"""

"""411
import json
import sys

def patch_json(source, patch):
    for key, val in patch.items():
        if val is None:
            if key in source:
                del source[key]
        elif isinstance(val, dict) and isinstance(source.get(key), dict):
            patch_json(source[key], val)
        else:
            source[key] = val
    return source


source_json = json.loads(sys.stdin.readline())
patch_json_obj = json.loads(sys.stdin.readline())

result = patch_json(source_json, patch_json_obj)

print(json.dumps(result, sort_keys=True, separators=(',', ':')))"""

"""412
import json
import sys
def deep_diff(old, new, path=""):
    diffs = []
    old_keys = set(old.keys()) if isinstance(old, dict) else set()
    new_keys = set(new.keys()) if isinstance(new, dict) else set()
    all_keys = old_keys.union(new_keys)
    for key in sorted(all_keys):
        sub_path = f"{path}.{key}" if path else key
        old_val = old.get(key) if isinstance(old, dict) else None
        new_val = new.get(key) if isinstance(new, dict) else None
        if key not in old_keys:

            diffs.append(f"{sub_path} : <missing> -> {json.dumps(new_val, separators=(',', ':'))}")
        elif key not in new_keys:
   
            diffs.append(f"{sub_path} : {json.dumps(old_val, separators=(',', ':'))} -> <missing>")
        elif isinstance(old_val, dict) and isinstance(new_val, dict):

            diffs.extend(deep_diff(old_val, new_val, sub_path))
        elif old_val != new_val:

            diffs.append(f"{sub_path} : {json.dumps(old_val, separators=(',', ':'))} -> {json.dumps(new_val, separators=(',', ':'))}")

    return diffs

old_json = json.loads(sys.stdin.readline())
new_json = json.loads(sys.stdin.readline())
diffs = deep_diff(old_json, new_json)
if diffs:
    for line in diffs:
        print(line)
else:
    print("No differences")
"""

"""413
import json
import sys
import re

def query_json(data, query):
    parts = re.findall(r'\w+|\[\d+\]', query)  # Кілттер мен индекстерді бөліп алу
    current = data
    try:
        for part in parts:
            if part.startswith('['):
                index = int(part[1:-1])
                current = current[index]
            else:
                current = current[part]
        return json.dumps(current, separators=(',', ':'))
    except (KeyError, IndexError, TypeError):
        return "NOT_FOUND"

# Енгізу
data = json.loads(sys.stdin.readline())
q_count = int(sys.stdin.readline())
queries = [sys.stdin.readline().strip() for _ in range(q_count)]
# Шешу
for q in queries:
    print(query_json(data, q))"""

"""414
from datetime import datetime, timedelta, timezone
import sys
import re

def parse_datetime(s):
    # Мысал: "2025-01-01 UTC+03:00"
    date_part, tz_part = s.strip().split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    # UTC+03:00 → (+/-)HH:MM
    match = re.match(r'UTC([+-])(\d{2}):(\d{2})', tz_part)
    sign = 1 if match[1] == '+' else -1
    hours = int(match[2])
    minutes = int(match[3])
    offset = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    return dt.replace(tzinfo=offset)

# Енгізу
t1 = parse_datetime(sys.stdin.readline())
t2 = parse_datetime(sys.stdin.readline())

# UTC-қа аудару
t1_utc = t1.astimezone(timezone.utc)
t2_utc = t2.astimezone(timezone.utc)

# Айырмашылықты толық күндерде есептеу
diff_days = abs((t2_utc.date() - t1_utc.date()).days)
print(diff_days)"""


"""414
from datetime import datetime, timedelta, timezone
import sys
import re

def parse_datetime(s):
    date_part, tz_part = s.strip().split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    match = re.match(r'UTC([+-])(\d{2}):(\d{2})', tz_part)
    sign = 1 if match[1] == '+' else -1
    hours = int(match[2])
    minutes = int(match[3])
    offset = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    return dt.replace(tzinfo=offset)

t1 = parse_datetime(sys.stdin.readline())
t2 = parse_datetime(sys.stdin.readline())

t1_utc = t1.astimezone(timezone.utc)
t2_utc = t2.astimezone(timezone.utc)

diff_seconds = abs((t2_utc - t1_utc).total_seconds())
diff_days = int(diff_seconds // (24*3600))
print(diff_days)"""


"""415
"""

"""416
from datetime import datetime, timezone, timedelta
import sys
import re

def parse_datetime(s):
    dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    match = re.search(r'UTC([+-])(\d{2}):(\d{2})', s)
    sign = 1 if match[1] == '+' else -1
    hours = int(match[2])
    minutes = int(match[3])
    offset = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    return dt.replace(tzinfo=offset)

start = parse_datetime(sys.stdin.readline())
end = parse_datetime(sys.stdin.readline())
start_utc = start.astimezone(timezone.utc)
end_utc = end.astimezone(timezone.utc)
print(int((end_utc - start_utc).total_seconds()))"""



"""417
import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

discriminant = b*b - 4*a*c

if discriminant < 0:
    print("0.0000000000")
else:
    sqrt_d = math.sqrt(discriminant)
    t1 = (-b - sqrt_d)/(2*a)
    t2 = (-b + sqrt_d)/(2*a)
    t_low = max(0, min(t1, t2))
    t_high = min(1, max(t1, t2))
    if t_low > t_high:
        print("0.0000000000")
    else:
        length = math.hypot(dx, dy) * (t_high - t_low)
        print(f"{length:.10f}")"""

"""418
x0, y0 = map(float, input().split())
x1, y1 = map(float, input().split())
x = (x1 * y0 + x0 * y1) / (y0 + y1)
y = 0.0
print(f"{x:.10f} {y:.10f}")"""

"""419
"""

"""420
n = int(input())
g = 0
outern = 0
inn = 0
for _ in range(n):
    parts = input().split()
    scope, x = parts[0], int(parts[1])
    if scope == "global":
        g += x
    elif scope == "nonlocal":
        outern += x
    else:  # local
        inn += x
print(f"{g} {outern}")"""

"""421
import importlib
n = int(input())
for _ in range(n):
    module_path, attr_name = input().split()
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(mod, attr_name):
        print("ATTRIBUTE_NOT_FOUND")
    else:
        attr = getattr(mod, attr_name)
        if callable(attr):
            print("CALLABLE")
        else:
            print("VALUE")"""
