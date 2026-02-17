
try:
    with open('warehouse_fields.txt', 'r', encoding='utf-16') as f:
        print(f.read())
except:
    # Try utf-8 just in case
    with open('warehouse_fields.txt', 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
