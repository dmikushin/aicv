import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union

class PersonalInfoFormatter(ABC):
    def __init__(self, personal_info: Dict[str, Any]):
        self.personal_info = personal_info or {}

    def format_first_name(self) -> str:
        return self.personal_info.get('first_name', '')

    def format_family_name(self) -> str:
        return self.personal_info.get('family_name', '')

    def format_name(self) -> str:
        return f"{self.format_first_name()} {self.format_family_name()}"

    def format_date_of_birth(self) -> str:
        return self.personal_info.get('date_of_birth', '')

    @abstractmethod
    def format_github(self) -> str:
        pass

    @abstractmethod
    def format_linkedin(self) -> str:
        pass

    @abstractmethod
    def format_email(self) -> str:
        pass

    @abstractmethod
    def format_phone(self) -> str:
        pass

    @abstractmethod
    def format_address(self) -> str:
        pass

    def has_phd(self) -> bool:
        degree = self.personal_info.get("degree", "")
        has_phd = False
        if (degree == 'PhD') or (degree == 'Ph.D') or (degree == 'Ph.D.'):
            has_phd = True
        return has_phd

    def format_field(self, field: str) -> str:
        value = str(self.personal_info.get(field, "") or "")
        if not value:
            return ""
        if field == 'name':
            return self.format_name(value)
        if field == 'first_name':
            return self.format_first_name(value)
        if field == 'family_name':
            return self.format_family_name(value)
        if field == 'name':
            return self.format_name(value)
        if field == 'date_of_birth':
            return self.format_date_of_birth(value)
        elif field == 'website':
            return self.format_website(value)
        elif field == 'github':
            return self.format_github(value)
        elif field == 'linkedin':
            return self.format_linkedin(value)
        elif field == 'email':
            return self.format_email(value)
        elif field == 'phone':
            return self.format_phone(value)
        elif field == 'address':
            return self.format_address(value)
        else:
            return value

    @staticmethod
    def parse_website_info(website):
        if not website:
            return "", ""
        if isinstance(website, dict):
            website_url = website.get('url', '')
        else:
            website_url = website
        website_text = re.sub(r'^.*?://', '', website_url)
        return website_text, website_url

    @staticmethod
    def parse_social_info(value, base_url, handle_prefix='@', path_segment=None):
        """
        Extracts username and constructs URL for social profiles.

        Args:
            value (str): The input value (URL, username, or @username).
            base_url (str): The base URL for the service (e.g., 'https://github.com/').
            handle_prefix (str): Prefix for handle (default '@').
            path_segment (str): Optional path segment to strip (e.g., 'github.com/', 'linkedin.com/in/').

        Returns:
            tuple: (username, url)
        """
        if not value:
            return "", ""
        value = value.strip()
        username = value
        if path_segment and path_segment in value:
            username = value.split(path_segment)[-1].strip('/')
        elif value.startswith(handle_prefix):
            username = value.lstrip(handle_prefix)
        # Remove any trailing slashes
        username = username.strip('/')
        url = f"{base_url}{username}"
        return f'{handle_prefix}{username}', url
