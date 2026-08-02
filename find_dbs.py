import os

print("=" * 60)
print("SEARCHING FOR ALL DB.SQLITE3 FILES ON SERVER")
print("=" * 60)

for root, dirs, files in os.walk('/home/KampungSipias/'):
    # Lewati folder virtualenvs untuk mempercepat pencarian
    if '.virtualenvs' in root or '.cache' in root:
        continue
    for f in files:
        if f == 'db.sqlite3':
            db_path = os.path.join(root, f)
            try:
                print(f"Database found: {db_path} | Size: {os.path.getsize(db_path) / 1024:.2f} KB | Modified: {os.path.getmtime(db_path)}")
            except Exception as e:
                print(f"Database found: {db_path} | Error: {e}")
                
print("=" * 60)
