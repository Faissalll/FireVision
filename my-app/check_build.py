import os

path = r"d:\Semester 5\IPPL\LastwebFRv\FireVision\my-app\dist\assets\index-BV0XhJMs.js"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "http://localhost:5001" in content:
    print("✅ URL FOUND in build.")
else:
    print("❌ URL NOT FOUND in build.")
