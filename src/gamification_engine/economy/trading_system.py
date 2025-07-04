"""
🏪 MARKETPLACE & TRADING SYSTEM
Student-to-student trading with auction house mechanics
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Union
import uuid

from .currency_system import CurrencyType, CurrencyManager


class ItemCategory(Enum):
    """Categories of tradeable items"""
    TOOLS = "mathematical_tools"
    DECORATIONS = "study_space_decorations"
    PET_ACCESSORIES = "pet_accessories"
    CONSUMABLES = "learning_boosters"
    COLLECTIBLES = "rare_collectibles"
    COSMETICS = "avatar_cosmetics"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"


@dataclass
class MarketplaceItem:
    """An item that can be traded in the marketplace"""
    item_id: str
    name: str
    description: str
    category: ItemCategory
    rarity: ItemRarity
    base_value: Dict[CurrencyType, int]
    owner_id: str
    created_date: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def get_market_value(self) -> Dict[CurrencyType, int]:
        """Calculate current market value based on rarity and demand"""
        rarity_multipliers = {
            ItemRarity.COMMON: 1.0,
            ItemRarity.UNCOMMON: 1.5,
            ItemRarity.RARE: 2.5,
            ItemRarity.EPIC: 4.0,
            ItemRarity.LEGENDARY: 7.0,
            ItemRarity.MYTHICAL: 12.0
        }
        
        multiplier = rarity_multipliers[self.rarity]
        return {currency: int(value * multiplier) for currency, value in self.base_value.items()}


@dataclass
class TradeOffer:
    """A trade offer between students"""
    offer_id: str
    from_student: str
    to_student: str
    offered_items: List[str]  # Item IDs
    offered_currency: Dict[CurrencyType, int]
    requested_items: List[str]  # Item IDs
    requested_currency: Dict[CurrencyType, int]
    message: str
    status: str  # "pending", "accepted", "rejected", "expired"
    created_date: datetime = field(default_factory=datetime.now)
    expires_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=7))


@dataclass
class AuctionListing:
    """An auction house listing"""
    listing_id: str
    seller_id: str
    item_id: str
    starting_bid: Dict[CurrencyType, int]
    current_bid: Dict[CurrencyType, int]
    current_bidder: Optional[str] = None
    buyout_price: Optional[Dict[CurrencyType, int]] = None
    auction_end: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=3))
    status: str = "active"  # "active", "sold", "expired"
    bid_history: List[Dict] = field(default_factory=list)


class Marketplace:
    """
    🏪 MARKETPLACE SYSTEM
    
    Central hub for all trading activities
    Features:
    - Direct student-to-student trading
    - Auction house with bidding
    - Price history and market analytics
    - Fraud protection and reputation system
    - Automated market maker for common items
    """
    
    def __init__(self, currency_manager: CurrencyManager):
        self.currency_manager = currency_manager
        self.items: Dict[str, MarketplaceItem] = {}
        self.student_inventories: Dict[str, List[str]] = {}
        self.trade_offers: Dict[str, TradeOffer] = {}
        self.auction_listings: Dict[str, AuctionListing] = {}
        self.market_history: List[Dict] = []
        self.reputation_scores: Dict[str, int] = {}
        
        # Initialize with some basic items
        self._create_starter_items()
    
    def _create_starter_items(self):
        """Create some basic items for the marketplace"""
        starter_items = [
            {
                "name": "Basic Calculator",
                "description": "A simple mathematical calculator for basic operations",
                "category": ItemCategory.TOOLS,
                "rarity": ItemRarity.COMMON,
                "base_value": {CurrencyType.COINS: 50}
            },
            {
                "name": "Vector Visualizer",
                "description": "Interactive 3D vector visualization tool",
                "category": ItemCategory.TOOLS,
                "rarity": ItemRarity.UNCOMMON,
                "base_value": {CurrencyType.COINS: 150, CurrencyType.GEMS: 2}
            },
            {
                "name": "Golden Desk Lamp",
                "description": "Elegant desk lamp for your study space",
                "category": ItemCategory.DECORATIONS,
                "rarity": ItemRarity.RARE,
                "base_value": {CurrencyType.COINS: 300, CurrencyType.GEMS: 5}
            },
            {
                "name": "Pet Food Deluxe",
                "description": "Premium food that makes mathematical pets extra happy",
                "category": ItemCategory.PET_ACCESSORIES,
                "rarity": ItemRarity.UNCOMMON,
                "base_value": {CurrencyType.COINS: 75, CurrencyType.ELEMENTS: 3}
            },
            {
                "name": "Focus Booster",
                "description": "Consumable that increases XP gain for 1 hour",
                "category": ItemCategory.CONSUMABLES,
                "rarity": ItemRarity.COMMON,
                "base_value": {CurrencyType.COINS: 100, CurrencyType.TOKENS: 2}
            }
        ]
        
        for item_data in starter_items:
            item_id = str(uuid.uuid4())
            item = MarketplaceItem(
                item_id=item_id,
                owner_id="marketplace",  # System-owned items
                **item_data
            )
            self.items[item_id] = item
    
    def give_starter_items(self, student_id: str):
        """Give new students some basic items to start trading"""
        if student_id not in self.student_inventories:
            self.student_inventories[student_id] = []
            self.reputation_scores[student_id] = 100  # Start with neutral reputation
            
            # Give basic calculator
            basic_calc = self._create_item_copy(list(self.items.keys())[0], student_id)
            self.student_inventories[student_id].append(basic_calc.item_id)
    
    def _create_item_copy(self, template_item_id: str, new_owner: str) -> MarketplaceItem:
        """Create a copy of an item for a new owner"""
        template = self.items[template_item_id]
        new_item_id = str(uuid.uuid4())
        new_item = MarketplaceItem(
            item_id=new_item_id,
            name=template.name,
            description=template.description,
            category=template.category,
            rarity=template.rarity,
            base_value=template.base_value.copy(),
            owner_id=new_owner,
            metadata=template.metadata.copy()
        )
        self.items[new_item_id] = new_item
        return new_item
    
    def create_trade_offer(self, from_student: str, to_student: str,
                          offered_items: List[str] = None,
                          offered_currency: Dict[CurrencyType, int] = None,
                          requested_items: List[str] = None,
                          requested_currency: Dict[CurrencyType, int] = None,
                          message: str = "") -> str:
        """
        Create a trade offer between students
        
        Returns:
            Trade offer ID if successful, None if invalid
        """
        # Validate offered items belong to sender
        student_inventory = self.student_inventories.get(from_student, [])
        if offered_items:
            for item_id in offered_items:
                if item_id not in student_inventory:
                    return None
        
        # Validate sender has enough currency
        from_balance = self.currency_manager.get_student_balance(from_student)
        if offered_currency:
            for currency_type, amount in offered_currency.items():
                if from_balance.get_balance(currency_type) < amount:
                    return None
        
        offer_id = str(uuid.uuid4())
        trade_offer = TradeOffer(
            offer_id=offer_id,
            from_student=from_student,
            to_student=to_student,
            offered_items=offered_items or [],
            offered_currency=offered_currency or {},
            requested_items=requested_items or [],
            requested_currency=requested_currency or {},
            message=message,
            status="pending"
        )
        
        self.trade_offers[offer_id] = trade_offer
        return offer_id
    
    def accept_trade_offer(self, offer_id: str, accepting_student: str) -> bool:
        """Accept a trade offer"""
        if offer_id not in self.trade_offers:
            return False
        
        offer = self.trade_offers[offer_id]
        
        # Validate acceptance
        if offer.to_student != accepting_student or offer.status != "pending":
            return False
        
        # Check if offer has expired
        if datetime.now() > offer.expires_date:
            offer.status = "expired"
            return False
        
        # Validate accepting student has requested items/currency
        accepter_inventory = self.student_inventories.get(accepting_student, [])
        if offer.requested_items:
            for item_id in offer.requested_items:
                if item_id not in accepter_inventory:
                    return False
        
        accepter_balance = self.currency_manager.get_student_balance(accepting_student)
        if offer.requested_currency:
            for currency_type, amount in offer.requested_currency.items():
                if accepter_balance.get_balance(currency_type) < amount:
                    return False
        
        # Execute the trade
        self._execute_trade(offer)
        offer.status = "accepted"
        
        # Update reputation scores
        self.reputation_scores[offer.from_student] += 1
        self.reputation_scores[accepting_student] += 1
        
        return True
    
    def _execute_trade(self, offer: TradeOffer):
        """Actually execute the trade between students"""
        from_inventory = self.student_inventories.setdefault(offer.from_student, [])
        to_inventory = self.student_inventories.setdefault(offer.to_student, [])
        
        # Transfer items from sender to receiver
        for item_id in offer.offered_items:
            if item_id in from_inventory:
                from_inventory.remove(item_id)
                to_inventory.append(item_id)
                self.items[item_id].owner_id = offer.to_student
        
        # Transfer items from receiver to sender
        for item_id in offer.requested_items:
            if item_id in to_inventory:
                to_inventory.remove(item_id)
                from_inventory.append(item_id)
                self.items[item_id].owner_id = offer.from_student
        
        # Transfer currency from sender to receiver
        for currency_type, amount in offer.offered_currency.items():
            self.currency_manager.transfer_currency(
                offer.from_student, offer.to_student, currency_type, amount, "Trade"
            )
        
        # Transfer currency from receiver to sender
        for currency_type, amount in offer.requested_currency.items():
            self.currency_manager.transfer_currency(
                offer.to_student, offer.from_student, currency_type, amount, "Trade"
            )
        
        # Record trade in market history
        self.market_history.append({
            "type": "trade",
            "participants": [offer.from_student, offer.to_student],
            "items_traded": offer.offered_items + offer.requested_items,
            "currency_traded": {**offer.offered_currency, **offer.requested_currency},
            "timestamp": datetime.now()
        })


class AuctionHouse:
    """
    🏛️ AUCTION HOUSE SYSTEM
    
    Advanced auction mechanics with bidding wars
    Features:
    - Timed auctions with automatic ending
    - Buyout prices for instant purchase
    - Bid history and analytics
    - Automatic outbid notifications
    - Reserve prices and starting bids
    """
    
    def __init__(self, marketplace: Marketplace):
        self.marketplace = marketplace
        self.active_auctions: Dict[str, AuctionListing] = {}
        self.completed_auctions: List[AuctionListing] = []
    
    def create_auction(self, seller_id: str, item_id: str,
                      starting_bid: Dict[CurrencyType, int],
                      buyout_price: Optional[Dict[CurrencyType, int]] = None,
                      duration_hours: int = 72) -> str:
        """Create a new auction listing"""
        # Validate seller owns the item
        seller_inventory = self.marketplace.student_inventories.get(seller_id, [])
        if item_id not in seller_inventory:
            return None
        
        listing_id = str(uuid.uuid4())
        auction = AuctionListing(
            listing_id=listing_id,
            seller_id=seller_id,
            item_id=item_id,
            starting_bid=starting_bid,
            current_bid=starting_bid.copy(),
            buyout_price=buyout_price,
            auction_end=datetime.now() + timedelta(hours=duration_hours)
        )
        
        self.active_auctions[listing_id] = auction
        
        # Remove item from seller's inventory (held in escrow)
        seller_inventory.remove(item_id)
        
        return listing_id
    
    def place_bid(self, listing_id: str, bidder_id: str, 
                 bid_amount: Dict[CurrencyType, int]) -> bool:
        """Place a bid on an auction"""
        if listing_id not in self.active_auctions:
            return False
        
        auction = self.active_auctions[listing_id]
        
        # Check if auction is still active
        if datetime.now() > auction.auction_end or auction.status != "active":
            return False
        
        # Validate bid is higher than current bid
        for currency_type, amount in bid_amount.items():
            current_amount = auction.current_bid.get(currency_type, 0)
            if amount <= current_amount:
                return False
        
        # Validate bidder has sufficient funds
        bidder_balance = self.marketplace.currency_manager.get_student_balance(bidder_id)
        for currency_type, amount in bid_amount.items():
            if bidder_balance.get_balance(currency_type) < amount:
                return False
        
        # Return previous bidder's currency
        if auction.current_bidder:
            for currency_type, amount in auction.current_bid.items():
                prev_balance = self.marketplace.currency_manager.get_student_balance(auction.current_bidder)
                prev_balance.add_currency(currency_type, amount)
        
        # Hold new bidder's currency in escrow
        for currency_type, amount in bid_amount.items():
            self.marketplace.currency_manager.spend_currency(
                bidder_id, currency_type, amount, f"Bid on auction {listing_id}"
            )
        
        # Update auction
        auction.current_bid = bid_amount.copy()
        auction.current_bidder = bidder_id
        auction.bid_history.append({
            "bidder": bidder_id,
            "amount": bid_amount,
            "timestamp": datetime.now()
        })
        
        return True
    
    def buyout_auction(self, listing_id: str, buyer_id: str) -> bool:
        """Buy out an auction at the buyout price"""
        if listing_id not in self.active_auctions:
            return False
        
        auction = self.active_auctions[listing_id]
        
        if not auction.buyout_price or auction.status != "active":
            return False
        
        # Validate buyer has sufficient funds
        buyer_balance = self.marketplace.currency_manager.get_student_balance(buyer_id)
        for currency_type, amount in auction.buyout_price.items():
            if buyer_balance.get_balance(currency_type) < amount:
                return False
        
        # Execute buyout
        self._complete_auction(listing_id, buyer_id, auction.buyout_price)
        return True
    
    def _complete_auction(self, listing_id: str, winner_id: str, final_price: Dict[CurrencyType, int]):
        """Complete an auction with a winner"""
        auction = self.active_auctions[listing_id]
        
        # Transfer payment to seller
        for currency_type, amount in final_price.items():
            if winner_id != auction.current_bidder:
                # If buyout, charge the buyer
                self.marketplace.currency_manager.spend_currency(
                    winner_id, currency_type, amount, f"Buyout auction {listing_id}"
                )
            # Pay the seller
            seller_balance = self.marketplace.currency_manager.get_student_balance(auction.seller_id)
            seller_balance.add_currency(currency_type, amount)
        
        # Transfer item to winner
        winner_inventory = self.marketplace.student_inventories.setdefault(winner_id, [])
        winner_inventory.append(auction.item_id)
        self.marketplace.items[auction.item_id].owner_id = winner_id
        
        # Update auction status
        auction.status = "sold"
        self.completed_auctions.append(auction)
        del self.active_auctions[listing_id]
        
        # Record in market history
        self.marketplace.market_history.append({
            "type": "auction_sale",
            "seller": auction.seller_id,
            "buyer": winner_id,
            "item": auction.item_id,
            "final_price": final_price,
            "timestamp": datetime.now()
        })
    
    def check_expired_auctions(self):
        """Check for and resolve expired auctions"""
        now = datetime.now()
        expired_auctions = []
        
        for listing_id, auction in self.active_auctions.items():
            if now > auction.auction_end and auction.status == "active":
                expired_auctions.append(listing_id)
        
        for listing_id in expired_auctions:
            auction = self.active_auctions[listing_id]
            
            if auction.current_bidder:
                # Complete auction with highest bidder
                self._complete_auction(listing_id, auction.current_bidder, auction.current_bid)
            else:
                # No bids, return item to seller
                seller_inventory = self.marketplace.student_inventories.setdefault(auction.seller_id, [])
                seller_inventory.append(auction.item_id)
                auction.status = "expired"
                self.completed_auctions.append(auction)
                del self.active_auctions[listing_id]


# Example usage and testing
if __name__ == "__main__":
    from .currency_system import CurrencyManager
    
    print("🧪 Testing Marketplace & Trading System...")
    
    # Initialize systems
    currency_manager = CurrencyManager()
    marketplace = Marketplace(currency_manager)
    auction_house = AuctionHouse(marketplace)
    
    # Give students some starting resources
    marketplace.give_starter_items("alice_123")
    marketplace.give_starter_items("bob_456")
    
    # Give them some currency
    currency_manager.award_currency("alice_123", "problem_solved_hard")
    currency_manager.award_currency("bob_456", "problem_solved_medium")
    
    print("Starting inventories:")
    print(f"Alice: {len(marketplace.student_inventories['alice_123'])} items")
    print(f"Bob: {len(marketplace.student_inventories['bob_456'])} items")
    
    # Test direct trading
    alice_items = marketplace.student_inventories["alice_123"]
    if alice_items:
        offer_id = marketplace.create_trade_offer(
            "alice_123", "bob_456",
            offered_items=[alice_items[0]],
            requested_currency={CurrencyType.COINS: 20},
            message="Trading my calculator for coins!"
        )
        
        if offer_id:
            success = marketplace.accept_trade_offer(offer_id, "bob_456")
            print(f"Trade completed: {success}")
    
    # Test auction system
    bob_items = marketplace.student_inventories["bob_456"]
    if bob_items:
        auction_id = auction_house.create_auction(
            "bob_456", bob_items[0],
            starting_bid={CurrencyType.COINS: 30},
            buyout_price={CurrencyType.COINS: 100},
            duration_hours=1
        )
        
        if auction_id:
            print(f"Auction created: {auction_id}")
            
            # Alice bids on the auction
            bid_success = auction_house.place_bid(
                auction_id, "alice_123", {CurrencyType.COINS: 50}
            )
            print(f"Bid placed: {bid_success}")
    
    print("✅ Marketplace & Trading Tests Complete!")
