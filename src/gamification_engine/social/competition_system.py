"""
⚔️ COMPETITION SYSTEM - PvP Battles & Tournaments
League of Legends inspired competitive learning with battles, tournaments, and rankings
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BattleType(Enum):
    """Different types of competitive battles"""
    SPEED_SOLVE = "Speed Solve"              # Fastest to solve problems
    ACCURACY_CHALLENGE = "Accuracy Challenge" # Most correct answers
    ENDURANCE_MARATHON = "Endurance Marathon" # Longest sustained solving
    CONCEPT_DUEL = "Concept Duel"            # Explain concepts better
    TEAM_RUMBLE = "Team Rumble"              # Guild vs Guild battles

class TournamentFormat(Enum):
    """Tournament bracket formats"""
    SINGLE_ELIMINATION = "Single Elimination"
    DOUBLE_ELIMINATION = "Double Elimination"
    ROUND_ROBIN = "Round Robin"
    SWISS_SYSTEM = "Swiss System"
    BATTLE_ROYALE = "Battle Royale"          # Everyone vs everyone

class BattleRank(Enum):
    """Competitive ranking system"""
    BRONZE_III = "Bronze III"
    BRONZE_II = "Bronze II"
    BRONZE_I = "Bronze I"
    SILVER_III = "Silver III"
    SILVER_II = "Silver II"
    SILVER_I = "Silver I"
    GOLD_III = "Gold III"
    GOLD_II = "Gold II"
    GOLD_I = "Gold I"
    PLATINUM_III = "Platinum III"
    PLATINUM_II = "Platinum II"
    PLATINUM_I = "Platinum I"
    DIAMOND_III = "Diamond III"
    DIAMOND_II = "Diamond II"
    DIAMOND_I = "Diamond I"
    MASTER = "Master"
    GRANDMASTER = "Grandmaster"
    CHALLENGER = "Challenger"

@dataclass
class BattleResult:
    """Result of a single battle"""
    battle_id: str
    battle_type: BattleType
    participants: List[str]  # Student IDs
    winner_id: str
    start_time: datetime
    end_time: datetime
    
    # Performance metrics
    participant_scores: Dict[str, int] = None
    problems_attempted: Dict[str, int] = None
    accuracy_rates: Dict[str, float] = None
    time_to_completion: Dict[str, float] = None
    
    # Rewards
    winner_xp: int = 0
    loser_xp: int = 0
    rank_points_change: Dict[str, int] = None
    
    def __post_init__(self):
        if self.participant_scores is None:
            self.participant_scores = {}
        if self.problems_attempted is None:
            self.problems_attempted = {}
        if self.accuracy_rates is None:
            self.accuracy_rates = {}
        if self.time_to_completion is None:
            self.time_to_completion = {}
        if self.rank_points_change is None:
            self.rank_points_change = {}

@dataclass
class Tournament:
    """Competitive tournament with multiple participants"""
    tournament_id: str
    name: str
    description: str
    format: TournamentFormat
    battle_type: BattleType
    
    # Tournament settings
    max_participants: int = 32
    entry_cost: int = 0  # XP cost to enter
    prize_pool: int = 0  # Total XP to distribute
    
    # Participants and brackets
    registered_participants: List[str] = None
    tournament_bracket: Dict = None
    completed_battles: List[str] = None  # Battle IDs
    
    # Timeline
    registration_start: datetime = None
    registration_end: datetime = None
    tournament_start: datetime = None
    tournament_end: Optional[datetime] = None
    
    # Results
    winner_id: Optional[str] = None
    runner_up_id: Optional[str] = None
    final_standings: List[str] = None
    
    def __post_init__(self):
        if self.registered_participants is None:
            self.registered_participants = []
        if self.tournament_bracket is None:
            self.tournament_bracket = {}
        if self.completed_battles is None:
            self.completed_battles = []
        if self.final_standings is None:
            self.final_standings = []

@dataclass
class CompetitorProfile:
    """Competitive profile for a student"""
    student_id: str
    current_rank: BattleRank = BattleRank.BRONZE_III
    rank_points: int = 0
    
    # Win/Loss statistics
    total_battles: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    
    # Performance stats
    average_score: float = 0.0
    best_score: int = 0
    current_win_streak: int = 0
    longest_win_streak: int = 0
    
    # Tournament history
    tournaments_entered: int = 0
    tournament_wins: int = 0
    tournament_top_3: int = 0
    
    # Seasonal stats (reset each semester)
    seasonal_rank_points: int = 0
    seasonal_battles: int = 0
    seasonal_wins: int = 0
    
    def update_win_rate(self):
        """Update win rate based on wins/losses"""
        if self.total_battles > 0:
            self.win_rate = self.wins / self.total_battles

class PvPBattleEngine:
    """Engine for managing PvP battles and competitive events"""
    
    def __init__(self):
        self.competitor_profiles: Dict[str, CompetitorProfile] = {}
        self.battle_results: Dict[str, BattleResult] = {}
        self.tournaments: Dict[str, Tournament] = {}
        self.active_battles: Dict[str, str] = {}  # student_id -> battle_id
        self.battle_queue: List[Dict] = []  # Players looking for matches
        
        # Ranking system
        self.rank_thresholds = {
            BattleRank.BRONZE_III: 0,
            BattleRank.BRONZE_II: 100,
            BattleRank.BRONZE_I: 200,
            BattleRank.SILVER_III: 300,
            BattleRank.SILVER_II: 450,
            BattleRank.SILVER_I: 600,
            BattleRank.GOLD_III: 800,
            BattleRank.GOLD_II: 1000,
            BattleRank.GOLD_I: 1200,
            BattleRank.PLATINUM_III: 1500,
            BattleRank.PLATINUM_II: 1800,
            BattleRank.PLATINUM_I: 2100,
            BattleRank.DIAMOND_III: 2500,
            BattleRank.DIAMOND_II: 3000,
            BattleRank.DIAMOND_I: 3500,
            BattleRank.MASTER: 4000,
            BattleRank.GRANDMASTER: 5000,
            BattleRank.CHALLENGER: 6000
        }
        
        self._load_data()
    
    def register_competitor(self, student_id: str) -> bool:
        """Register a student for competitive play"""
        if student_id in self.competitor_profiles:
            return False
        
        profile = CompetitorProfile(student_id=student_id)
        self.competitor_profiles[student_id] = profile
        
        logger.info(f"Registered competitor: {student_id}")
        self._save_data()
        return True
    
    def queue_for_battle(self, student_id: str, battle_type: BattleType, 
                        preferred_rank_range: int = 200) -> bool:
        """Add student to battle queue"""
        if student_id not in self.competitor_profiles:
            self.register_competitor(student_id)
        
        if student_id in self.active_battles:
            logger.warning(f"Student {student_id} already in an active battle")
            return False
        
        # Check if already in queue
        for entry in self.battle_queue:
            if entry['student_id'] == student_id:
                logger.warning(f"Student {student_id} already in battle queue")
                return False
        
        queue_entry = {
            'student_id': student_id,
            'battle_type': battle_type,
            'queue_time': datetime.now(),
            'preferred_rank_range': preferred_rank_range
        }
        
        self.battle_queue.append(queue_entry)
        
        # Try to find a match immediately
        self._attempt_matchmaking()
        
        logger.info(f"Student {student_id} queued for {battle_type.value}")
        return True
    
    def _attempt_matchmaking(self):
        """Try to match players in the queue"""
        if len(self.battle_queue) < 2:
            return
        
        # Simple matchmaking: find closest rank players
        for i, player1 in enumerate(self.battle_queue):
            for j, player2 in enumerate(self.battle_queue[i+1:], i+1):
                if player1['battle_type'] == player2['battle_type']:
                    # Check rank compatibility
                    profile1 = self.competitor_profiles[player1['student_id']]
                    profile2 = self.competitor_profiles[player2['student_id']]
                    
                    rank_diff = abs(profile1.rank_points - profile2.rank_points)
                    max_diff = max(player1['preferred_rank_range'], player2['preferred_rank_range'])
                    
                    if rank_diff <= max_diff:
                        # Create battle
                        self._create_battle(
                            [player1['student_id'], player2['student_id']],
                            player1['battle_type']
                        )
                        
                        # Remove from queue
                        self.battle_queue.remove(player1)
                        self.battle_queue.remove(player2)
                        return
    
    def _create_battle(self, participants: List[str], battle_type: BattleType) -> str:
        """Create a new PvP battle"""
        battle_id = str(uuid.uuid4())
        
        battle = BattleResult(
            battle_id=battle_id,
            battle_type=battle_type,
            participants=participants,
            winner_id="",  # To be determined
            start_time=datetime.now(),
            end_time=datetime.now()  # Will be updated when battle ends
        )
        
        self.battle_results[battle_id] = battle
        
        # Mark participants as in battle
        for participant in participants:
            self.active_battles[participant] = battle_id
        
        logger.info(f"Created {battle_type.value} battle {battle_id} with {len(participants)} participants")
        return battle_id
    
    def complete_battle(self, battle_id: str, winner_id: str, 
                       participant_scores: Dict[str, int],
                       performance_data: Dict = None) -> bool:
        """Complete a battle and calculate rewards/ranking changes"""
        if battle_id not in self.battle_results:
            return False
        
        battle = self.battle_results[battle_id]
        battle.winner_id = winner_id
        battle.end_time = datetime.now()
        battle.participant_scores = participant_scores
        
        if performance_data:
            battle.problems_attempted = performance_data.get('problems_attempted', {})
            battle.accuracy_rates = performance_data.get('accuracy_rates', {})
            battle.time_to_completion = performance_data.get('time_to_completion', {})
        
        # Calculate XP and rank point changes
        self._calculate_battle_rewards(battle)
        
        # Update competitor profiles
        for participant in battle.participants:
            profile = self.competitor_profiles[participant]
            profile.total_battles += 1
            
            if participant == winner_id:
                profile.wins += 1
                profile.current_win_streak += 1
                profile.longest_win_streak = max(profile.longest_win_streak, profile.current_win_streak)
            else:
                profile.losses += 1
                profile.current_win_streak = 0
            
            # Update rank points
            rank_change = battle.rank_points_change.get(participant, 0)
            profile.rank_points += rank_change
            profile.seasonal_rank_points += rank_change
            
            # Update rank
            new_rank = self._calculate_rank(profile.rank_points)
            if new_rank != profile.current_rank:
                logger.info(f"Competitor {participant} promoted to {new_rank.value}!")
                profile.current_rank = new_rank
            
            # Update stats
            profile.update_win_rate()
            if participant_scores.get(participant, 0) > profile.best_score:
                profile.best_score = participant_scores[participant]
            
            # Update average score
            total_score = profile.average_score * (profile.total_battles - 1) + participant_scores.get(participant, 0)
            profile.average_score = total_score / profile.total_battles
        
        # Free up participants
        for participant in battle.participants:
            if participant in self.active_battles:
                del self.active_battles[participant]
        
        logger.info(f"Battle {battle_id} completed. Winner: {winner_id}")
        self._save_data()
        return True
    
    def _calculate_battle_rewards(self, battle: BattleResult):
        """Calculate XP and rank point rewards for battle participants"""
        winner_id = battle.winner_id
        
        # Base rewards
        base_winner_xp = 100
        base_loser_xp = 50
        base_rank_points = 25
        
        # Calculate performance multipliers
        winner_score = battle.participant_scores.get(winner_id, 0)
        total_score = sum(battle.participant_scores.values())
        performance_ratio = winner_score / total_score if total_score > 0 else 1.0
        
        # XP rewards
        battle.winner_xp = int(base_winner_xp * (1 + performance_ratio))
        battle.loser_xp = base_loser_xp
        
        # Rank point changes (consider rank differences)
        for participant in battle.participants:
            if participant == winner_id:
                # Winner gains rank points
                points_gained = int(base_rank_points * (1 + performance_ratio * 0.5))
                battle.rank_points_change[participant] = points_gained
            else:
                # Loser loses fewer points
                points_lost = int(base_rank_points * 0.6)
                battle.rank_points_change[participant] = -points_lost
    
    def _calculate_rank(self, rank_points: int) -> BattleRank:
        """Calculate rank based on rank points"""
        for rank, threshold in reversed(list(self.rank_thresholds.items())):
            if rank_points >= threshold:
                return rank
        return BattleRank.BRONZE_III
    
    def create_tournament(self, name: str, description: str, format: TournamentFormat,
                         battle_type: BattleType, max_participants: int = 32,
                         entry_cost: int = 0, prize_pool: int = 1000) -> str:
        """Create a new tournament"""
        tournament_id = str(uuid.uuid4())
        
        tournament = Tournament(
            tournament_id=tournament_id,
            name=name,
            description=description,
            format=format,
            battle_type=battle_type,
            max_participants=max_participants,
            entry_cost=entry_cost,
            prize_pool=prize_pool,
            registration_start=datetime.now(),
            registration_end=datetime.now() + timedelta(days=3),
            tournament_start=datetime.now() + timedelta(days=3, hours=1)
        )
        
        self.tournaments[tournament_id] = tournament
        
        logger.info(f"Created tournament: {name} (ID: {tournament_id})")
        self._save_data()
        return tournament_id
    
    def register_for_tournament(self, student_id: str, tournament_id: str) -> bool:
        """Register student for a tournament"""
        if tournament_id not in self.tournaments:
            return False
        
        tournament = self.tournaments[tournament_id]
        
        # Check registration window
        now = datetime.now()
        if now < tournament.registration_start or now > tournament.registration_end:
            logger.warning(f"Tournament {tournament_id} registration is closed")
            return False
        
        # Check capacity
        if len(tournament.registered_participants) >= tournament.max_participants:
            logger.warning(f"Tournament {tournament_id} is full")
            return False
        
        # Check if already registered
        if student_id in tournament.registered_participants:
            return False
        
        # Register student
        tournament.registered_participants.append(student_id)
        
        # Update competitor profile
        if student_id in self.competitor_profiles:
            self.competitor_profiles[student_id].tournaments_entered += 1
        
        logger.info(f"Student {student_id} registered for tournament {tournament.name}")
        self._save_data()
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, CompetitorProfile]]:
        """Get top competitors by rank points"""
        sorted_competitors = sorted(
            self.competitor_profiles.items(),
            key=lambda x: x[1].rank_points,
            reverse=True
        )
        return sorted_competitors[:limit]
    
    def get_competitor_stats(self, student_id: str) -> Optional[Dict]:
        """Get comprehensive competitor statistics"""
        if student_id not in self.competitor_profiles:
            return None
        
        profile = self.competitor_profiles[student_id]
        
        # Get recent battles
        recent_battles = [
            battle for battle in self.battle_results.values()
            if student_id in battle.participants and battle.winner_id
        ]
        recent_battles.sort(key=lambda x: x.end_time, reverse=True)
        
        return {
            'profile': asdict(profile),
            'recent_battles': [asdict(b) for b in recent_battles[:5]],
            'is_in_queue': any(entry['student_id'] == student_id for entry in self.battle_queue),
            'is_in_battle': student_id in self.active_battles
        }
    
    def _load_data(self):
        """Load competition data from storage"""
        try:
            # In a real implementation, this would load from a database
            pass
        except Exception as e:
            logger.error(f"Error loading competition data: {e}")
    
    def _save_data(self):
        """Save competition data to storage"""
        try:
            # In a real implementation, this would save to a database
            logger.debug("Competition data saved successfully")
        except Exception as e:
            logger.error(f"Error saving competition data: {e}")

class TournamentManager:
    """Advanced tournament management with brackets and scheduling"""
    
    def __init__(self, battle_engine: PvPBattleEngine):
        self.battle_engine = battle_engine
    
    def generate_bracket(self, tournament_id: str) -> bool:
        """Generate tournament bracket based on format"""
        if tournament_id not in self.battle_engine.tournaments:
            return False
        
        tournament = self.battle_engine.tournaments[tournament_id]
        participants = tournament.registered_participants.copy()
        
        if tournament.format == TournamentFormat.SINGLE_ELIMINATION:
            bracket = self._generate_single_elimination_bracket(participants)
        elif tournament.format == TournamentFormat.ROUND_ROBIN:
            bracket = self._generate_round_robin_bracket(participants)
        else:
            # Default to single elimination
            bracket = self._generate_single_elimination_bracket(participants)
        
        tournament.tournament_bracket = bracket
        logger.info(f"Generated {tournament.format.value} bracket for tournament {tournament.name}")
        return True
    
    def _generate_single_elimination_bracket(self, participants: List[str]) -> Dict:
        """Generate single elimination tournament bracket"""
        # Shuffle participants for random seeding
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Create bracket structure
        bracket = {
            'rounds': [],
            'current_round': 0
        }
        
        # First round pairs
        first_round = []
        for i in range(0, len(shuffled), 2):
            if i + 1 < len(shuffled):
                first_round.append({
                    'match_id': str(uuid.uuid4()),
                    'player1': shuffled[i],
                    'player2': shuffled[i + 1],
                    'winner': None,
                    'battle_id': None
                })
            else:
                # Bye for odd number of players
                first_round.append({
                    'match_id': str(uuid.uuid4()),
                    'player1': shuffled[i],
                    'player2': None,
                    'winner': shuffled[i],  # Auto-advance
                    'battle_id': None
                })
        
        bracket['rounds'].append(first_round)
        return bracket
    
    def _generate_round_robin_bracket(self, participants: List[str]) -> Dict:
        """Generate round robin tournament bracket"""
        bracket = {
            'rounds': [],
            'current_round': 0,
            'standings': {p: {'wins': 0, 'losses': 0, 'points': 0} for p in participants}
        }
        
        # Generate all possible matchups
        matches = []
        for i, player1 in enumerate(participants):
            for player2 in participants[i+1:]:
                matches.append({
                    'match_id': str(uuid.uuid4()),
                    'player1': player1,
                    'player2': player2,
                    'winner': None,
                    'battle_id': None
                })
        
        # Distribute matches across rounds for scheduling
        matches_per_round = max(1, len(participants) // 2)
        rounds = []
        for i in range(0, len(matches), matches_per_round):
            rounds.append(matches[i:i + matches_per_round])
        
        bracket['rounds'] = rounds
        return bracket

# Example usage and testing
if __name__ == "__main__":
    print("⚔️ Testing Competition System...")
    
    # Create battle engine
    engine = PvPBattleEngine()
    
    # Register competitors
    engine.register_competitor("alice_competitive")
    engine.register_competitor("bob_challenger")
    engine.register_competitor("charlie_fighter")
    
    # Queue for battles
    engine.queue_for_battle("alice_competitive", BattleType.SPEED_SOLVE)
    engine.queue_for_battle("bob_challenger", BattleType.SPEED_SOLVE)
    
    # Check if battle was created
    if engine.active_battles:
        # Simulate battle completion
        active_battle_id = list(engine.active_battles.values())[0]
        engine.complete_battle(
            active_battle_id,
            "alice_competitive",
            {"alice_competitive": 95, "bob_challenger": 78},
            {
                "problems_attempted": {"alice_competitive": 20, "bob_challenger": 18},
                "accuracy_rates": {"alice_competitive": 0.95, "bob_challenger": 0.87},
                "time_to_completion": {"alice_competitive": 180, "bob_challenger": 205}
            }
        )
    
    # Create tournament
    tournament_manager = TournamentManager(engine)
    tournament_id = engine.create_tournament(
        "Linear Algebra Championship",
        "Battle for matrix mastery supremacy!",
        TournamentFormat.SINGLE_ELIMINATION,
        BattleType.ACCURACY_CHALLENGE,
        max_participants=8,
        prize_pool=5000
    )
    
    # Register for tournament
    engine.register_for_tournament("alice_competitive", tournament_id)
    engine.register_for_tournament("bob_challenger", tournament_id)
    engine.register_for_tournament("charlie_fighter", tournament_id)
    
    # Generate bracket
    tournament_manager.generate_bracket(tournament_id)
    
    # Get stats
    alice_stats = engine.get_competitor_stats("alice_competitive")
    print(f"✅ Alice's Competition Stats: Rank = {alice_stats['profile']['current_rank']}, Points = {alice_stats['profile']['rank_points']}")
    
    # Get leaderboard
    leaderboard = engine.get_leaderboard()
    print(f"🏆 Competition Leaderboard: {[(id, profile.rank_points) for id, profile in leaderboard]}")
    
    print("🎉 Competition System Test Complete!")
