"""
🪙 CURRENCY SYSTEM
Multi-tier mathematical currency with earning and spending mechanics
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Union
import json


class CurrencyType(Enum):
    """Different types of mathematical currency"""
    COINS = "coins"  # Basic currency from problem solving
    GEMS = "gems"    # Premium currency from major achievements
    ELEMENTS = "mathematical_elements"  # Rare materials from exploration
    TOKENS = "skill_tokens"  # Specialized currency for skill upgrades
    PRESTIGE = "prestige_points"  # Ultra-rare currency from prestige resets


@dataclass
class Transaction:
    """Record of a currency transaction"""
    transaction_id: str
    student_id: str
    currency_type: CurrencyType
    amount: int
    transaction_type: str  # "earn", "spend", "trade", "gift"
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)


@dataclass
class CurrencyBalance:
    """Student's currency holdings"""
    student_id: str
    coins: int = 0
    gems: int = 0
    elements: int = 0
    tokens: int = 0
    prestige: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def get_balance(self, currency_type: CurrencyType) -> int:
        """Get balance for specific currency type"""
        if currency_type == CurrencyType.COINS:
            return self.coins
        elif currency_type == CurrencyType.GEMS:
            return self.gems
        elif currency_type == CurrencyType.ELEMENTS:
            return self.elements
        elif currency_type == CurrencyType.TOKENS:
            return self.tokens
        elif currency_type == CurrencyType.PRESTIGE:
            return self.prestige
        else:
            return 0
    
    def add_currency(self, currency_type: CurrencyType, amount: int):
        """Add currency to balance"""
        current = self.get_balance(currency_type)
        if currency_type == CurrencyType.COINS:
            self.coins = max(0, current + amount)
        elif currency_type == CurrencyType.GEMS:
            self.gems = max(0, current + amount)
        elif currency_type == CurrencyType.ELEMENTS:
            self.elements = max(0, current + amount)
        elif currency_type == CurrencyType.TOKENS:
            self.tokens = max(0, current + amount)
        elif currency_type == CurrencyType.PRESTIGE:
            self.prestige = max(0, current + amount)
        self.last_updated = datetime.now()


