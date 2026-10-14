"""
NLP Engine for College & Placement FAQ Chatbot
-----------------------------------------------
This module handles:
1. Loading and parsing FAQ knowledge base from JSON.
2. Text cleaning and normalization.
3. TF-IDF vectorization with n-grams and sublinear term frequency.
4. Cosine similarity calculation between user input and indexed questions/patterns.
5. Confidence scoring, threshold filtering, fallback handling, and related question recommendations.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FAQNLPEngine:
    """
    Intelligent FAQ matching engine utilizing TF-IDF and Cosine Similarity.
    Indexes primary questions, user query variations (patterns), and keywords.
    """

    def __init__(self, json_path: str, default_threshold: float = 0.30):
        """
        Initialize the FAQ NLP Engine.

        :param json_path: Path to the faq_data.json file.
        :param default_threshold: Default cosine similarity threshold (0.0 to 1.0).
        """
        self.json_path = json_path
        self.default_threshold = default_threshold
        self.metadata: Dict[str, Any] = {}
        self.faqs: List[Dict[str, Any]] = []
        
        # Corpus indexing containers
        self.indexed_texts: List[str] = []
        self.index_to_faq: List[Dict[str, Any]] = []
        
        # Scikit-learn TF-IDF Vectorizer and Matrix
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        
        # Load and train
        self.load_data()
        self.build_index()

    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Clean and normalize raw text for reliable vectorization.
        - Converts to lowercase
        - Standardizes common abbreviations (e.g., b.tech -> btech, c++ -> cpp)
        - Removes special symbols while keeping alphanumeric tokens
        """
        if not text or not isinstance(text, str):
            return ""
        
        text = text.lower().strip()
        
        # Domain-specific normalizations
        text = re.sub(r'\bb\.?\s*tech\b', 'btech', text)
        text = re.sub(r'\bm\.?\s*tech\b', 'mtech', text)
        text = re.sub(r'\bt\s*&\s*p\b', 'tnp placement', text)
        text = re.sub(r'\bc\+\+\b', 'cpp', text)
        text = re.sub(r'\bc#\b', 'csharp', text)
        text = re.sub(r'[\/\\_\-]', ' ', text)
        
        # Strip other punctuation and excessive whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def load_data(self) -> None:
        """Load FAQ dataset from the specified JSON file."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"FAQ data file not found at: {self.json_path}")
        
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.metadata = data.get("metadata", {})
            self.faqs = data.get("faqs", [])

        if not self.faqs:
            raise ValueError("The FAQ dataset contains no questions.")

    def build_index(self) -> None:
        """
        Build index with pattern-level granularity.
        Indexing every phrasing variation yields significantly higher cosine similarity
        for varied user phrasing than averaging long paragraphs.
        """
        self.indexed_texts = []
        self.index_to_faq = []

        for faq in self.faqs:
            # 1. Index primary question
            cleaned_q = self.preprocess_text(faq.get("question", ""))
            if cleaned_q:
                self.indexed_texts.append(cleaned_q)
                self.index_to_faq.append(faq)

            # 2. Index all pattern variants
            for pattern in faq.get("patterns", []):
                cleaned_p = self.preprocess_text(pattern)
                if cleaned_p:
                    self.indexed_texts.append(cleaned_p)
                    self.index_to_faq.append(faq)

            # 3. Index tags / keywords combination
            tags = " ".join(faq.get("tags", []))
            cleaned_tags = self.preprocess_text(tags)
            if cleaned_tags:
                self.indexed_texts.append(cleaned_tags)
                self.index_to_faq.append(faq)

        # Configure TF-IDF with unigrams + bigrams and sublinear term frequency
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            sublinear_tf=True,
            norm='l2'
        )

        # Fit and transform the corpus
        self.tfidf_matrix = self.vectorizer.fit_transform(self.indexed_texts)

    def get_categories(self) -> List[str]:
        """Return a sorted list of unique FAQ categories."""
        categories = set(faq.get("category", "General") for faq in self.faqs)
        return sorted(list(categories))

    def get_faqs_by_category(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter FAQs by category or return all."""
        if not category or category == "All Categories":
            return self.faqs
        return [faq for faq in self.faqs if faq.get("category") == category]

    def find_match(self, user_query: str, threshold: Optional[float] = None) -> Dict[str, Any]:
        """
        Find the most relevant FAQ for the given user query.

        :param user_query: Question typed by the student.
        :param threshold: Cosine similarity cutoff (defaults to self.default_threshold).
        :return: Result dictionary containing match status, FAQ details, score, and suggestions.
        """
        if threshold is None:
            threshold = self.default_threshold

        cleaned_query = self.preprocess_text(user_query)

        # Handle empty or whitespace-only input
        if not cleaned_query:
            return {
                "matched": False,
                "confidence": 0.0,
                "confidence_percent": "0.0%",
                "question": None,
                "answer": "Please enter a valid question or keyword so I can assist you.",
                "category": None,
                "suggestions": self.get_sample_questions(3),
                "is_empty": True
            }

        # Vectorize user query
        query_vector = self.vectorizer.transform([cleaned_query])

        # Compute cosine similarity against all indexed entries
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # Aggregate maximum score per unique FAQ id
        faq_scores: Dict[int, float] = {}
        faq_map: Dict[int, Dict[str, Any]] = {}

        for idx, score in enumerate(similarities):
            faq = self.index_to_faq[idx]
            faq_id = faq["id"]
            faq_map[faq_id] = faq
            if faq_id not in faq_scores or score > faq_scores[faq_id]:
                faq_scores[faq_id] = float(score)

        # Sort FAQs by highest similarity score
        sorted_faqs = sorted(faq_scores.items(), key=lambda item: item[1], reverse=True)

        if not sorted_faqs:
            return self._build_fallback(user_query, [])

        top_faq_id, top_score = sorted_faqs[0]
        top_faq = faq_map[top_faq_id]

        # Collect top 3 alternate suggestions
        suggestions = []
        for fid, score in sorted_faqs[1:4]:
            if score > 0.08:  # Minimum relevance for suggestions
                suggestions.append(faq_map[fid]["question"])

        # Check if top score meets the threshold
        if top_score >= threshold:
            return {
                "matched": True,
                "confidence": round(top_score, 4),
                "confidence_percent": f"{round(top_score * 100, 1)}%",
                "faq_id": top_faq["id"],
                "question": top_faq["question"],
                "category": top_faq.get("category", "General"),
                "answer": top_faq["answer"],
                "tags": top_faq.get("tags", []),
                "suggestions": suggestions,
                "is_empty": False
            }
        else:
            return self._build_fallback(user_query, sorted_faqs, faq_map, top_score)

    def _build_fallback(
        self,
        query: str,
        sorted_faqs: List[Tuple[int, float]],
        faq_map: Optional[Dict[int, Dict[str, Any]]] = None,
        top_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Construct a helpful fallback response when similarity is below threshold.
        Includes closest potential matches and campus contact options.
        """
        suggestions = []
        if faq_map and sorted_faqs:
            for fid, score in sorted_faqs[:3]:
                if score > 0.05:
                    suggestions.append(faq_map[fid]["question"])

        # If no close matches, pick popular sample questions
        if not suggestions:
            suggestions = self.get_sample_questions(3)

        fallback_answer = (
            "I'm sorry, but I couldn't find a sufficiently close match for your query in the current FAQ database.\n\n"
            "**Here are a few ways to get assistance:**\n"
            "- Try rephrasing your question with simple keywords (e.g., *'placement eligibility'*, *'hostel fee'*, *'scholarships'*).\n"
            "- For **Admissions queries**, email: `admissions@apex-demo-institute.edu` or call `1800-123-4567`.\n"
            "- For **Placement & Internship queries**, email: `placements@apex-demo-institute.edu`.\n"
            "- For **Exams & Transcripts**, email: `examcell@apex-demo-institute.edu`."
        )

        return {
            "matched": False,
            "confidence": round(top_score, 4),
            "confidence_percent": f"{round(top_score * 100, 1)}%",
            "question": None,
            "category": "Unmatched / Fallback",
            "answer": fallback_answer,
            "suggestions": suggestions,
            "is_empty": False
        }

    def get_sample_questions(self, count: int = 5) -> List[str]:
        """Return a diverse list of sample questions across categories."""
        samples = [
            "What is the minimum CGPA required for campus placement?",
            "What are the annual tuition fees for B.Tech?",
            "What is the mandatory attendance requirement?",
            "Are internships mandatory in engineering?",
            "What is the one student one job placement policy?",
            "Which top recruiting companies visit the campus?",
            "How do I get an NOC for an off-campus internship?",
            "What are the hostel and mess facilities?",
            "What merit scholarships are available?",
            "How should I prepare for coding and technical interviews?"
        ]
        return samples[:count]
