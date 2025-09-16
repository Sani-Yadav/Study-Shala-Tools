print("Python is working!")
print(f"Python version: {__import__('sys').version}")
print(f"Current directory: {__import__('os').getcwd()}")
try:
    import django
    print(f"Django version: {django.__version__}")
except ImportError:
    print("Django is not installed")
