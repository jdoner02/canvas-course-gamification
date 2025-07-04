"""
Dr. Lynch MATH 231 - YouTube Content Integration
Automated transcript extraction and skill mapping for video content
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging


# Mock YouTube API (in production, would use google-api-python-client)
class MockYouTubeAPI:
    """Mock YouTube API for demonstration purposes"""

    def __init__(self, api_key: str = "mock_api_key"):
        self.api_key = api_key

    def get_playlist_videos(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get videos from a playlist"""
        # Mock data representing Dr. Lynch's videos
        mock_videos = [
            {
                "id": "video_001",
                "title": "Introduction to Vectors - MATH 231",
                "description": "Basic vector concepts and notation",
                "duration": "PT15M30S",
                "published_at": "2024-08-15T10:00:00Z",
                "view_count": 1250,
                "like_count": 45,
            },
            {
                "id": "video_002",
                "title": "Vector Operations - Addition and Scalar Multiplication",
                "description": "How to add vectors and multiply by scalars",
                "duration": "PT22M45S",
                "published_at": "2024-08-17T10:00:00Z",
                "view_count": 980,
                "like_count": 38,
            },
            {
                "id": "video_003",
                "title": "Dot Product and Cross Product",
                "description": "Understanding vector multiplication operations",
                "duration": "PT28M15S",
                "published_at": "2024-08-20T10:00:00Z",
                "view_count": 1150,
                "like_count": 52,
            },
            {
                "id": "video_004",
                "title": "Systems of Linear Equations - Gaussian Elimination",
                "description": "Solving linear systems step by step",
                "duration": "PT35M20S",
                "published_at": "2024-08-22T10:00:00Z",
                "view_count": 1340,
                "like_count": 67,
            },
            {
                "id": "video_005",
                "title": "Matrix Operations - Addition, Multiplication, Inverse",
                "description": "Comprehensive matrix operations tutorial",
                "duration": "PT42M10S",
                "published_at": "2024-08-25T10:00:00Z",
                "view_count": 1420,
                "like_count": 73,
            },
        ]
        return mock_videos

    def get_video_transcript(self, video_id: str) -> str:
        """Get transcript for a video"""
        mock_transcripts = {
            "video_001": """
            Welcome to MATH 231 Linear Algebra. Today we're going to talk about vectors.
            A vector is a mathematical object that has both magnitude and direction.
            We can represent vectors in two ways: geometrically as arrows, or algebraically as ordered pairs or triples.
            For example, the vector from the origin to the point (3, 4) in R2 can be written as <3, 4> or [3, 4].
            The magnitude of this vector is the square root of 3 squared plus 4 squared, which equals 5.
            This comes from the Pythagorean theorem.
            """,
            "video_002": """
            Now let's look at vector operations. The first operation is vector addition.
            To add two vectors, we add their corresponding components.
            If we have vector u equals <2, 3> and vector v equals <1, 4>, then u plus v equals <3, 7>.
            Geometrically, this is equivalent to placing the vectors head to tail.
            The second operation is scalar multiplication. When we multiply a vector by a scalar, we multiply each component by that scalar.
            For example, 2 times the vector <3, 4> equals <6, 8>.
            Scalar multiplication changes the magnitude but preserves the direction if the scalar is positive.
            """,
            "video_003": """
            Today we'll cover two important vector products: the dot product and cross product.
            The dot product of two vectors u and v is defined as u dot v equals the sum of the products of corresponding components.
            For vectors u equals <u1, u2> and v equals <v1, v2>, the dot product is u1 times v1 plus u2 times v2.
            The dot product gives us information about the angle between vectors.
            The cross product is only defined for vectors in R3. If u equals <u1, u2, u3> and v equals <v1, v2, v3>,
            then u cross v equals <u2v3 - u3v2, u3v1 - u1v3, u1v2 - u2v1>.
            The cross product gives us a vector perpendicular to both input vectors.
            """,
            "video_004": """
            Let's solve systems of linear equations using Gaussian elimination.
            Consider the system: x + 2y = 5, 3x - y = 1.
            We can represent this as an augmented matrix: [1 2 | 5; 3 -1 | 1].
            First, we eliminate the x coefficient in the second row by subtracting 3 times the first row from the second row.
            This gives us [1 2 | 5; 0 -7 | -14].
            Now we can solve for y: -7y = -14, so y = 2.
            Substituting back: x + 2(2) = 5, so x = 1.
            Therefore, the solution is x = 1, y = 2.
            """,
            "video_005": """
            Matrix operations are fundamental to linear algebra. Let's start with matrix addition.
            To add two matrices, they must have the same dimensions, and we add corresponding entries.
            For matrix multiplication, the number of columns in the first matrix must equal the number of rows in the second.
            The (i,j) entry of the product is the dot product of the i-th row of the first matrix with the j-th column of the second.
            Finding the inverse of a matrix is more complex. For a 2x2 matrix A = [a b; c d],
            the inverse is (1/(ad-bc)) * [d -b; -c a], provided ad-bc is not zero.
            The determinant ad-bc tells us if the matrix is invertible.
            """,
        }
        return mock_transcripts.get(video_id, "Transcript not available")


