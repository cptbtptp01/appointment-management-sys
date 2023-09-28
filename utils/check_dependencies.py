import os

py_files = ['main.py', 'gui/custom_widgets.py', 'db/db_handler.py']

for file in py_files:
    # Read your Python code file(s)
    with open(file, 'r') as f:
        code_content = f.read()

    # Search for import statements in your code
    imported_packages = set()
    for line in code_content.split('\n'):
        if line.startswith('import ') or line.startswith('from '):
            package_name = line.split(' ')[1].split('.')[0]
            imported_packages.add(package_name)

    # Find packages that are in your code
    unused_packages = set(imported_packages)
    print(f"imported modules in {os.path.basename(file)}:", unused_packages)
