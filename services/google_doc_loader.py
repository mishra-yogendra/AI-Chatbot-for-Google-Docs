import requests
import re

def load_google_doc(doc_url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", doc_url)
    if not match:
        raise ValueError("Invalid Google Doc URL")

    doc_id = match.group(1)
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    response = requests.get(export_url)
    if response.status_code != 200:
        raise ValueError("Document not accessible. Make sure it's public.")

    return response.text.strip()