@dataclass
class VideoContent:
    """Represents a single video and its associated content"""

    video_id: str
    title: str
    description: str
    duration: str
    transcript: str
    timestamps: List[Tuple[float, str]] = field(default_factory=list)
    skill_mappings: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    difficulty_level: int = 1
    view_count: int = 0
    engagement_score: float = 0.0


@dataclass
class SkillMapping:
    """Maps video content to specific skills in the curriculum"""

    skill_id: str
    video_id: str
    start_time: float
    end_time: float
    confidence_score: float
    content_type: str  # explanation, example, practice, review


class DrLynchYouTubeManager:
    """
    Manages YouTube content integration for Dr. Lynch's MATH 231 course
    Handles transcript extraction, skill mapping, and content organization
    """

    def __init__(self, api_key: str = None):
        self.youtube_api = MockYouTubeAPI(api_key or "mock_key")
        self.videos: Dict[str, VideoContent] = {}
        self.skill_mappings: List[SkillMapping] = []
        self.content_database: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__)

        # Skill keywords for automatic mapping
        self.skill_keywords = {
            "vector_introduction": [
                "vector",
                "magnitude",
                "direction",
                "arrow",
                "ordered pair",
            ],
            "vector_operations": [
                "vector addition",
                "scalar multiplication",
                "components",
            ],
            "vector_products": [
                "dot product",
                "cross product",
                "perpendicular",
                "angle",
            ],
            "linear_equations": ["system", "gaussian elimination", "augmented matrix"],
            "matrix_basics": ["matrix", "entries", "dimensions", "rows", "columns"],
            "matrix_operations": [
                "matrix addition",
                "matrix multiplication",
                "inverse",
                "determinant",
            ],
            "determinant_computation": ["determinant", "cofactor", "expansion"],
            "eigenvalues": ["eigenvalue", "eigenvector", "characteristic polynomial"],
            "vector_spaces": ["vector space", "subspace", "linear combination", "span"],
            "linear_transformations": [
                "transformation",
                "linear map",
                "kernel",
                "image",
            ],
        }

    async def process_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Process entire playlist and extract all content"""
        self.logger.info(f"Processing playlist: {playlist_id}")

        # Get playlist videos
        videos = self.youtube_api.get_playlist_videos(playlist_id)
        processed_count = 0

        for video_data in videos:
            try:
                video_content = await self._process_single_video(video_data)
                self.videos[video_content.video_id] = video_content
                processed_count += 1

                # Add small delay to respect API limits
                await asyncio.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Error processing video {video_data.get('id')}: {e}")

        # Generate skill mappings
        self._generate_skill_mappings()

        # Build searchable content database
        self._build_content_database()

        return {
            "playlist_id": playlist_id,
            "total_videos": len(videos),
            "processed_videos": processed_count,
            "skill_mappings": len(self.skill_mappings),
            "processing_timestamp": datetime.now().isoformat(),
        }

    async def _process_single_video(self, video_data: Dict[str, Any]) -> VideoContent:
        """Process a single video and extract content"""
        video_id = video_data["id"]

        # Get transcript
        transcript = self.youtube_api.get_video_transcript(video_id)

        # Extract keywords from transcript and title
        keywords = self._extract_keywords(transcript, video_data["title"])

        # Generate timestamps (simplified for demo)
        timestamps = self._generate_timestamps(transcript)

        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(video_data)

        video_content = VideoContent(
            video_id=video_id,
            title=video_data["title"],
            description=video_data["description"],
            duration=video_data["duration"],
            transcript=transcript,
            timestamps=timestamps,
            keywords=keywords,
            view_count=video_data.get("view_count", 0),
            engagement_score=engagement_score,
        )

        self.logger.info(f"Processed video: {video_content.title}")
        return video_content

    def _extract_keywords(self, transcript: str, title: str) -> List[str]:
        """Extract relevant keywords from transcript and title"""
        text = f"{title} {transcript}".lower()
        keywords = []

        # Mathematical terms
        math_terms = [
            "vector",
            "matrix",
            "determinant",
            "eigenvalue",
            "eigenvector",
            "linear",
            "algebra",
            "system",
            "equation",
            "transformation",
            "dot product",
            "cross product",
            "gaussian",
            "elimination",
            "inverse",
            "transpose",
            "dimension",
            "basis",
            "subspace",
        ]

        for term in math_terms:
            if term in text:
                keywords.append(term)

        return keywords

    def _generate_timestamps(self, transcript: str) -> List[Tuple[float, str]]:
        """Generate approximate timestamps for key concepts"""
        # This is a simplified implementation
        # In practice, would use speech recognition timing data
        sentences = transcript.split(".")
        timestamps = []

        current_time = 0.0
        time_per_sentence = 5.0  # Assume 5 seconds per sentence

        for sentence in sentences:
            if sentence.strip():
                timestamps.append((current_time, sentence.strip()))
                current_time += time_per_sentence

        return timestamps

    def _calculate_engagement_score(self, video_data: Dict[str, Any]) -> float:
        """Calculate engagement score based on views, likes, etc."""
        views = video_data.get("view_count", 0)
        likes = video_data.get("like_count", 0)

        if views == 0:
            return 0.0

        # Simple engagement calculation
        like_ratio = likes / views if views > 0 else 0
        engagement = (like_ratio * 100) + (views / 100)  # Normalized score
        return min(engagement, 100.0)  # Cap at 100

    def _generate_skill_mappings(self):
        """Generate mappings between video content and curriculum skills"""
        self.skill_mappings = []

        for video_id, video in self.videos.items():
            transcript_lower = video.transcript.lower()
            title_lower = video.title.lower()

            for skill_id, keywords in self.skill_keywords.items():
                confidence = 0.0
                matches = 0

                for keyword in keywords:
                    if keyword in transcript_lower:
                        confidence += 0.3
                        matches += 1
                    if keyword in title_lower:
                        confidence += 0.5
                        matches += 1

                # Normalize confidence score
                if matches > 0:
                    confidence = min(confidence / len(keywords), 1.0)

                    # Only create mapping if confidence is above threshold
                    if confidence > 0.3:
                        mapping = SkillMapping(
                            skill_id=skill_id,
                            video_id=video_id,
                            start_time=0.0,
                            end_time=self._parse_duration(video.duration),
                            confidence_score=confidence,
                            content_type="explanation",
                        )
                        self.skill_mappings.append(mapping)
                        video.skill_mappings.append(skill_id)

    def _parse_duration(self, duration_str: str) -> float:
        """Parse YouTube duration format (PT15M30S) to seconds"""
        # Simple parser for PT format
        duration_str = duration_str.replace("PT", "")
        minutes = 0
        seconds = 0

        if "M" in duration_str:
            parts = duration_str.split("M")
            minutes = int(parts[0])
            duration_str = parts[1]

        if "S" in duration_str:
            seconds = int(duration_str.replace("S", ""))

        return minutes * 60 + seconds

    def _build_content_database(self):
        """Build searchable content database"""
        self.content_database = {}

        for video_id, video in self.videos.items():
            # Index by keywords
            for keyword in video.keywords:
                if keyword not in self.content_database:
                    self.content_database[keyword] = []
                self.content_database[keyword].append(video_id)

            # Index by skill mappings
            for skill_id in video.skill_mappings:
                if skill_id not in self.content_database:
                    self.content_database[skill_id] = []
                self.content_database[skill_id].append(video_id)

    def search_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for videos related to a query"""
        query_lower = query.lower()
        results = []

        # Direct keyword matches
        matching_videos = set()
        for keyword, video_ids in self.content_database.items():
            if query_lower in keyword.lower():
                matching_videos.update(video_ids)

        # Transcript search
        for video_id, video in self.videos.items():
            if (
                query_lower in video.transcript.lower()
                or query_lower in video.title.lower()
            ):
                matching_videos.add(video_id)

        # Build results with relevance scoring
        for video_id in matching_videos:
            video = self.videos[video_id]
            relevance_score = self._calculate_relevance(video, query_lower)
            results.append(
                {
                    "video_id": video_id,
                    "title": video.title,
                    "description": video.description,
                    "duration": video.duration,
                    "relevance_score": relevance_score,
                    "skill_mappings": video.skill_mappings,
                    "engagement_score": video.engagement_score,
                }
            )

        # Sort by relevance and return top results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def _calculate_relevance(self, video: VideoContent, query: str) -> float:
        """Calculate relevance score for search results"""
        score = 0.0

        # Title match (highest weight)
        if query in video.title.lower():
            score += 10.0

        # Description match
        if query in video.description.lower():
            score += 5.0

        # Transcript matches
        transcript_matches = video.transcript.lower().count(query)
        score += transcript_matches * 2.0

        # Keyword matches
        for keyword in video.keywords:
            if query in keyword.lower():
                score += 3.0

        # Engagement boost
        score += video.engagement_score * 0.1

        return score

    def get_videos_for_skill(self, skill_id: str) -> List[Dict[str, Any]]:
        """Get all videos mapped to a specific skill"""
        relevant_mappings = [m for m in self.skill_mappings if m.skill_id == skill_id]

        videos = []
        for mapping in relevant_mappings:
            video = self.videos.get(mapping.video_id)
            if video:
                videos.append(
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "duration": video.duration,
                        "confidence_score": mapping.confidence_score,
                        "content_type": mapping.content_type,
                        "start_time": mapping.start_time,
                        "end_time": mapping.end_time,
                    }
                )

        # Sort by confidence score
        videos.sort(key=lambda x: x["confidence_score"], reverse=True)
        return videos

    def export_content_database(self, output_file: str):
        """Export processed content to JSON file"""
        export_data = {
            "processing_timestamp": datetime.now().isoformat(),
            "total_videos": len(self.videos),
            "total_skill_mappings": len(self.skill_mappings),
            "videos": {},
            "skill_mappings": [],
            "content_index": self.content_database,
        }

        # Export video data
        for video_id, video in self.videos.items():
            export_data["videos"][video_id] = {
                "title": video.title,
                "description": video.description,
                "duration": video.duration,
                "keywords": video.keywords,
                "skill_mappings": video.skill_mappings,
                "engagement_score": video.engagement_score,
                "view_count": video.view_count,
            }

        # Export skill mappings
        for mapping in self.skill_mappings:
            export_data["skill_mappings"].append(
                {
                    "skill_id": mapping.skill_id,
                    "video_id": mapping.video_id,
                    "confidence_score": mapping.confidence_score,
                    "content_type": mapping.content_type,
                }
            )

        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)


