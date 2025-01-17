# tableapp/utils.py

import os
import re
from urllib.parse import urlparse

def sanitize_filename(filename):
    """
    Sanitizes the filename to remove or replace unwanted characters.
    """
    filename = os.path.basename(filename)
    # Replace spaces with underscores and remove non-alphanumeric characters except underscores and hyphens
    filename = re.sub(r'[^A-Za-z0-9._-]', '_', filename)
    return filename.lower()

def get_s3_key(url):
    """
    Extracts the S3 object key from the external URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.path.lstrip('/')
