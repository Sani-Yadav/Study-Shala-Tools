import sys
import os

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

print(f"Current working directory: {os.getcwd()}")
print(f"Project root: {project_root}")

# Try to import the module
try:
    print("\nTrying to import media_downloader...")
    import media_downloader
    print(f"Success! media_downloader module path: {media_downloader.__file__}")
    
    print("\nContents of media_downloader:", dir(media_downloader))
    
    print("\nTrying to import downloader from media_downloader...")
    from media_downloader import downloader
    print(f"Success! downloader module path: {downloader.__file__}")
    
    print("\nContents of downloader:", dir(downloader))
    
except ImportError as e:
    print(f"\nImport error: {e}")
    print("\nPython path:")
    for i, path in enumerate(sys.path, 1):
        print(f"{i}. {path}")
    
    print("\nContents of project root:")
    for item in os.listdir(project_root):
        print(f"- {item}")
        
    print("\nContents of media_downloader directory:")
    media_downloader_path = os.path.join(project_root, 'media_downloader')
    if os.path.exists(media_downloader_path):
        for item in os.listdir(media_downloader_path):
            print(f"- {item}")
    else:
        print(f"Directory not found: {media_downloader_path}")
