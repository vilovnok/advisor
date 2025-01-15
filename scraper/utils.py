import re

class Mixin:
    def extract_and_remove_url(self, content):
        url_pattern = r'url:\s*(https?://\S+)'
        match = re.search(url_pattern, content)
        url = match.group(1) if match else None
        cleaned_text = re.sub(url_pattern, '', content).strip()

        return url, cleaned_text