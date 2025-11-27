"""
Citation Formatter Utility
Formats research sources into clean Markdown citation blocks.
"""

from typing import List, Dict


class CitationFormatter:

    @staticmethod
    def markdown(sources: List[Dict]) -> str:
        """
        Converts list of source dicts into formatted Markdown.
        
        Expected source format:
        {
            "title": "...",
            "url": "...",
            "content": "...",
            "relevance_score": 0.87
        }
        """

        if not sources:
            return "_No sources available._"

        lines = []
        added = set()  # prevent duplicates

        for src in sources:
            title = src.get("title", "Untitled Source").strip()
            url = src.get("url", "").strip()

            # Skip empty or repeated URLs
            if not url or url in added:
                continue

            added.add(url)

            lines.append(f"- **{title}** — <{url}>")

        return "\n".join(lines)
