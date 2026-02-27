import json
import sys

def patch_json(source, patch):
    for key, val in patch.items():
        if val is None:
            # Егер patch мәні null болса → бастапқыдан өшіру
            if key in source:
                del source[key]
        elif isinstance(val, dict) and isinstance(source.get(key), dict):
            # Егер екі мән де JSON объектісі → рекурсивті патч
            patch_json(source[key], val)
        else:
            # Әйтпесе → ауыстыру немесе қосу
            source[key] = val
    return source

# Енгізу
source_json = json.loads(sys.stdin.readline())
patch_json_obj = json.loads(sys.stdin.readline())

# Патч қолдану
result = patch_json(source_json, patch_json_obj)

# Лексикографиялық сұрыптап шығару
print(json.dumps(result, sort_keys=True, separators=(',', ':')))







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