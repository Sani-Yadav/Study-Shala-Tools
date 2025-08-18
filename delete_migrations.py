import os

for root, dirs, files in os.walk('.'):
    if 'migrations' in root:
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(root, file))
            elif file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

print("✅ All migration files (except __init__.py) deleted.")
