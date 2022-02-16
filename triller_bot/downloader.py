from requests import get

def download(url, filename):
    """
    Downloads a file from the given url and saves it to the given filename.
    """
    r = get(url, stream=True)
    
    if not r.ok:
        return False
    
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return True
class Downloader:

    download = download
                
    
