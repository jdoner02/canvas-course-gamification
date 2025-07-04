"""
🎮 SOCIAL GAMIFICATION ENGINE
League of Legends + Discord inspired collaborative learning system

This module handles:
- Study party formation and management
- Guild systems with ranking and progression
- Mentorship chains and peer teaching
- PvP competitions and tournaments
- Social leaderboards and achievements
"""

from .guild_system import GuildManager, Guild, StudyParty
from .mentorship_system import MentorshipChain, PeerTeachingEngine
from .competition_system import PvPBattleEngine, TournamentManager

__all__ = [
    'GuildManager',
    'Guild', 
    'StudyParty',
    'MentorshipChain',
    'PeerTeachingEngine',
    'PvPBattleEngine',
    'TournamentManager'
]
