from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union

class EmojisFormatter(ABC):
    section_emojis = {
        'academic': '🎓',
        'education': '🎓',
        'professional': '💼',
        'experience': '💼',
        'employment': '💼',
        'work': '💼',
        'award': '🏆',
        'skill': '🔧',
        'competenc': '🔧',
        'technolog': '💻',
        'language': '🗣️',
        'publication': '📚',
        'research': '🔬',
        'project': '📋',
        'interest': '⚡',
        'hobby': '⚡',
        'phd': '📝',
        'thesis': '📄',
        'certification': '🏅',
        'volunteer': '🤝',
        'achievement': '🏆'
    }

    @staticmethod
    def find_emoji(heading_text: str) -> str:
        heading_lower = heading_text.lower()
        for keyword, emoji in EmojisFormatter.section_emojis.items():
            if keyword in heading_lower:
                return emoji
        return '📄'
