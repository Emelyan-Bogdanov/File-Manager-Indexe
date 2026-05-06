"""
Search Service for PyQt5 File Indexer
Handles indexer loading, searching, and result ranking.
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result (indexer)."""
    indexer_path: str
    filename: str
    filepath: str
    description: str
    keywords: List[str]
    matched_words: Dict[str, List[str]]
    relevance_score: float
    file_exists: bool


class SearchEngine:
    """Advanced search engine for file indexers."""

    INDEXER_FOLDER = "indexers"
    MAX_RESULTS = 50

    def __init__(self, indexer_folder: str = INDEXER_FOLDER):
        """Initialize SearchEngine."""
        self.indexer_folder = Path(indexer_folder)
        self.indexers: List[Dict[str, Any]] = []
        self._load_all_indexers()

    def _load_all_indexers(self) -> None:
        """Load all indexer JSON files."""
        self.indexers = []
        
        if not self.indexer_folder.exists():
            self.indexer_folder.mkdir(parents=True, exist_ok=True)
            return

        try:
            for json_file in self.indexer_folder.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        indexer_data = json.load(f)
                        indexer_data["_file_path"] = str(json_file)
                        self.indexers.append(indexer_data)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading indexer {json_file}: {e}")
        except Exception as e:
            print(f"Error reading indexers folder: {e}")

    def search(self, query: str) -> List[SearchResult]:
        """Search indexers based on query words."""
        self._load_all_indexers()

        if not query.strip():
            return []

        search_words = self._normalize_text(query)
        if not search_words:
            return []

        results: List[SearchResult] = []
        for indexer in self.indexers:
            result = self._search_indexer(indexer, search_words)
            if result:
                results.append(result)

        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[: self.MAX_RESULTS]

    def _search_indexer(
        self, indexer: Dict[str, Any], search_words: List[str]
    ) -> SearchResult:
        """Search a single indexer."""
        filename = indexer.get("filename", "")
        filepath = indexer.get("filepath", "")
        description = indexer.get("description", "")
        keywords = indexer.get("keywords", [])
        indexer_path = indexer.get("_file_path", "")

        file_exists = os.path.exists(filepath)

        matched_words = {
            "filename": [],
            "keywords": [],
            "description": []
        }

        filename_matches = self._find_word_matches(filename, search_words)
        matched_words["filename"] = filename_matches

        keywords_matches = self._find_word_matches(" ".join(keywords), search_words)
        matched_words["keywords"] = keywords_matches

        description_matches = self._find_word_matches(description, search_words)
        matched_words["description"] = description_matches

        total_matches = len(set(
            filename_matches + keywords_matches + description_matches
        ))

        if total_matches == 0:
            return None

        relevance_score = self._calculate_relevance(
            total_matches,
            len(search_words),
            len(filename_matches) > 0,
            len(keywords_matches) > 0,
            len(description_matches) > 0
        )

        return SearchResult(
            indexer_path=indexer_path,
            filename=filename,
            filepath=filepath,
            description=description,
            keywords=keywords,
            matched_words=matched_words,
            relevance_score=relevance_score,
            file_exists=file_exists
        )

    def _find_word_matches(self, text: str, search_words: List[str]) -> List[str]:
        """Find which search words match in text."""
        text_words = self._normalize_text(text)
        matches = []

        for search_word in search_words:
            for text_word in text_words:
                if search_word == text_word:
                    matches.append(search_word)
                    break

        return matches

    def _normalize_text(self, text: str) -> List[str]:
        """Normalize text: lowercase, remove punctuation, split."""
        normalized = re.sub(r'[^\w\s]', '', text.lower())
        words = [w for w in normalized.split() if w]
        return words

    def _calculate_relevance(
        self,
        total_matches: int,
        total_search_words: int,
        has_filename_match: bool,
        has_keyword_match: bool,
        has_description_match: bool
    ) -> float:
        """Calculate relevance score (0.0 to 1.0)."""
        score = 0.0

        base_score = min(total_matches / max(total_search_words, 1), 1.0)
        score += base_score * 0.5

        if has_filename_match:
            score += 0.3
        if has_keyword_match:
            score += 0.1
        if has_description_match:
            score += 0.1

        return min(score, 1.0)
