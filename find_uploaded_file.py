import os

print("=" * 60)
print("SEARCHING FOR THE NEW UPLOADED FILE")
print("=" * 60)

target_suffix = "41bfe1"
found = False

for root, dirs, files in os.walk('/home/KampungSipias/'):
    if '.virtualenvs' in root or '.cache' in root:
        continue
    for f in files:
        if target_suffix in f:
            file_path = os.path.join(root, f)
            print(f"File found at: {file_path} | Size: {os.path.getsize(file_path) / 1024:.2f} KB")
            found = True

if not found:
    print(f"No file containing '{target_suffix}' was found on the server!")
print("=" * 60)