class CurrencyManager:
    """
    🪙 CURRENCY MANAGEMENT SYSTEM
    
    Handles all currency operations, earning mechanics, and economic balance
    Features:
    - Multiple currency types with different earning methods
    - Daily/weekly earning bonuses
    - Anti-inflation economic modeling
    - Trading and gifting systems
    - Transaction history and analytics
    """
    
    def __init__(self):
        self.balances: Dict[str, CurrencyBalance] = {}
        self.transactions: List[Transaction] = []
        self.earning_rates = self._initialize_earning_rates()
        self.daily_limits = self._initialize_daily_limits()
        
    def _initialize_earning_rates(self) -> Dict[str, Dict[CurrencyType, int]]:
        """Initialize base earning rates for different activities"""
        return {
            "problem_solved_easy": {CurrencyType.COINS: 10, CurrencyType.ELEMENTS: 1},
            "problem_solved_medium": {CurrencyType.COINS: 25, CurrencyType.ELEMENTS: 3},
            "problem_solved_hard": {CurrencyType.COINS: 50, CurrencyType.GEMS: 1, CurrencyType.ELEMENTS: 5},
            "video_completed": {CurrencyType.COINS: 5, CurrencyType.TOKENS: 1},
            "quiz_perfect": {CurrencyType.COINS: 30, CurrencyType.GEMS: 2},
            "peer_teaching": {CurrencyType.COINS: 20, CurrencyType.TOKENS: 2},
            "daily_login": {CurrencyType.COINS: 15, CurrencyType.ELEMENTS: 1},
            "weekly_streak": {CurrencyType.GEMS: 5, CurrencyType.TOKENS: 3},
            "monthly_milestone": {CurrencyType.GEMS: 25, CurrencyType.PRESTIGE: 1},
            "prestige_reset": {CurrencyType.PRESTIGE: 100}
        }
    
    def _initialize_daily_limits(self) -> Dict[CurrencyType, int]:
        """Initialize daily earning limits to prevent farming"""
        return {
            CurrencyType.COINS: 500,
            CurrencyType.GEMS: 20,
            CurrencyType.ELEMENTS: 50,
            CurrencyType.TOKENS: 30,
            CurrencyType.PRESTIGE: 5
        }
    
    def get_student_balance(self, student_id: str) -> CurrencyBalance:
        """Get student's current currency balance"""
        if student_id not in self.balances:
            self.balances[student_id] = CurrencyBalance(student_id=student_id)
        return self.balances[student_id]
    
    def award_currency(self, student_id: str, activity: str, 
                      multiplier: float = 1.0, bonus_reason: str = "") -> Dict[CurrencyType, int]:
        """
        Award currency for completed activity
        
        Args:
            student_id: Student receiving currency
            activity: Type of activity completed
            multiplier: Bonus multiplier (e.g., weekend bonus = 1.5)
            bonus_reason: Reason for any bonus applied
            
        Returns:
            Dictionary of currency types and amounts awarded
        """
        if activity not in self.earning_rates:
            return {}
        
        balance = self.get_student_balance(student_id)
        daily_earned = self._get_daily_earnings(student_id)
        awarded = {}
        
        for currency_type, base_amount in self.earning_rates[activity].items():
            # Apply multiplier and check daily limits
            amount = int(base_amount * multiplier)
            daily_limit = self.daily_limits[currency_type]
            
            if daily_earned.get(currency_type, 0) + amount <= daily_limit:
                balance.add_currency(currency_type, amount)
                awarded[currency_type] = amount
                
                # Record transaction
                transaction = Transaction(
                    transaction_id=f"{student_id}_{datetime.now().isoformat()}",
                    student_id=student_id,
                    currency_type=currency_type,
                    amount=amount,
                    transaction_type="earn",
                    description=f"Earned from {activity}" + (f" ({bonus_reason})" if bonus_reason else ""),
                    metadata={"activity": activity, "multiplier": multiplier}
                )
                self.transactions.append(transaction)
        
        return awarded
    
    def spend_currency(self, student_id: str, currency_type: CurrencyType, 
                      amount: int, description: str) -> bool:
        """
        Spend currency for purchases
        
        Args:
            student_id: Student spending currency
            currency_type: Type of currency to spend
            amount: Amount to spend
            description: What the currency is being spent on
            
        Returns:
            True if transaction successful, False if insufficient funds
        """
        balance = self.get_student_balance(student_id)
        current_balance = balance.get_balance(currency_type)
        
        if current_balance >= amount:
            balance.add_currency(currency_type, -amount)
            
            # Record transaction
            transaction = Transaction(
                transaction_id=f"{student_id}_{datetime.now().isoformat()}",
                student_id=student_id,
                currency_type=currency_type,
                amount=-amount,
                transaction_type="spend",
                description=description
            )
            self.transactions.append(transaction)
            return True
        
        return False
    
    def transfer_currency(self, from_student: str, to_student: str,
                         currency_type: CurrencyType, amount: int, 
                         reason: str = "Gift") -> bool:
        """
        Transfer currency between students
        
        Args:
            from_student: Student sending currency
            to_student: Student receiving currency
            currency_type: Type of currency to transfer
            amount: Amount to transfer
            reason: Reason for transfer
            
        Returns:
            True if transfer successful, False if insufficient funds
        """
        if self.spend_currency(from_student, currency_type, amount, f"Transfer to {to_student}: {reason}"):
            recipient_balance = self.get_student_balance(to_student)
            recipient_balance.add_currency(currency_type, amount)
            
            # Record recipient transaction
            transaction = Transaction(
                transaction_id=f"{to_student}_{datetime.now().isoformat()}",
                student_id=to_student,
                currency_type=currency_type,
                amount=amount,
                transaction_type="gift",
                description=f"Received from {from_student}: {reason}",
                metadata={"sender": from_student}
            )
            self.transactions.append(transaction)
            return True
        
        return False
    
    def _get_daily_earnings(self, student_id: str) -> Dict[CurrencyType, int]:
        """Get today's earnings for a student"""
        today = datetime.now().date()
        daily_earnings = {}
        
        for transaction in self.transactions:
            if (transaction.student_id == student_id and 
                transaction.transaction_type == "earn" and
                transaction.timestamp.date() == today):
                
                currency = transaction.currency_type
                daily_earnings[currency] = daily_earnings.get(currency, 0) + transaction.amount
        
        return daily_earnings
    
    def get_leaderboard(self, currency_type: CurrencyType, limit: int = 10) -> List[Dict]:
        """
        Get currency leaderboard
        
        Args:
            currency_type: Type of currency to rank by
            limit: Number of top students to return
            
        Returns:
            List of dictionaries with student_id and balance
        """
        rankings = []
        for student_id, balance in self.balances.items():
            amount = balance.get_balance(currency_type)
            rankings.append({"student_id": student_id, "balance": amount})
        
        rankings.sort(key=lambda x: x["balance"], reverse=True)
        return rankings[:limit]
    
    def get_transaction_history(self, student_id: str, days: int = 30) -> List[Transaction]:
        """Get transaction history for a student"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            t for t in self.transactions 
            if t.student_id == student_id and t.timestamp >= cutoff_date
        ]
    
    def apply_economic_event(self, event_type: str, multiplier: float, duration_hours: int):
        """
        Apply server-wide economic events
        
        Args:
            event_type: Type of economic event
            multiplier: Earning rate multiplier
            duration_hours: How long the event lasts
        """
        # This would be implemented with a scheduling system
        # For now, just update earning rates temporarily
        print(f"🎉 Economic Event: {event_type} - {multiplier}x earnings for {duration_hours} hours!")
    
    def export_data(self) -> Dict:
        """Export all currency data for analytics"""
        return {
            "balances": {k: v.__dict__ for k, v in self.balances.items()},
            "transactions": [t.__dict__ for t in self.transactions],
            "earning_rates": {k: {ct.value: amt for ct, amt in v.items()} 
                            for k, v in self.earning_rates.items()},
            "daily_limits": {ct.value: limit for ct, limit in self.daily_limits.items()}
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize currency manager
    currency_manager = CurrencyManager()
    
    # Test earning currency
    print("🧪 Testing Currency System...")
    
    # Student solves problems
    earned = currency_manager.award_currency("alice_123", "problem_solved_hard", multiplier=1.5, bonus_reason="Weekend Bonus")
    print(f"Alice earned: {earned}")
    
    # Check balance
    balance = currency_manager.get_student_balance("alice_123")
    print(f"Alice's balance: Coins={balance.coins}, Gems={balance.gems}, Elements={balance.elements}")
    
    # Test spending
    success = currency_manager.spend_currency("alice_123", CurrencyType.COINS, 30, "Bought vector visualization tool")
    print(f"Purchase successful: {success}")
    
    # Test transfer
    currency_manager.award_currency("bob_456", "problem_solved_easy")
    transfer_success = currency_manager.transfer_currency("alice_123", "bob_456", CurrencyType.COINS, 10, "Helping with homework")
    print(f"Transfer successful: {transfer_success}")
    
    # Check leaderboard
    leaderboard = currency_manager.get_leaderboard(CurrencyType.COINS)
    print(f"Coin Leaderboard: {leaderboard}")
    
    print("✅ Currency System Tests Complete!")
