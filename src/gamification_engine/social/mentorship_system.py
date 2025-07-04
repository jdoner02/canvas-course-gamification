"""
🎓 MENTORSHIP SYSTEM - Peer Teaching & Knowledge Transfer
Create mentorship chains where advanced students guide newcomers, earning rewards for teaching
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentorshipLevel(Enum):
    """Different levels of mentorship expertise"""
    NOVICE_GUIDE = "Novice Guide"        # Can help with basic concepts
    SKILLED_TUTOR = "Skilled Tutor"      # Can explain intermediate topics
    EXPERT_MENTOR = "Expert Mentor"      # Can teach advanced concepts
    MASTER_TEACHER = "Master Teacher"    # Can guide other mentors

class TeachingMethod(Enum):
    """Different ways mentors can help students"""
    ONE_ON_ONE = "One-on-One Tutoring"
    SMALL_GROUP = "Small Group Teaching"
    CONCEPT_EXPLANATION = "Concept Explanation"
    PROBLEM_WALKTHROUGH = "Problem Walkthrough"
    STUDY_GUIDE_CREATION = "Study Guide Creation"
    PEER_REVIEW = "Peer Review"

@dataclass
class TeachingSession:
    """Individual teaching/mentoring session"""
    session_id: str
    mentor_id: str
    mentee_ids: List[str]
    topic: str
    method: TeachingMethod
    start_time: datetime
    end_time: Optional[datetime] = None
    concepts_taught: List[str] = None
    problems_solved: int = 0
    
    # Feedback and ratings
    mentee_satisfaction: List[float] = None  # 1-5 ratings from mentees
    learning_effectiveness: float = 0.0      # How much mentees improved
    mentor_confidence: float = 0.0           # Mentor's confidence in teaching
    
    # Rewards earned
    mentor_xp_earned: int = 0
    mentee_xp_earned: int = 0
    
    def __post_init__(self):
        if self.concepts_taught is None:
            self.concepts_taught = []
        if self.mentee_satisfaction is None:
            self.mentee_satisfaction = []

@dataclass
class MentorProfile:
    """Profile for a student who mentors others"""
    student_id: str
    mentorship_level: MentorshipLevel = MentorshipLevel.NOVICE_GUIDE
    
    # Teaching stats
    total_sessions: int = 0
    total_students_helped: int = 0
    total_teaching_hours: float = 0.0
    average_satisfaction_rating: float = 0.0
    
    # Expertise areas
    strong_topics: List[str] = None
    teaching_methods: List[TeachingMethod] = None
    
    # Availability and preferences
    available_times: List[str] = None  # "Monday 2-4 PM", etc.
    max_mentees_per_session: int = 3
    preferred_difficulty_levels: List[str] = None
    
    # Achievements and recognition
    teaching_badges: List[str] = None
    mentorship_points: int = 0
    hall_of_fame_entries: int = 0
    
    def __post_init__(self):
        if self.strong_topics is None:
            self.strong_topics = []
        if self.teaching_methods is None:
            self.teaching_methods = [TeachingMethod.ONE_ON_ONE]
        if self.available_times is None:
            self.available_times = []
        if self.preferred_difficulty_levels is None:
            self.preferred_difficulty_levels = ["Beginner", "Intermediate"]
        if self.teaching_badges is None:
            self.teaching_badges = []

@dataclass
class MentorshipChain:
    """Chain of mentorship relationships (A mentors B, B mentors C, etc.)"""
    chain_id: str
    chain_name: str
    participants: List[str]  # Ordered from most experienced to least
    creation_date: datetime = None
    
    # Chain dynamics
    knowledge_flow_efficiency: float = 0.0  # How well knowledge transfers down
    chain_collaboration_score: float = 0.0
    total_chain_xp: int = 0
    
    # Chain achievements
    concepts_mastered_as_chain: List[str] = None
    chain_teaching_streak: int = 0  # Days with teaching activity
    
    def __post_init__(self):
        if self.creation_date is None:
            self.creation_date = datetime.now()
        if self.concepts_mastered_as_chain is None:
            self.concepts_mastered_as_chain = []

class PeerTeachingEngine:
    """Engine for managing peer teaching and mentorship"""
    
    def __init__(self):
        self.mentor_profiles: Dict[str, MentorProfile] = {}
        self.teaching_sessions: Dict[str, TeachingSession] = {}
        self.mentorship_chains: Dict[str, MentorshipChain] = {}
        self.active_sessions: Dict[str, str] = {}  # student_id -> session_id
        
        # Matching system
        self.help_requests: List[Dict] = []  # Students seeking help
        self.mentor_availability: Dict[str, List[str]] = {}  # mentor_id -> available times
        
        self._load_data()
    
    def register_as_mentor(self, student_id: str, strong_topics: List[str] = None,
                          available_times: List[str] = None) -> bool:
        """Register a student as a mentor"""
        if student_id in self.mentor_profiles:
            logger.info(f"Student {student_id} already registered as mentor")
            return False
        
        profile = MentorProfile(
            student_id=student_id,
            strong_topics=strong_topics or [],
            available_times=available_times or []
        )
        
        self.mentor_profiles[student_id] = profile
        logger.info(f"Registered {student_id} as mentor")
        self._save_data()
        return True
    
    def request_help(self, student_id: str, topic: str, preferred_method: TeachingMethod,
                    urgency: str = "normal") -> str:
        """Student requests help with a topic"""
        request_id = str(uuid.uuid4())
        
        request = {
            'request_id': request_id,
            'student_id': student_id,
            'topic': topic,
            'preferred_method': preferred_method,
            'urgency': urgency,
            'timestamp': datetime.now(),
            'status': 'pending'
        }
        
        self.help_requests.append(request)
        
        # Try to auto-match with available mentors
        matched_mentor = self._find_best_mentor(topic, preferred_method)
        if matched_mentor:
            self._create_teaching_session(matched_mentor, [student_id], topic, preferred_method)
            request['status'] = 'matched'
            request['matched_mentor'] = matched_mentor
        
        logger.info(f"Help request created: {request_id} for topic '{topic}'")
        self._save_data()
        return request_id
    
    def _find_best_mentor(self, topic: str, method: TeachingMethod) -> Optional[str]:
        """Find the best available mentor for a topic"""
        candidates = []
        
        for mentor_id, profile in self.mentor_profiles.items():
            # Check if mentor knows the topic
            if topic in profile.strong_topics:
                # Check if mentor supports the teaching method
                if method in profile.teaching_methods:
                    # Check if mentor is available (simplified)
                    if mentor_id not in self.active_sessions:
                        score = profile.average_satisfaction_rating + (profile.mentorship_points / 1000)
                        candidates.append((mentor_id, score))
        
        # Return best mentor
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        return None
    
    def _create_teaching_session(self, mentor_id: str, mentee_ids: List[str],
                               topic: str, method: TeachingMethod) -> str:
        """Create a new teaching session"""
        session_id = str(uuid.uuid4())
        
        session = TeachingSession(
            session_id=session_id,
            mentor_id=mentor_id,
            mentee_ids=mentee_ids,
            topic=topic,
            method=method,
            start_time=datetime.now()
        )
        
        self.teaching_sessions[session_id] = session
        
        # Mark participants as busy
        self.active_sessions[mentor_id] = session_id
        for mentee_id in mentee_ids:
            self.active_sessions[mentee_id] = session_id
        
        logger.info(f"Created teaching session {session_id} for topic '{topic}'")
        return session_id
    
    def start_teaching_session(self, mentor_id: str, mentee_ids: List[str],
                             topic: str, method: TeachingMethod) -> str:
        """Manually start a teaching session"""
        return self._create_teaching_session(mentor_id, mentee_ids, topic, method)
    
    def end_teaching_session(self, session_id: str, concepts_taught: List[str],
                           problems_solved: int, mentor_confidence: float,
                           mentee_ratings: List[float]) -> bool:
        """End a teaching session and calculate rewards"""
        if session_id not in self.teaching_sessions:
            return False
        
        session = self.teaching_sessions[session_id]
        session.end_time = datetime.now()
        session.concepts_taught = concepts_taught
        session.problems_solved = problems_solved
        session.mentor_confidence = mentor_confidence
        session.mentee_satisfaction = mentee_ratings
        
        # Calculate learning effectiveness
        avg_satisfaction = sum(mentee_ratings) / len(mentee_ratings) if mentee_ratings else 0
        session.learning_effectiveness = (avg_satisfaction + mentor_confidence) / 2
        
        # Calculate XP rewards
        base_xp = len(concepts_taught) * 20 + problems_solved * 10
        effectiveness_multiplier = session.learning_effectiveness / 5.0  # 0-1 scale
        
        session.mentor_xp_earned = int(base_xp * (1 + effectiveness_multiplier))
        session.mentee_xp_earned = int(base_xp * 0.5)  # Mentees get less XP
        
        # Update mentor profile
        mentor_profile = self.mentor_profiles[session.mentor_id]
        mentor_profile.total_sessions += 1
        mentor_profile.total_students_helped += len(session.mentee_ids)
        
        # Calculate session duration
        duration = (session.end_time - session.start_time).total_seconds() / 3600  # hours
        mentor_profile.total_teaching_hours += duration
        
        # Update average satisfaction
        total_ratings = mentor_profile.average_satisfaction_rating * (mentor_profile.total_sessions - 1)
        total_ratings += avg_satisfaction
        mentor_profile.average_satisfaction_rating = total_ratings / mentor_profile.total_sessions
        
        # Add mentorship points
        mentor_profile.mentorship_points += session.mentor_xp_earned
        
        # Check for level up
        self._check_mentorship_level_up(session.mentor_id)
        
        # Free up participants
        for participant in [session.mentor_id] + session.mentee_ids:
            if participant in self.active_sessions:
                del self.active_sessions[participant]
        
        logger.info(f"Ended teaching session {session_id}. Mentor earned {session.mentor_xp_earned} XP")
        self._save_data()
        return True
    
    def _check_mentorship_level_up(self, mentor_id: str):
        """Check if mentor should level up their mentorship level"""
        profile = self.mentor_profiles[mentor_id]
        
        # Level up criteria
        if (profile.mentorship_points >= 10000 and 
            profile.average_satisfaction_rating >= 4.5 and
            profile.total_sessions >= 50):
            profile.mentorship_level = MentorshipLevel.MASTER_TEACHER
        elif (profile.mentorship_points >= 5000 and 
              profile.average_satisfaction_rating >= 4.0 and
              profile.total_sessions >= 25):
            profile.mentorship_level = MentorshipLevel.EXPERT_MENTOR
        elif (profile.mentorship_points >= 2000 and 
              profile.average_satisfaction_rating >= 3.5 and
              profile.total_sessions >= 10):
            profile.mentorship_level = MentorshipLevel.SKILLED_TUTOR
        
        logger.info(f"Mentor {mentor_id} level: {profile.mentorship_level.value}")
    
    def create_mentorship_chain(self, chain_name: str, participants: List[str]) -> str:
        """Create a mentorship chain from most to least experienced"""
        chain_id = str(uuid.uuid4())
        
        # Sort participants by mentorship experience
        sorted_participants = sorted(
            participants,
            key=lambda x: self.mentor_profiles.get(x, MentorProfile(x)).mentorship_points,
            reverse=True
        )
        
        chain = MentorshipChain(
            chain_id=chain_id,
            chain_name=chain_name,
            participants=sorted_participants
        )
        
        self.mentorship_chains[chain_id] = chain
        
        logger.info(f"Created mentorship chain: {chain_name} with {len(participants)} participants")
        self._save_data()
        return chain_id
    
    def get_mentor_leaderboard(self, limit: int = 10) -> List[Tuple[str, MentorProfile]]:
        """Get top mentors by points"""
        sorted_mentors = sorted(
            self.mentor_profiles.items(),
            key=lambda x: x[1].mentorship_points,
            reverse=True
        )
        return sorted_mentors[:limit]
    
    def get_mentor_stats(self, mentor_id: str) -> Optional[Dict]:
        """Get comprehensive mentor statistics"""
        if mentor_id not in self.mentor_profiles:
            return None
        
        profile = self.mentor_profiles[mentor_id]
        
        # Get recent sessions
        recent_sessions = [
            session for session in self.teaching_sessions.values()
            if session.mentor_id == mentor_id and session.end_time
        ]
        recent_sessions.sort(key=lambda x: x.end_time, reverse=True)
        
        return {
            'profile': asdict(profile),
            'recent_sessions': [asdict(s) for s in recent_sessions[:5]],
            'total_xp_earned': sum(s.mentor_xp_earned for s in recent_sessions),
            'is_active': mentor_id in self.active_sessions
        }
    
    def _load_data(self):
        """Load mentorship data from storage"""
        try:
            # In a real implementation, this would load from a database
            pass
        except Exception as e:
            logger.error(f"Error loading mentorship data: {e}")
    
    def _save_data(self):
        """Save mentorship data to storage"""
        try:
            # In a real implementation, this would save to a database
            logger.debug("Mentorship data saved successfully")
        except Exception as e:
            logger.error(f"Error saving mentorship data: {e}")

# Example usage and testing
if __name__ == "__main__":
    print("🎓 Testing Mentorship System...")
    
    # Create peer teaching engine
    engine = PeerTeachingEngine()
    
    # Register mentors
    engine.register_as_mentor(
        "alice_advanced",
        strong_topics=["Matrix Multiplication", "Eigenvalues", "Linear Transformations"],
        available_times=["Monday 2-4 PM", "Wednesday 1-3 PM"]
    )
    
    engine.register_as_mentor(
        "bob_intermediate",
        strong_topics=["Vector Operations", "Matrix Basics"],
        available_times=["Tuesday 3-5 PM", "Thursday 2-4 PM"]
    )
    
    # Student requests help
    request_id = engine.request_help(
        "charlie_beginner",
        "Matrix Multiplication",
        TeachingMethod.ONE_ON_ONE,
        "high"
    )
    
    # Find active session (should be auto-created)
    active_session = None
    for session in engine.teaching_sessions.values():
        if not session.end_time:
            active_session = session
            break
    
    if active_session:
        # End the session with some data
        engine.end_teaching_session(
            active_session.session_id,
            concepts_taught=["Matrix Multiplication", "Row Operations"],
            problems_solved=5,
            mentor_confidence=4.2,
            mentee_ratings=[4.5]
        )
    
    # Create mentorship chain
    chain_id = engine.create_mentorship_chain(
        "Linear Algebra Masters",
        ["alice_advanced", "bob_intermediate", "charlie_beginner"]
    )
    
    # Get mentor stats
    alice_stats = engine.get_mentor_stats("alice_advanced")
    print(f"✅ Alice's Mentor Stats: {alice_stats}")
    
    # Get leaderboard
    leaderboard = engine.get_mentor_leaderboard()
    print(f"🏆 Mentor Leaderboard: {[(id, profile.mentorship_points) for id, profile in leaderboard]}")
    
    print("🎉 Mentorship System Test Complete!")
