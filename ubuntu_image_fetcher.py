import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path

def fetch_image():
    """
    Ubuntu-Inspired Image Fetcher
    Prompts user for an image URL, downloads it respectfully, and saves it to Fetched_Images directory
    """
    print("=" * 50)
    print("Ubuntu-Inspired Image Fetcher")
    print('"I am because we are"')
    print("=" * 50)
    
    # Prompt user for URL
    url = input("Please enter the URL of the image you wish to fetch: ").strip()
    
    if not url:
        print("No URL provided. Exiting with respect for your decision.")
        return
    
    # Create directory for community sharing
    directory = "Fetched_Images"
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Community directory '{directory}' is ready for sharing")
    except OSError as e:
        print(f"✗ Could not create directory: {e}")
        return
    
    # Respectfully attempt to fetch the image
    try:
        print("Connecting to the global community...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Verify we're getting an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print("✗ The provided URL does not point to an image resource.")
            print(f"Received content type: {content_type}")
            return
        
        # Extract filename from URL or generate one
        filename = extract_filename(url, content_type)
        filepath = os.path.join(directory, filename)
        
        # Save the image with respect for the shared resource
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully fetched and saved: {filename}")
        print(f"✓ The image is now available for community sharing in '{directory}/'")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not fetch the image: {e}")
        print("Please check the URL and your internet connection.")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")

def extract_filename(url, content_type):
    """
    Extract filename from URL or generate one based on content type
    """
    # Try to get filename from URL path
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)  # Handle URL-encoded characters
    filename = os.path.basename(path)
    
    # If no filename in URL, generate one
    if not filename or '.' not in filename:
        # Get extension from content type
        extension = content_type.split('/')[-1]
        if 'jpeg' in extension:  # Handle jpeg vs jpg convention
            extension = 'jpg'
        filename = f"community_image.{extension}"
    
    return filename

if __name__ == "__main__":
    fetch_image()