#!/usr/bin/env python3
"""
🎥 Content Curation Engine
Part of Eagle Adventures 2 - Educational MMORPG Platform

Automates intelligent content curation and integration:
- 3Blue1Brown animation integration
- Khan Academy exercise synchronization
- MIT OpenCourseWare content mapping
- YouTube educational video curation
- AI-powered content personalization
- Adaptive learning pathway generation

Created by: AI Agent Collaboration Team
Date: January 4, 2025
Version: 1.0.0
"""

import asyncio
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

import yaml
import requests
from bs4 import BeautifulSoup
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of educational content"""

    VIDEO = "video"
    INTERACTIVE = "interactive"
    EXERCISE = "exercise"
    SIMULATION = "simulation"
    READING = "reading"
    QUIZ = "quiz"
    PROJECT = "project"
    GAME = "game"


class ContentSource(Enum):
    """Educational content sources"""

    THREE_BLUE_ONE_BROWN = "3blue1brown"
    KHAN_ACADEMY = "khan_academy"
    MIT_OCW = "mit_ocw"
    YOUTUBE_EDU = "youtube_edu"
    COURSERA = "coursera"
    EDX = "edx"
    CUSTOM = "custom"


class DifficultyLevel(Enum):
    """Content difficulty levels"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LearningObjective(Enum):
    """Learning objectives taxonomy"""

    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


@dataclass
class ContentItem:
    """Individual piece of educational content"""

    content_id: str
    title: str
    description: str
    content_type: ContentType
    source: ContentSource
    url: str
    difficulty: DifficultyLevel
    duration_minutes: int
    topics: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    quality_score: float = 0.0
    engagement_score: float = 0.0
    effectiveness_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LearningPath:
    """Structured learning pathway"""

    path_id: str
    title: str
    description: str
    subject_area: str
    total_duration: int
    difficulty_progression: List[DifficultyLevel]
    content_sequence: List[str]  # Content IDs in order
    adaptive_branching: Dict[str, List[str]] = field(default_factory=dict)
    prerequisites: List[str] = field(default_factory=list)
    learning_goals: List[str] = field(default_factory=list)
    assessment_points: List[int] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PersonalizationProfile:
    """Student personalization preferences"""

    student_id: str
    learning_style: str
    preferred_content_types: List[ContentType]
    difficulty_preference: DifficultyLevel
    pace_preference: str  # "slow", "normal", "fast"
    attention_span: int  # minutes
    interests: List[str]
    mastered_topics: Set[str] = field(default_factory=set)
    struggling_topics: Set[str] = field(default_factory=set)
    content_ratings: Dict[str, float] = field(default_factory=dict)
    time_spent: Dict[str, int] = field(default_factory=dict)


