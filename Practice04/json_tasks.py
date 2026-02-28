#1
import json
x =  '{ "name":"Aisha", "age":18, "city":"Shymkent"}'
y = json.loads(x)
print(y["age"])



#2
import json
x = {
  "name": "Aisha",
  "age": 18,
  "city": "Shymkent"
}
y = json.dumps(x)
print(y)

#3
json_string = '''
{
    "students": [
        {"name": "Ali", "grade": 90},
        {"name": "Aigerim", "grade": 95},
        {"name": "Nurlan", "grade": 85}
    ]
}
'''
data = json.loads(json_string)
for student in data["students"]:
    print(student["name"], "-", student["grade"])

#4
import json
data = {
    "product": "Laptop",
    "price": 350000,
    "in_stock": True
}
with open("product.json", "w") as file:
    json.dump(data, file, indent=4)
print("Файлға жазылды.")


#5
import json
with open("product.json", "r") as file:
    data = json.load(file)
print(data)
print(data["product"])





import json
with open("sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)

print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")

    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")
