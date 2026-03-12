names = ["Ali", "Dana", "Aruzhan"]
scores = [80, 90, 85]

# 1
for i, name in enumerate(names):
    print(i, name)

# 2
for name, score in zip(names, scores):
    print(name, score)

# 3
for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)

# 4
print(list(enumerate(names)))

# 5
print(list(zip(names, scores)))