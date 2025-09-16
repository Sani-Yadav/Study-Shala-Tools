import sys
import os

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
print(f"Project root: {project_root}")
sys.path.insert(0, project_root)

# Print Python path
print("\nPython path:")
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")

# Check if media_downloader directory exists
media_downloader_path = os.path.join(project_root, 'media_downloader')
print(f"\nChecking if media_downloader exists at: {media_downloader_path}")
if os.path.exists(media_downloader_path):
    print("media_downloader directory exists!")
    print("Contents of media_downloader directory:")
    for item in os.listdir(media_downloader_path):
        print(f"  - {item}")
    
    # Try to import the module
    try:
        import importlib.util
        
        # Try to import the module directly
        print("\nTrying to import media_downloader.downloader.test_view...")
        from media_downloader.downloader import test_view
        print("Successfully imported media_downloader.downloader.test_view")
        print(f"Test view function: {test_view.test_view}")
        
    except ImportError as e:
        print(f"\nImport error: {e}")
        print("\nTrying to import just media_downloader...")
        try:
            import media_downloader
            print(f"Successfully imported media_downloader from: {media_downloader.__file__}")
        except ImportError as e2:
            print(f"Failed to import media_downloader: {e2}")
            
            # Check if media_downloader has __init__.py
            init_path = os.path.join(media_downloader_path, '__init__.py')
            print(f"\nChecking for __init__.py at: {init_path}")
            if os.path.exists(init_path):
                print("__init__.py exists!")
            else:
                print("__init__.py is missing! Creating it...")
                with open(init_path, 'w') as f:
                    f.write("# This is a Python package")
else:
    print("media_downloader directory does not exist at the expected location!")