class ContentCurationEngine:
    """
    Intelligent content curation and personalization system.

    Automatically discovers, evaluates, and sequences educational content
    from multiple sources to create personalized learning experiences.
    """

    def __init__(self, config_path: str = "config/automation_config.yml"):
        self.config_path = config_path
        self.config = self._load_configuration()
        self.content_library: Dict[str, ContentItem] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        self.personalization_profiles: Dict[str, PersonalizationProfile] = {}

        # Initialize content sources
        self.content_sources = self._initialize_content_sources()

        # Initialize AI for content analysis
        self.openai_client = None
        if self.config.get("openai_api_key"):
            openai.api_key = self.config["openai_api_key"]
            self.openai_client = openai

        # Initialize content storage
        self.content_dir = Path("data/content")
        self.content_dir.mkdir(parents=True, exist_ok=True)

        logger.info("🎥 Content Curation Engine initialized")

    def _load_configuration(self) -> Dict[str, Any]:
        """Load content curation configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("content_curation", {})
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return {}

    def _initialize_content_sources(self) -> Dict[str, Dict[str, Any]]:
        """Initialize content source configurations"""
        return {
            ContentSource.THREE_BLUE_ONE_BROWN.value: {
                "base_url": "https://www.3blue1brown.com",
                "youtube_channel": "UCYO_jab_esuFRV4b17AJtAw",
                "topics": [
                    "linear_algebra",
                    "calculus",
                    "neural_networks",
                    "cryptography",
                ],
                "api_endpoint": None,  # No official API
                "scraping_allowed": True,
            },
            ContentSource.KHAN_ACADEMY.value: {
                "base_url": "https://www.khanacademy.org",
                "api_endpoint": "https://www.khanacademy.org/api/v1",
                "topics": ["math", "science", "computing", "economics"],
                "requires_auth": True,
            },
            ContentSource.MIT_OCW.value: {
                "base_url": "https://ocw.mit.edu",
                "api_endpoint": None,
                "topics": ["mathematics", "computer_science", "physics", "engineering"],
                "open_access": True,
            },
            ContentSource.YOUTUBE_EDU.value: {
                "base_url": "https://www.youtube.com",
                "api_endpoint": "https://www.googleapis.com/youtube/v3",
                "requires_api_key": True,
                "channels": [
                    "UCYO_jab_esuFRV4b17AJtAw",  # 3Blue1Brown
                    "UCotwjyJnb-4KW7bmsOoLfkg",  # Numberphile
                    "UCiJt6d6Ff1zOz6g4ypwJx7A",  # Mathemaniac
                ],
            },
        }

    async def curate_content_for_topic(
        self,
        topic: str,
        difficulty_level: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
        max_items: int = 20,
    ) -> Dict[str, Any]:
        """Curate content for a specific topic"""
        try:
            logger.info(f"Curating content for topic: {topic}")

            curated_content = []

            # Search each content source
            for source in ContentSource:
                try:
                    source_content = await self._search_content_source(
                        source, topic, difficulty_level
                    )
                    curated_content.extend(source_content)
                except Exception as e:
                    logger.warning(f"Failed to search {source.value}: {e}")
                    continue

            # Evaluate and rank content
            ranked_content = await self._evaluate_and_rank_content(
                curated_content, topic
            )

            # Select top content items
            selected_content = ranked_content[:max_items]

            # Store in content library
            for item in selected_content:
                self.content_library[item.content_id] = item

            # Save content to file
            await self._save_curated_content(topic, selected_content)

            logger.info(f"Curated {len(selected_content)} items for {topic}")

            return {
                "success": True,
                "topic": topic,
                "total_found": len(curated_content),
                "selected": len(selected_content),
                "content_items": [item.__dict__ for item in selected_content],
                "sources_searched": [source.value for source in ContentSource],
            }

        except Exception as e:
            logger.error(f"Content curation error: {e}")
            return {"success": False, "error": str(e)}

    async def _search_content_source(
        self, source: ContentSource, topic: str, difficulty: DifficultyLevel
    ) -> List[ContentItem]:
        """Search specific content source for topic"""

        if source == ContentSource.THREE_BLUE_ONE_BROWN:
            return await self._search_3blue1brown(topic, difficulty)
        elif source == ContentSource.KHAN_ACADEMY:
            return await self._search_khan_academy(topic, difficulty)
        elif source == ContentSource.MIT_OCW:
            return await self._search_mit_ocw(topic, difficulty)
        elif source == ContentSource.YOUTUBE_EDU:
            return await self._search_youtube_edu(topic, difficulty)
        else:
            return []

    async def _search_3blue1brown(
        self, topic: str, difficulty: DifficultyLevel
    ) -> List[ContentItem]:
        """Search 3Blue1Brown content"""
        content_items = []

        # Predefined 3Blue1Brown content mapping
        content_mapping = {
            "linear_algebra": [
                {
                    "title": "Essence of Linear Algebra",
                    "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
                    "description": "Visual introduction to linear algebra concepts",
                    "duration": 180,
                    "topics": ["vectors", "matrices", "eigenvalues", "transformations"],
                }
            ],
            "calculus": [
                {
                    "title": "Essence of Calculus",
                    "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr",
                    "description": "Visual approach to understanding calculus",
                    "duration": 200,
                    "topics": ["derivatives", "integrals", "limits", "optimization"],
                }
            ],
            "neural_networks": [
                {
                    "title": "Neural Networks",
                    "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi",
                    "description": "Visual guide to neural networks and deep learning",
                    "duration": 240,
                    "topics": ["perceptrons", "backpropagation", "gradient_descent"],
                }
            ],
        }

        matching_content = content_mapping.get(topic.lower(), [])

        for content in matching_content:
            content_item = ContentItem(
                content_id=str(uuid.uuid4()),
                title=content["title"],
                description=content["description"],
                content_type=ContentType.VIDEO,
                source=ContentSource.THREE_BLUE_ONE_BROWN,
                url=content["url"],
                difficulty=difficulty,
                duration_minutes=content["duration"],
                topics=content["topics"],
                quality_score=0.95,  # 3Blue1Brown is high quality
                engagement_score=0.90,
                effectiveness_score=0.88,
            )
            content_items.append(content_item)

        return content_items

    async def _search_khan_academy(
        self, topic: str, difficulty: DifficultyLevel
    ) -> List[ContentItem]:
        """Search Khan Academy content"""
        content_items = []

        # Simulate Khan Academy content search
        khan_content = {
            "algebra": [
                {
                    "title": "Introduction to Algebra",
                    "url": "https://www.khanacademy.org/math/algebra",
                    "description": "Basic algebraic concepts and operations",
                    "duration": 45,
                    "content_type": ContentType.INTERACTIVE,
                }
            ],
            "geometry": [
                {
                    "title": "Basic Geometry",
                    "url": "https://www.khanacademy.org/math/geometry",
                    "description": "Fundamental geometric concepts",
                    "duration": 60,
                    "content_type": ContentType.INTERACTIVE,
                }
            ],
        }

        matching_content = khan_content.get(topic.lower(), [])

        for content in matching_content:
            content_item = ContentItem(
                content_id=str(uuid.uuid4()),
                title=content["title"],
                description=content["description"],
                content_type=content["content_type"],
                source=ContentSource.KHAN_ACADEMY,
                url=content["url"],
                difficulty=difficulty,
                duration_minutes=content["duration"],
                quality_score=0.85,
                engagement_score=0.80,
                effectiveness_score=0.82,
            )
            content_items.append(content_item)

        return content_items

    async def _search_mit_ocw(
        self, topic: str, difficulty: DifficultyLevel
    ) -> List[ContentItem]:
        """Search MIT OpenCourseWare content"""
        content_items = []

        # Simulate MIT OCW content
        mit_content = {
            "calculus": [
                {
                    "title": "Single Variable Calculus",
                    "url": "https://ocw.mit.edu/courses/mathematics/18-01-single-variable-calculus-fall-2006/",
                    "description": "Comprehensive single variable calculus course",
                    "duration": 600,
                    "content_type": ContentType.READING,
                }
            ],
            "linear_algebra": [
                {
                    "title": "Linear Algebra",
                    "url": "https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010/",
                    "description": "Complete linear algebra course with Gilbert Strang",
                    "duration": 500,
                    "content_type": ContentType.VIDEO,
                }
            ],
        }

        matching_content = mit_content.get(topic.lower(), [])

        for content in matching_content:
            content_item = ContentItem(
                content_id=str(uuid.uuid4()),
                title=content["title"],
                description=content["description"],
                content_type=content["content_type"],
                source=ContentSource.MIT_OCW,
                url=content["url"],
                difficulty=DifficultyLevel.ADVANCED,  # MIT content is typically advanced
                duration_minutes=content["duration"],
                quality_score=0.92,
                engagement_score=0.75,
                effectiveness_score=0.88,
            )
            content_items.append(content_item)

        return content_items

    async def _search_youtube_edu(
        self, topic: str, difficulty: DifficultyLevel
    ) -> List[ContentItem]:
        """Search educational YouTube content"""
        content_items = []

        # Simulate YouTube educational content search
        youtube_content = {
            "statistics": [
                {
                    "title": "Statistics Fundamentals",
                    "url": "https://www.youtube.com/watch?v=xxpc-HPKN28",
                    "description": "Introduction to statistical concepts",
                    "duration": 25,
                    "channel": "StatQuest",
                }
            ],
            "probability": [
                {
                    "title": "Probability Basics",
                    "url": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
                    "description": "Basic probability theory and applications",
                    "duration": 30,
                    "channel": "Khan Academy",
                }
            ],
        }

        matching_content = youtube_content.get(topic.lower(), [])

        for content in matching_content:
            content_item = ContentItem(
                content_id=str(uuid.uuid4()),
                title=content["title"],
                description=content["description"],
                content_type=ContentType.VIDEO,
                source=ContentSource.YOUTUBE_EDU,
                url=content["url"],
                difficulty=difficulty,
                duration_minutes=content["duration"],
                quality_score=0.75,
                engagement_score=0.85,
                effectiveness_score=0.70,
            )
            content_items.append(content_item)

        return content_items

    async def _evaluate_and_rank_content(
        self, content_items: List[ContentItem], topic: str
    ) -> List[ContentItem]:
        """Evaluate and rank content items by quality and relevance"""

        for item in content_items:
            # Calculate composite score
            relevance_score = await self._calculate_relevance_score(item, topic)
            quality_weight = 0.4
            engagement_weight = 0.3
            effectiveness_weight = 0.2
            relevance_weight = 0.1

            composite_score = (
                item.quality_score * quality_weight
                + item.engagement_score * engagement_weight
                + item.effectiveness_score * effectiveness_weight
                + relevance_score * relevance_weight
            )

            item.metadata["composite_score"] = composite_score
            item.metadata["relevance_score"] = relevance_score

        # Sort by composite score
        return sorted(
            content_items,
            key=lambda x: x.metadata.get("composite_score", 0),
            reverse=True,
        )

    async def _calculate_relevance_score(self, item: ContentItem, topic: str) -> float:
        """Calculate content relevance to topic using AI"""
        try:
            if self.openai_client:
                # Use AI to assess relevance
                prompt = f"""
                Rate the relevance of this content to the topic '{topic}' on a scale of 0.0 to 1.0:
                
                Title: {item.title}
                Description: {item.description}
                Topics: {', '.join(item.topics)}
                
                Respond with only a number between 0.0 and 1.0.
                """

                response = await self.openai_client.Completion.acreate(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=10,
                    temperature=0.1,
                )

                score_text = response.choices[0].text.strip()
                return float(score_text)
            else:
                # Fallback: simple keyword matching
                topic_lower = topic.lower()
                title_lower = item.title.lower()
                desc_lower = item.description.lower()

                if topic_lower in title_lower:
                    return 0.9
                elif topic_lower in desc_lower:
                    return 0.7
                elif any(topic_lower in t.lower() for t in item.topics):
                    return 0.8
                else:
                    return 0.3

        except Exception as e:
            logger.warning(f"Relevance calculation failed: {e}")
            return 0.5

    async def create_personalized_learning_path(
        self,
        student_id: str,
        subject_area: str,
        learning_goals: List[str],
        time_constraint: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create personalized learning path for student"""
        try:
            # Get or create personalization profile
            if student_id not in self.personalization_profiles:
                profile = PersonalizationProfile(
                    student_id=student_id,
                    learning_style="visual",
                    preferred_content_types=[
                        ContentType.VIDEO,
                        ContentType.INTERACTIVE,
                    ],
                    difficulty_preference=DifficultyLevel.INTERMEDIATE,
                    pace_preference="normal",
                    attention_span=25,
                    interests=[],
                )
                self.personalization_profiles[student_id] = profile
            else:
                profile = self.personalization_profiles[student_id]

            # Find relevant content
            relevant_content = await self._find_content_for_goals(
                learning_goals, subject_area
            )

            # Personalize content selection
            personalized_content = await self._personalize_content_selection(
                relevant_content, profile
            )

            # Create adaptive sequence
            content_sequence = await self._create_adaptive_sequence(
                personalized_content, profile, time_constraint
            )

            # Create learning path
            path_id = str(uuid.uuid4())
            learning_path = LearningPath(
                path_id=path_id,
                title=f"Personalized {subject_area} Path for {student_id}",
                description=f"Adaptive learning path tailored to achieve: {', '.join(learning_goals)}",
                subject_area=subject_area,
                total_duration=sum(
                    self.content_library[cid].duration_minutes
                    for cid in content_sequence
                ),
                difficulty_progression=self._calculate_difficulty_progression(
                    content_sequence
                ),
                content_sequence=content_sequence,
                learning_goals=learning_goals,
            )

            self.learning_paths[path_id] = learning_path

            # Save learning path
            await self._save_learning_path(learning_path)

            logger.info(f"Created personalized learning path for {student_id}")

            return {
                "success": True,
                "path_id": path_id,
                "total_duration": learning_path.total_duration,
                "content_count": len(content_sequence),
                "learning_path": learning_path.__dict__,
            }

        except Exception as e:
            logger.error(f"Learning path creation error: {e}")
            return {"success": False, "error": str(e)}

    async def _find_content_for_goals(
        self, goals: List[str], subject: str
    ) -> List[ContentItem]:
        """Find content items that match learning goals"""
        relevant_content = []

        for goal in goals:
            # Search content library for matching items
            for item in self.content_library.values():
                if (
                    subject.lower() in item.title.lower()
                    or subject.lower() in item.description.lower()
                    or any(subject.lower() in topic.lower() for topic in item.topics)
                ):

                    if (
                        goal.lower() in item.description.lower()
                        or goal.lower() in item.title.lower()
                    ):
                        relevant_content.append(item)

        return list(set(relevant_content))  # Remove duplicates

    async def _personalize_content_selection(
        self, content: List[ContentItem], profile: PersonalizationProfile
    ) -> List[ContentItem]:
        """Filter and rank content based on personalization profile"""
        personalized = []

        for item in content:
            # Check content type preference
            if item.content_type in profile.preferred_content_types:
                score_boost = 0.2
            else:
                score_boost = 0.0

            # Check difficulty preference
            if item.difficulty == profile.difficulty_preference:
                score_boost += 0.15

            # Check duration vs attention span
            if item.duration_minutes <= profile.attention_span:
                score_boost += 0.1

            # Check if topic was previously struggled with
            if any(topic in profile.struggling_topics for topic in item.topics):
                score_boost += 0.25  # Prioritize struggling topics

            # Update item score
            original_score = item.metadata.get("composite_score", 0.5)
            item.metadata["personalized_score"] = original_score + score_boost

            personalized.append(item)

        # Sort by personalized score
        return sorted(
            personalized,
            key=lambda x: x.metadata.get("personalized_score", 0),
            reverse=True,
        )

    async def _create_adaptive_sequence(
        self,
        content: List[ContentItem],
        profile: PersonalizationProfile,
        time_limit: Optional[int],
    ) -> List[str]:
        """Create adaptive content sequence"""
        sequence = []
        total_time = 0

        # Sort content by difficulty (easier first, unless profile prefers otherwise)
        difficulty_order = [
            DifficultyLevel.BEGINNER,
            DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.ADVANCED,
            DifficultyLevel.EXPERT,
        ]
        if profile.difficulty_preference == DifficultyLevel.ADVANCED:
            content.sort(key=lambda x: difficulty_order.index(x.difficulty))
        else:
            content.sort(key=lambda x: difficulty_order.index(x.difficulty))

        for item in content:
            if time_limit and total_time + item.duration_minutes > time_limit:
                break

            sequence.append(item.content_id)
            total_time += item.duration_minutes

        return sequence

    def _calculate_difficulty_progression(
        self, content_sequence: List[str]
    ) -> List[DifficultyLevel]:
        """Calculate difficulty progression for learning path"""
        progression = []
        for content_id in content_sequence:
            if content_id in self.content_library:
                progression.append(self.content_library[content_id].difficulty)
        return progression

    async def _save_curated_content(self, topic: str, content_items: List[ContentItem]):
        """Save curated content to file"""
        filename = (
            self.content_dir
            / f"curated_{topic}_{datetime.now().strftime('%Y%m%d')}.json"
        )

        with open(filename, "w") as f:
            json.dump(
                [item.__dict__ for item in content_items], f, indent=2, default=str
            )

    async def _save_learning_path(self, learning_path: LearningPath):
        """Save learning path to file"""
        filename = self.content_dir / f"learning_path_{learning_path.path_id}.json"

        with open(filename, "w") as f:
            json.dump(learning_path.__dict__, f, indent=2, default=str)

    async def get_curation_status(self) -> Dict[str, Any]:
        """Get content curation system status"""
        return {
            "total_content_items": len(self.content_library),
            "learning_paths": len(self.learning_paths),
            "personalization_profiles": len(self.personalization_profiles),
            "sources_configured": len(self.content_sources),
            "system_health": "operational",
        }

    async def update_student_progress(
        self, student_id: str, content_id: str, completion_time: int, rating: float
    ):
        """Update student progress and personalization"""
        if student_id in self.personalization_profiles:
            profile = self.personalization_profiles[student_id]
            profile.time_spent[content_id] = completion_time
            profile.content_ratings[content_id] = rating

            # Update topics based on performance
            if content_id in self.content_library:
                content = self.content_library[content_id]
                if rating >= 4.0:  # Good performance
                    profile.mastered_topics.update(content.topics)
                elif rating <= 2.0:  # Poor performance
                    profile.struggling_topics.update(content.topics)


# CLI Interface for testing
async def main():
    """Main function for testing the content curation engine"""
    engine = ContentCurationEngine()

    # Test content curation
    result = await engine.curate_content_for_topic(
        "linear_algebra", DifficultyLevel.INTERMEDIATE
    )
    print("🎥 Content Curation Result:")
    print(json.dumps(result, indent=2, default=str))

    # Test personalized learning path
    if result["success"]:
        path_result = await engine.create_personalized_learning_path(
            student_id="student_123",
            subject_area="mathematics",
            learning_goals=[
                "understand linear transformations",
                "master matrix operations",
            ],
            time_constraint=120,  # 2 hours
        )
        print("\n📚 Learning Path Result:")
        print(json.dumps(path_result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
