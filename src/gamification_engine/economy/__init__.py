"""
🪙 ECONOMY & TRADING SYSTEM
Mathematical marketplace with currency, items, and trading mechanics
Inspired by: Black Desert Online, Steam Marketplace, EVE Online
"""

from .currency_system import CurrencyManager, CurrencyType
from .trading_system import Marketplace, AuctionHouse, ItemCategory

__all__ = [
    'CurrencyManager',
    'CurrencyType', 
    'Marketplace',
    'AuctionHouse',
    'ItemCategory'
]

__version__ = "1.0.0"
__author__ = "AI-Driven Development Agent"
__description__ = "Mathematical economy system with trading and investment mechanics"