# Example usage and testing
async def main():
    """Test the YouTube content manager"""
    print("🎥 Dr. Lynch MATH 231 - YouTube Content Integration")
    print("=" * 60)

    # Initialize manager
    youtube_manager = DrLynchYouTubeManager()

    # Process Dr. Lynch's playlist
    playlist_result = await youtube_manager.process_playlist("PLxxxxxxxxxxxxx")
    print(f"✅ Processed {playlist_result['processed_videos']} videos")
    print(f"🎯 Generated {playlist_result['skill_mappings']} skill mappings")

    # Test content search
    print("\n🔍 Testing Content Search:")
    search_queries = ["vectors", "matrix", "determinant", "eigenvalue"]

    for query in search_queries:
        results = youtube_manager.search_content(query, limit=3)
        print(f"\n   Query: '{query}'")
        for result in results:
            print(
                f"   📹 {result['title']} (relevance: {result['relevance_score']:.1f})"
            )

    # Test skill-specific video retrieval
    print(f"\n🎯 Videos for 'vector_operations' skill:")
    skill_videos = youtube_manager.get_videos_for_skill("vector_operations")
    for video in skill_videos:
        print(f"   📹 {video['title']} (confidence: {video['confidence_score']:.2f})")

    # Export content database
    youtube_manager.export_content_database("dr_lynch_youtube_content.json")
    print(f"\n💾 Exported content database to: dr_lynch_youtube_content.json")


if __name__ == "__main__":
    asyncio.run(main())
