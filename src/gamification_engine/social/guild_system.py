"""
🏰 GUILD SYSTEM - League of Legends Inspired Collaborative Learning
Transform study groups into competitive guilds with ranking, progression, and team dynamics.
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


class GuildRank(Enum):
    """Guild ranking system based on collective performance"""

    IRON = "Iron"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    MASTER = "Master"
    CHALLENGER = "Challenger"


class StudyPartyType(Enum):
    """Different types of study sessions"""

    HOMEWORK_GRIND = "Homework Grind"  # Focused problem solving
    EXAM_PREP = "Exam Preparation"  # Review and practice tests
    CONCEPT_MASTERY = "Concept Deep Dive"  # Understanding fundamentals
    PEER_TEACHING = "Peer Teaching"  # Students teaching each other
    COMPETITION = "Battle Royale"  # Competitive problem solving


@dataclass
class StudyPartySession:
    """Individual study session data"""

    session_id: str
    party_type: StudyPartyType
    participants: List[str]  # Student IDs
    start_time: datetime
    end_time: Optional[datetime] = None
    problems_solved: int = 0
    concepts_mastered: List[str] = None
    collaboration_score: float = 0.0  # How well team worked together
    learning_efficiency: float = 0.0  # Problems solved per minute

    def __post_init__(self):
        if self.concepts_mastered is None:
            self.concepts_mastered = []


@dataclass
class StudyParty:
    """2-5 student collaborative learning group (like LoL team)"""

    party_id: str
    leader_id: str
    members: List[str]  # Student IDs
    guild_id: Optional[str] = None
    max_size: int = 5
    current_session: Optional[StudyPartySession] = None
    sessions_history: List[StudyPartySession] = None
    total_xp_earned: int = 0
    team_synergy_rating: float = 0.0  # How well they work together
    preferred_study_times: List[str] = None

    def __post_init__(self):
        if self.sessions_history is None:
            self.sessions_history = []
        if self.preferred_study_times is None:
            self.preferred_study_times = []

    def can_add_member(self) -> bool:
        """Check if party has room for more members"""
        return len(self.members) < self.max_size

    def add_member(self, student_id: str) -> bool:
        """Add a student to the party"""
        if self.can_add_member() and student_id not in self.members:
            self.members.append(student_id)
            logger.info(f"Added student {student_id} to study party {self.party_id}")
            return True
        return False

    def remove_member(self, student_id: str) -> bool:
        """Remove a student from the party"""
        if student_id in self.members:
            self.members.remove(student_id)
            if student_id == self.leader_id and self.members:
                # Auto-promote next member to leader
                self.leader_id = self.members[0]
            logger.info(
                f"Removed student {student_id} from study party {self.party_id}"
            )
            return True
        return False


@dataclass
class Guild:
    """Large learning community (like LoL clubs or Discord servers)"""

    guild_id: str
    name: str
    description: str
    leader_id: str
    officers: List[str]  # Students with management permissions
    members: List[str]  # All guild members
    study_parties: List[str]  # Party IDs in this guild
    rank: GuildRank = GuildRank.IRON
    guild_xp: int = 0
    level: int = 1
    max_members: int = 50

    # Guild perks and benefits
    perks_unlocked: List[str] = None
    guild_hall_upgrades: List[str] = None

    # Competition and events
    tournament_wins: int = 0
    challenges_completed: int = 0

    # Social features
    guild_motto: str = "Learning Together!"
    guild_color: str = "#4A90E2"  # Hex color for guild identity
    creation_date: datetime = None

    def __post_init__(self):
        if self.perks_unlocked is None:
            self.perks_unlocked = []
        if self.guild_hall_upgrades is None:
            self.guild_hall_upgrades = []
        if self.creation_date is None:
            self.creation_date = datetime.now()

    def can_add_member(self) -> bool:
        """Check if guild has room for more members"""
        return len(self.members) < self.max_members

    def add_member(self, student_id: str) -> bool:
        """Add a student to the guild"""
        if self.can_add_member() and student_id not in self.members:
            self.members.append(student_id)
            logger.info(f"Added student {student_id} to guild {self.name}")
            return True
        return False

    def promote_to_officer(self, student_id: str) -> bool:
        """Promote a member to officer status"""
        if student_id in self.members and student_id not in self.officers:
            self.officers.append(student_id)
            logger.info(
                f"Promoted student {student_id} to officer in guild {self.name}"
            )
            return True
        return False

    def calculate_guild_rank(self) -> GuildRank:
        """Calculate guild rank based on collective performance"""
        if self.guild_xp >= 100000:
            return GuildRank.CHALLENGER
        elif self.guild_xp >= 50000:
            return GuildRank.MASTER
        elif self.guild_xp >= 25000:
            return GuildRank.DIAMOND
        elif self.guild_xp >= 12500:
            return GuildRank.PLATINUM
        elif self.guild_xp >= 6250:
            return GuildRank.GOLD
        elif self.guild_xp >= 3125:
            return GuildRank.SILVER
        elif self.guild_xp >= 1000:
            return GuildRank.BRONZE
        else:
            return GuildRank.IRON


class GuildManager:
    """Manages all guild operations and social interactions"""

    def __init__(self):
        self.guilds: Dict[str, Guild] = {}
        self.study_parties: Dict[str, StudyParty] = {}
        self.student_to_guild: Dict[str, str] = {}  # Student ID -> Guild ID
        self.student_to_party: Dict[str, str] = {}  # Student ID -> Party ID

        # Load existing data
        self._load_data()

    def create_guild(
        self,
        name: str,
        description: str,
        leader_id: str,
        motto: str = None,
        color: str = None,
    ) -> str:
        """Create a new guild"""
        guild_id = str(uuid.uuid4())

        guild = Guild(
            guild_id=guild_id,
            name=name,
            description=description,
            leader_id=leader_id,
            officers=[leader_id],
            members=[leader_id],
            study_parties=[],
            guild_motto=motto or "Learning Together!",
            guild_color=color or "#4A90E2",
        )

        self.guilds[guild_id] = guild
        self.student_to_guild[leader_id] = guild_id

        logger.info(f"Created new guild: {name} (ID: {guild_id})")
        self._save_data()
        return guild_id

    def join_guild(self, student_id: str, guild_id: str) -> bool:
        """Student joins an existing guild"""
        if guild_id not in self.guilds:
            logger.error(f"Guild {guild_id} not found")
            return False

        guild = self.guilds[guild_id]
        if not guild.can_add_member():
            logger.error(f"Guild {guild.name} is at capacity")
            return False

        # Remove from current guild if in one
        if student_id in self.student_to_guild:
            self.leave_guild(student_id)

        # Add to new guild
        if guild.add_member(student_id):
            self.student_to_guild[student_id] = guild_id
            self._save_data()
            return True

        return False

    def leave_guild(self, student_id: str) -> bool:
        """Student leaves their current guild"""
        if student_id not in self.student_to_guild:
            return False

        guild_id = self.student_to_guild[student_id]
        guild = self.guilds[guild_id]

        # Remove from guild
        if student_id in guild.members:
            guild.members.remove(student_id)
        if student_id in guild.officers:
            guild.officers.remove(student_id)

        # Handle leadership transfer
        if guild.leader_id == student_id and guild.members:
            guild.leader_id = guild.officers[0] if guild.officers else guild.members[0]

        # Clean up mappings
        del self.student_to_guild[student_id]

        logger.info(f"Student {student_id} left guild {guild.name}")
        self._save_data()
        return True

    def create_study_party(
        self, leader_id: str, party_type: StudyPartyType = StudyPartyType.HOMEWORK_GRIND
    ) -> str:
        """Create a new study party"""
        party_id = str(uuid.uuid4())

        # Get guild if leader is in one
        guild_id = self.student_to_guild.get(leader_id)

        party = StudyParty(
            party_id=party_id,
            leader_id=leader_id,
            members=[leader_id],
            guild_id=guild_id,
        )

        self.study_parties[party_id] = party
        self.student_to_party[leader_id] = party_id

        # Add party to guild if applicable
        if guild_id and guild_id in self.guilds:
            self.guilds[guild_id].study_parties.append(party_id)

        logger.info(f"Created study party {party_id} led by {leader_id}")
        self._save_data()
        return party_id

    def join_study_party(self, student_id: str, party_id: str) -> bool:
        """Student joins an existing study party"""
        if party_id not in self.study_parties:
            logger.error(f"Study party {party_id} not found")
            return False

        party = self.study_parties[party_id]

        # Check if party has room
        if not party.can_add_member():
            logger.error(f"Study party {party_id} is at capacity")
            return False

        # Leave current party if in one
        if student_id in self.student_to_party:
            self.leave_study_party(student_id)

        # Add to new party
        if party.add_member(student_id):
            self.student_to_party[student_id] = party_id
            self._save_data()
            return True

        return False

    def leave_study_party(self, student_id: str) -> bool:
        """Student leaves their current study party"""
        if student_id not in self.student_to_party:
            return False

        party_id = self.student_to_party[student_id]
        party = self.study_parties[party_id]

        if party.remove_member(student_id):
            del self.student_to_party[student_id]

            # If party is empty, remove it
            if not party.members:
                if party.guild_id and party.guild_id in self.guilds:
                    guild = self.guilds[party.guild_id]
                    if party_id in guild.study_parties:
                        guild.study_parties.remove(party_id)
                del self.study_parties[party_id]

            self._save_data()
            return True

        return False

    def start_study_session(self, party_id: str, session_type: StudyPartyType) -> str:
        """Start a collaborative study session"""
        if party_id not in self.study_parties:
            logger.error(f"Study party {party_id} not found")
            return None

        party = self.study_parties[party_id]

        # End current session if one exists
        if party.current_session and not party.current_session.end_time:
            self.end_study_session(party_id)

        # Create new session
        session_id = str(uuid.uuid4())
        session = StudyPartySession(
            session_id=session_id,
            party_type=session_type,
            participants=party.members.copy(),
            start_time=datetime.now(),
        )

        party.current_session = session

        logger.info(f"Started {session_type.value} session for party {party_id}")
        self._save_data()
        return session_id

    def end_study_session(self, party_id: str) -> bool:
        """End the current study session and calculate rewards"""
        if party_id not in self.study_parties:
            return False

        party = self.study_parties[party_id]
        if not party.current_session or party.current_session.end_time:
            return False

        # End the session
        session = party.current_session
        session.end_time = datetime.now()

        # Calculate session duration and efficiency
        duration = (
            session.end_time - session.start_time
        ).total_seconds() / 60  # minutes
        if duration > 0:
            session.learning_efficiency = session.problems_solved / duration

        # Calculate XP rewards based on performance
        base_xp = session.problems_solved * 10
        collaboration_bonus = int(base_xp * session.collaboration_score)
        efficiency_bonus = int(base_xp * min(session.learning_efficiency / 2.0, 1.0))

        total_xp = base_xp + collaboration_bonus + efficiency_bonus
        party.total_xp_earned += total_xp

        # Add to guild XP if applicable
        if party.guild_id and party.guild_id in self.guilds:
            guild = self.guilds[party.guild_id]
            guild.guild_xp += total_xp
            guild.rank = guild.calculate_guild_rank()

        # Archive the session
        party.sessions_history.append(session)
        party.current_session = None

        logger.info(f"Ended study session for party {party_id}. XP earned: {total_xp}")
        self._save_data()
        return True

    def get_guild_leaderboard(self, limit: int = 10) -> List[Tuple[str, Guild]]:
        """Get top guilds by XP"""
        sorted_guilds = sorted(
            self.guilds.items(), key=lambda x: x[1].guild_xp, reverse=True
        )
        return sorted_guilds[:limit]

    def get_student_guild_info(self, student_id: str) -> Optional[Dict]:
        """Get comprehensive guild information for a student"""
        if student_id not in self.student_to_guild:
            return None

        guild_id = self.student_to_guild[student_id]
        guild = self.guilds[guild_id]

        # Get party info if in one
        party_info = None
        if student_id in self.student_to_party:
            party_id = self.student_to_party[student_id]
            party = self.study_parties[party_id]
            party_info = {
                "party_id": party_id,
                "leader": party.leader_id,
                "members": party.members,
                "total_xp": party.total_xp_earned,
                "current_session": party.current_session is not None,
            }

        return {
            "guild": asdict(guild),
            "party": party_info,
            "is_officer": student_id in guild.officers,
            "is_leader": student_id == guild.leader_id,
        }

    def _load_data(self):
        """Load guild data from storage"""
        try:
            # In a real implementation, this would load from a database
            # For now, we'll start with empty data
            pass
        except Exception as e:
            logger.error(f"Error loading guild data: {e}")

    def _save_data(self):
        """Save guild data to storage"""
        try:
            # In a real implementation, this would save to a database
            # For now, we'll just log the save operation
            logger.debug("Guild data saved successfully")
        except Exception as e:
            logger.error(f"Error saving guild data: {e}")


# Example usage and testing
if __name__ == "__main__":
    print("🏰 Testing Guild System...")

    # Create guild manager
    guild_manager = GuildManager()

    # Create a guild
    guild_id = guild_manager.create_guild(
        name="Linear Algebra Legends",
        description="Elite students mastering matrices and vectors",
        leader_id="student_alice",
        motto="Vectors Unite!",
        color="#FF6B6B",
    )

    # Add members to guild
    guild_manager.join_guild("student_bob", guild_id)
    guild_manager.join_guild("student_charlie", guild_id)

    # Create study party
    party_id = guild_manager.create_study_party(
        "student_alice", StudyPartyType.EXAM_PREP
    )
    guild_manager.join_study_party("student_bob", party_id)

    # Start study session
    session_id = guild_manager.start_study_session(party_id, StudyPartyType.EXAM_PREP)

    # Simulate study activity
    party = guild_manager.study_parties[party_id]
    if party.current_session:
        party.current_session.problems_solved = 15
        party.current_session.collaboration_score = 0.85
        party.current_session.concepts_mastered = [
            "Matrix Multiplication",
            "Determinants",
        ]

    # End session
    guild_manager.end_study_session(party_id)

    # Get student info
    student_info = guild_manager.get_student_guild_info("student_alice")
    print(f"✅ Alice's Guild Info: {student_info}")

    # Get leaderboard
    leaderboard = guild_manager.get_guild_leaderboard()
    print(
        f"🏆 Guild Leaderboard: {[(name, guild.guild_xp) for name, guild in leaderboard]}"
    )

    print("🎉 Guild System Test Complete!")
