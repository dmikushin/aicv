import re
from aicv.backend.personal_info import PersonalInfoFormatter
from aicv.backend.emojis import EmojisFormatter

class EmojisFormatterMarkdown(EmojisFormatter):
    @staticmethod
    def add_section_emojis(content: str) -> str:
        content = re.sub(
            r'^(#) ([^#\n][^\n]*)$',
            lambda m: f'{m.group(1)} {EmojisFormatter.find_emoji(m.group(2))} {m.group(2)}',
            content,
            flags=re.MULTILINE
        )
        content = re.sub(
            r'^(##) ([^#\n][^\n]*)$',
            lambda m: f'{m.group(1)} {EmojisFormatter.find_emoji(m.group(2))} {m.group(2)}',
            content,
            flags=re.MULTILINE
        )
        return content

class PersonalInfoFormatterMarkdown(PersonalInfoFormatter):
    def format_website(self) -> str:
        website = self.personal_info.get('website', '')
        website_text, _ = parse_website_info(website)
        if not website_text:
            return ""
        return f"[{website_text}]({website_url})"

    def format_linkedin(self) -> str:
        linkedin = self.personal_info.get('linkedin', '')
        linkedin_text, linkedin_url = parse_social_info(linkedin, "https://www.linkedin.com/in/", "@", "linkedin.com/in/")
        return f"[{linkedin_text}]({linkedin_url})"

    def format_github(self) -> str:
        github = self.personal_info.get('github', '')
        github_text, github_url = parse_social_info(github, "https://github.com/", "@", "github.com/")
        return f"[{github_text}]({github_url})"

    def format_email(self) -> str:
        email = self.personal_info.get('email', '')
        if not email:
            return ""
        return f"[{email}](mailto:{email})"

    def format_phone(self) -> str:
        phone = self.personal_info.get('phone', '')
        return phone or ""

    def format_address(self, address) -> str:
        address = self.personal_info.get('address', '')
        return address or ""

def create_markdown(content, personal_info, emojis=True):
    f = PersonalInfoFormatterMarkdown(personal_info)

    # Format personal info fields with proper formatting
    info_lines = [
        f"- **Name**: {f.format_field('name')}",
        f"- **Position**: {f.format_field('position')}",
        f"- **Address**: {f.format_field('address')}",
        f"- **Phone**: {f.format_field('phone')}",
        f"- **Email**: {f.format_field('email')}",
        f"- **Website**: {f.format_field('website')}",
        f"- **GitHub**: {f.format_field('github')}",
        f"- **Date of Birth**: {f.format_field('date_of_birth')}"
    ]
    return '\n'.join(info_lines) + '\n\n' + content

