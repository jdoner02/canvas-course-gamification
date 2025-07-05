#!/usr/bin/env python3
"""
Eagle Adventures 2 - Mobile Interface System
==========================================

Responsive mobile interface for students to access the gamified learning
platform on smartphones and tablets with native-like experience.

Features:
- Progressive Web App (PWA) capabilities
- Touch-optimized UI components
- Offline functionality for key features
- Push notifications for engagement
- Gesture-based navigation
- Mobile-first responsive design
- Native device integration

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceType(Enum):
    """Mobile device types"""

    SMARTPHONE = "smartphone"
    TABLET = "tablet"
    PHABLET = "phablet"
    DESKTOP = "desktop"


class MobileFeature(Enum):
    """Available mobile features"""

    PUSH_NOTIFICATIONS = "push_notifications"
    OFFLINE_MODE = "offline_mode"
    TOUCH_GESTURES = "touch_gestures"
    CAMERA_INTEGRATION = "camera_integration"
    VOICE_INPUT = "voice_input"
    GPS_LOCATION = "gps_location"
    HAPTIC_FEEDBACK = "haptic_feedback"


class UIComponent(Enum):
    """Mobile UI components"""

    PLAYER_DASHBOARD = "player_dashboard"
    PET_COMPANION = "pet_companion"
    SKILL_TREE = "skill_tree"
    QUEST_LOG = "quest_log"
    GUILD_CHAT = "guild_chat"
    LEADERBOARD = "leaderboard"
    MARKETPLACE = "marketplace"
    SETTINGS = "settings"


@dataclass
class MobileSession:
    """Mobile user session"""

    session_id: str
    user_id: str
    device_type: DeviceType
    device_capabilities: List[MobileFeature]
    active_components: List[UIComponent]
    session_start: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    offline_actions: List[Dict[str, Any]] = field(default_factory=list)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)


@dataclass
class MobileUIConfig:
    """Mobile UI configuration"""

    theme: str = "eagle_adventures_mobile"
    font_size_scale: float = 1.0
    touch_target_size: int = 44  # iOS recommended minimum
    gesture_sensitivity: float = 1.0
    animation_speed: str = "fast"
    offline_cache_size: int = 50  # MB
    notification_badge_limit: int = 99


class MobileInterfaceOrchestrator:
    """
    Orchestrates mobile interface for Eagle Adventures 2 platform.

    Provides responsive, touch-optimized UI with PWA capabilities,
    offline functionality, and native device integration.
    """

    def __init__(self, config_path: str = "config/mobile_interface_config.yml"):
        self.config_path = config_path
        self.config = self._load_config()

        # Track active mobile sessions
        self.active_sessions: Dict[str, MobileSession] = {}

        # UI component registry
        self.ui_components = self._initialize_ui_components()

        # PWA service worker
        self.service_worker = None

        # Notification system
        self.notification_system = None

        self._initialize_mobile_features()

        logger.info(
            "📱 Mobile Interface Orchestrator initialized for Eagle Adventures 2"
        )

    def _load_config(self) -> Dict[str, Any]:
        """Load mobile interface configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("mobile_interface", {})
        except Exception as e:
            logger.warning(f"⚠️ Could not load mobile config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default mobile interface configuration"""
        return {
            "pwa_enabled": True,
            "offline_mode": True,
            "push_notifications": True,
            "themes": {
                "default": "eagle_adventures_mobile",
                "dark_mode": "eagle_adventures_dark",
                "accessibility": "eagle_adventures_accessible",
            },
            "performance": {
                "lazy_loading": True,
                "image_compression": True,
                "cache_strategy": "aggressive",
            },
            "gestures": {
                "swipe_navigation": True,
                "pinch_zoom": True,
                "long_press_menus": True,
            },
        }

    def _initialize_ui_components(self) -> Dict[str, Any]:
        """Initialize mobile UI components"""
        components = {
            "player_dashboard": {
                "template": "mobile/dashboard.html",
                "style": "mobile/dashboard.css",
                "script": "mobile/dashboard.js",
                "features": ["touch_navigation", "swipe_gestures", "pull_to_refresh"],
            },
            "pet_companion": {
                "template": "mobile/pet_companion.html",
                "style": "mobile/pet_companion.css",
                "script": "mobile/pet_companion.js",
                "features": ["touch_interaction", "haptic_feedback", "animation"],
            },
            "skill_tree": {
                "template": "mobile/skill_tree.html",
                "style": "mobile/skill_tree.css",
                "script": "mobile/skill_tree.js",
                "features": ["pinch_zoom", "pan_navigation", "touch_targets"],
            },
            "quest_log": {
                "template": "mobile/quest_log.html",
                "style": "mobile/quest_log.css",
                "script": "mobile/quest_log.js",
                "features": ["infinite_scroll", "swipe_actions", "offline_sync"],
            },
            "guild_chat": {
                "template": "mobile/guild_chat.html",
                "style": "mobile/guild_chat.css",
                "script": "mobile/guild_chat.js",
                "features": ["real_time_messaging", "voice_input", "emoji_picker"],
            },
        }

        logger.info(f"🎨 Initialized {len(components)} mobile UI components")
        return components

    def _initialize_mobile_features(self):
        """Initialize mobile-specific features"""
        try:
            # Initialize PWA service worker
            if self.config.get("pwa_enabled", True):
                self._setup_pwa_service_worker()

            # Initialize push notification system
            if self.config.get("push_notifications", True):
                self._setup_push_notifications()

            # Initialize offline caching
            if self.config.get("offline_mode", True):
                self._setup_offline_caching()

            logger.info("✅ Mobile features initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize mobile features: {e}")

    def _setup_pwa_service_worker(self):
        """Set up Progressive Web App service worker"""
        service_worker_config = {
            "cache_name": "eagle_adventures_v1",
            "cache_files": [
                "/",
                "/static/css/mobile.css",
                "/static/js/mobile.js",
                "/static/images/icons/",
                "/api/player/profile",
                "/api/pet/status",
            ],
            "offline_fallbacks": {
                "html": "/offline.html",
                "image": "/static/images/offline-image.png",
                "api": "/api/offline",
            },
        }

        self.service_worker = service_worker_config
        logger.info("📱 PWA service worker configured")

    def _setup_push_notifications(self):
        """Set up mobile push notification system"""
        notification_config = {
            "vapid_keys": {
                "public_key": "generated_public_key",
                "private_key": "generated_private_key",
            },
            "notification_types": {
                "quest_completed": {
                    "title": "Quest Completed! 🎉",
                    "body": "You've completed {quest_name}! Claim your reward.",
                    "icon": "/static/images/icons/quest_complete.png",
                    "badge": "/static/images/badges/quest.png",
                },
                "pet_needs_attention": {
                    "title": "Your {pet_name} needs attention 🐾",
                    "body": "Feed and care for your companion to keep them happy!",
                    "icon": "/static/images/icons/pet_alert.png",
                    "badge": "/static/images/badges/pet.png",
                },
                "guild_message": {
                    "title": "New Guild Message 💬",
                    "body": "{sender}: {message_preview}",
                    "icon": "/static/images/icons/guild_message.png",
                    "badge": "/static/images/badges/guild.png",
                },
                "level_up": {
                    "title": "Level Up! ⚡",
                    "body": "Congratulations! You've reached level {level}!",
                    "icon": "/static/images/icons/level_up.png",
                    "badge": "/static/images/badges/level.png",
                },
            },
        }

        self.notification_system = notification_config
        logger.info("🔔 Push notification system configured")

    def _setup_offline_caching(self):
        """Set up offline caching strategy"""
        cache_config = {
            "strategies": {
                "network_first": ["api/player/*", "api/live/*"],
                "cache_first": ["static/*", "images/*"],
                "stale_while_revalidate": ["api/content/*", "api/quests/*"],
            },
            "cache_size_limits": {
                "images": 25,  # MB
                "api_responses": 10,  # MB
                "static_assets": 15,  # MB
            },
            "offline_actions": {
                "max_queue_size": 100,
                "sync_interval": 30,  # seconds
                "retry_attempts": 3,
            },
        }

        logger.info("💾 Offline caching strategy configured")

    async def create_mobile_session(
        self, user_id: str, device_info: Dict[str, Any]
    ) -> str:
        """
        Create new mobile session for user

        Args:
            user_id: Student user ID
            device_info: Device capabilities and type info

        Returns:
            Mobile session ID
        """
        session_id = str(uuid.uuid4())

        # Detect device type based on screen size and capabilities
        device_type = self._detect_device_type(device_info)

        # Determine available features based on device capabilities
        device_capabilities = self._detect_device_capabilities(device_info)

        # Create session
        session = MobileSession(
            session_id=session_id,
            user_id=user_id,
            device_type=device_type,
            device_capabilities=device_capabilities,
            active_components=[UIComponent.PLAYER_DASHBOARD],
            notification_preferences=self._get_default_notification_preferences(),
        )

        self.active_sessions[session_id] = session

        logger.info(
            f"📱 Created mobile session for user {user_id} (Session: {session_id})"
        )

        return {
            "success": True,
            "session_id": session_id,
            "device_type": device_type.value,
            "available_features": [f.value for f in device_capabilities],
            "ui_config": self._get_mobile_ui_config(device_type),
        }

    def _detect_device_type(self, device_info: Dict[str, Any]) -> DeviceType:
        """Detect device type from device information"""
        screen_width = device_info.get("screen_width", 0)
        screen_height = device_info.get("screen_height", 0)
        user_agent = device_info.get("user_agent", "").lower()

        # Device type detection logic
        if "tablet" in user_agent or (screen_width >= 768 and screen_height >= 1024):
            return DeviceType.TABLET
        elif screen_width >= 414 and screen_width <= 500:  # Large phones
            return DeviceType.PHABLET
        elif screen_width < 768:  # Small screens
            return DeviceType.SMARTPHONE
        else:
            return DeviceType.DESKTOP

    def _detect_device_capabilities(
        self, device_info: Dict[str, Any]
    ) -> List[MobileFeature]:
        """Detect available device capabilities"""
        capabilities = []

        # Check for various capabilities based on device info and user agent
        if device_info.get("has_touch", True):
            capabilities.append(MobileFeature.TOUCH_GESTURES)

        if device_info.get("has_camera", False):
            capabilities.append(MobileFeature.CAMERA_INTEGRATION)

        if device_info.get("has_microphone", False):
            capabilities.append(MobileFeature.VOICE_INPUT)

        if device_info.get("has_geolocation", False):
            capabilities.append(MobileFeature.GPS_LOCATION)

        if device_info.get("has_vibration", False):
            capabilities.append(MobileFeature.HAPTIC_FEEDBACK)

        # Always available features
        capabilities.extend(
            [MobileFeature.PUSH_NOTIFICATIONS, MobileFeature.OFFLINE_MODE]
        )

        return capabilities

    def _get_default_notification_preferences(self) -> Dict[str, bool]:
        """Get default notification preferences"""
        return {
            "quest_completed": True,
            "level_up": True,
            "pet_needs_attention": True,
            "guild_message": True,
            "daily_challenge": True,
            "study_reminder": True,
            "achievement_unlocked": True,
        }

    def _get_mobile_ui_config(self, device_type: DeviceType) -> Dict[str, Any]:
        """Get mobile UI configuration for device type"""
        base_config = MobileUIConfig()

        # Adjust for device type
        if device_type == DeviceType.SMARTPHONE:
            base_config.font_size_scale = 0.9
            base_config.touch_target_size = 44
        elif device_type == DeviceType.TABLET:
            base_config.font_size_scale = 1.1
            base_config.touch_target_size = 48
        elif device_type == DeviceType.PHABLET:
            base_config.font_size_scale = 1.0
            base_config.touch_target_size = 46

        return {
            "theme": base_config.theme,
            "font_size_scale": base_config.font_size_scale,
            "touch_target_size": base_config.touch_target_size,
            "gesture_sensitivity": base_config.gesture_sensitivity,
            "animation_speed": base_config.animation_speed,
            "components": self.ui_components,
        }

    async def render_mobile_component(
        self, session_id: str, component: UIComponent, data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Render mobile UI component with data

        Args:
            session_id: Mobile session ID
            component: UI component to render
            data: Component-specific data

        Returns:
            Rendered component data
        """
        if session_id not in self.active_sessions:
            return {"error": "Invalid session"}

        session = self.active_sessions[session_id]
        component_config = self.ui_components.get(component.value, {})

        # Get user-specific data
        user_data = await self._get_user_data(session.user_id)

        # Render component based on type
        if component == UIComponent.PLAYER_DASHBOARD:
            return await self._render_player_dashboard(session, user_data)
        elif component == UIComponent.PET_COMPANION:
            return await self._render_pet_companion(session, user_data)
        elif component == UIComponent.SKILL_TREE:
            return await self._render_skill_tree(session, user_data)
        elif component == UIComponent.QUEST_LOG:
            return await self._render_quest_log(session, user_data)
        elif component == UIComponent.GUILD_CHAT:
            return await self._render_guild_chat(session, user_data)
        else:
            return {"error": "Component not implemented"}

    async def _get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Get user data for mobile interface"""
        # Mock user data - would integrate with actual user system
        return {
            "player_id": user_id,
            "name": "Test Student",
            "level": 15,
            "xp": 2350,
            "xp_to_next_level": 650,
            "coins": 450,
            "gems": 12,
            "pet": {
                "name": "Algebra the Dragon",
                "type": "Mathematical Dragon",
                "happiness": 85,
                "hunger": 60,
                "energy": 90,
            },
            "active_quests": [
                {"id": "q1", "name": "Master Linear Transformations", "progress": 0.7},
                {"id": "q2", "name": "Pet Care Champion", "progress": 0.4},
            ],
            "guild": {"name": "Matrix Masters", "role": "member", "unread_messages": 3},
        }

    async def _render_player_dashboard(
        self, session: MobileSession, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render mobile player dashboard"""
        return {
            "component": "player_dashboard",
            "data": {
                "player_info": {
                    "name": user_data["name"],
                    "level": user_data["level"],
                    "xp_current": user_data["xp"],
                    "xp_max": user_data["xp"] + user_data["xp_to_next_level"],
                    "xp_progress": user_data["xp"]
                    / (user_data["xp"] + user_data["xp_to_next_level"]),
                },
                "currency": {"coins": user_data["coins"], "gems": user_data["gems"]},
                "quick_actions": [
                    {"icon": "🐾", "label": "Pet", "component": "pet_companion"},
                    {"icon": "🌳", "label": "Skills", "component": "skill_tree"},
                    {"icon": "📜", "label": "Quests", "component": "quest_log"},
                    {"icon": "👥", "label": "Guild", "component": "guild_chat"},
                ],
                "notifications": [
                    {
                        "type": "quest_progress",
                        "message": "Linear Transformations quest 70% complete!",
                    },
                    {"type": "pet_status", "message": "Algebra is getting hungry 🍎"},
                ],
            },
            "ui_config": self._get_mobile_ui_config(session.device_type),
        }

    async def _render_pet_companion(
        self, session: MobileSession, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render mobile pet companion interface"""
        pet_data = user_data["pet"]

        return {
            "component": "pet_companion",
            "data": {
                "pet_info": pet_data,
                "care_actions": [
                    {"action": "feed", "icon": "🍎", "cost": 10, "effect": "hunger"},
                    {"action": "play", "icon": "🎾", "cost": 0, "effect": "happiness"},
                    {"action": "study", "icon": "📚", "cost": 0, "effect": "energy"},
                ],
                "pet_status": {
                    "happiness": {
                        "value": pet_data["happiness"],
                        "max": 100,
                        "color": "green",
                    },
                    "hunger": {
                        "value": pet_data["hunger"],
                        "max": 100,
                        "color": "orange",
                    },
                    "energy": {
                        "value": pet_data["energy"],
                        "max": 100,
                        "color": "blue",
                    },
                },
                "interaction_features": [
                    (
                        "touch_to_pet"
                        if MobileFeature.TOUCH_GESTURES in session.device_capabilities
                        else None
                    ),
                    (
                        "haptic_feedback"
                        if MobileFeature.HAPTIC_FEEDBACK in session.device_capabilities
                        else None
                    ),
                ],
            },
            "ui_config": self._get_mobile_ui_config(session.device_type),
        }

    async def _render_skill_tree(
        self, session: MobileSession, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render mobile skill tree interface"""
        return {
            "component": "skill_tree",
            "data": {
                "skill_categories": [
                    {
                        "name": "Linear Algebra Foundations",
                        "progress": 0.8,
                        "skills": [
                            {"name": "Vectors", "unlocked": True, "mastered": True},
                            {
                                "name": "Matrix Operations",
                                "unlocked": True,
                                "mastered": False,
                            },
                            {
                                "name": "Determinants",
                                "unlocked": False,
                                "mastered": False,
                            },
                        ],
                    },
                    {
                        "name": "Advanced Concepts",
                        "progress": 0.3,
                        "skills": [
                            {
                                "name": "Eigenvalues",
                                "unlocked": True,
                                "mastered": False,
                            },
                            {
                                "name": "Diagonalization",
                                "unlocked": False,
                                "mastered": False,
                            },
                        ],
                    },
                ],
                "navigation_features": [
                    (
                        "pinch_zoom"
                        if MobileFeature.TOUCH_GESTURES in session.device_capabilities
                        else None
                    ),
                    (
                        "pan_navigation"
                        if MobileFeature.TOUCH_GESTURES in session.device_capabilities
                        else None
                    ),
                ],
            },
            "ui_config": self._get_mobile_ui_config(session.device_type),
        }

    async def _render_quest_log(
        self, session: MobileSession, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render mobile quest log interface"""
        return {
            "component": "quest_log",
            "data": {
                "active_quests": user_data["active_quests"],
                "completed_today": 2,
                "total_completed": 15,
                "daily_challenge": {
                    "name": "Matrix Multiplication Marathon",
                    "description": "Complete 5 matrix multiplication problems",
                    "progress": 3,
                    "total": 5,
                    "reward": "50 XP + 25 coins",
                },
                "interaction_features": [
                    (
                        "swipe_to_dismiss"
                        if MobileFeature.TOUCH_GESTURES in session.device_capabilities
                        else None
                    ),
                    (
                        "pull_to_refresh"
                        if MobileFeature.TOUCH_GESTURES in session.device_capabilities
                        else None
                    ),
                ],
            },
            "ui_config": self._get_mobile_ui_config(session.device_type),
        }

    async def _render_guild_chat(
        self, session: MobileSession, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render mobile guild chat interface"""
        guild_data = user_data["guild"]

        return {
            "component": "guild_chat",
            "data": {
                "guild_info": guild_data,
                "recent_messages": [
                    {
                        "sender": "Alex_Math",
                        "message": "Anyone need help with determinants?",
                        "time": "2 min ago",
                    },
                    {
                        "sender": "Sarah_Study",
                        "message": "Great job on yesterday's challenge everyone! 🎉",
                        "time": "15 min ago",
                    },
                    {
                        "sender": "Mike_Matrix",
                        "message": "Study group at 3 PM today?",
                        "time": "1 hour ago",
                    },
                ],
                "input_features": [
                    (
                        "voice_input"
                        if MobileFeature.VOICE_INPUT in session.device_capabilities
                        else None
                    ),
                    "emoji_picker",
                    "quick_responses",
                ],
            },
            "ui_config": self._get_mobile_ui_config(session.device_type),
        }

    async def send_push_notification(
        self, user_id: str, notification_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send push notification to mobile device"""
        if not self.notification_system:
            return {"error": "Notification system not initialized"}

        notification_config = self.notification_system["notification_types"].get(
            notification_type
        )
        if not notification_config:
            return {"error": "Unknown notification type"}

        # Format notification with user data
        title = notification_config["title"].format(**data)
        body = notification_config["body"].format(**data)

        notification = {
            "title": title,
            "body": body,
            "icon": notification_config["icon"],
            "badge": notification_config["badge"],
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"📲 Sending push notification to {user_id}: {title}")

        return {
            "success": True,
            "notification": notification,
            "delivery_status": "queued",
        }

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get mobile session status"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}

        session = self.active_sessions[session_id]

        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "device_type": session.device_type.value,
            "device_capabilities": [f.value for f in session.device_capabilities],
            "active_components": [c.value for c in session.active_components],
            "session_duration": (
                datetime.now() - session.session_start
            ).total_seconds(),
            "last_activity": session.last_activity.isoformat(),
            "offline_actions_queued": len(session.offline_actions),
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get mobile interface system status"""
        active_sessions = len(self.active_sessions)

        return {
            "system": "mobile_interface_orchestrator",
            "status": "operational",
            "active_sessions": active_sessions,
            "features": {
                "pwa_enabled": self.config.get("pwa_enabled", True),
                "offline_mode": self.config.get("offline_mode", True),
                "push_notifications": self.config.get("push_notifications", True),
            },
            "ui_components": list(self.ui_components.keys()),
            "last_updated": datetime.now().isoformat(),
        }


# Example usage and testing
async def main():
    """Example mobile interface usage"""

    # Initialize mobile interface
    mobile_interface = MobileInterfaceOrchestrator()

    # Create mobile session for student
    device_info = {
        "screen_width": 375,
        "screen_height": 812,
        "user_agent": "iPhone Safari Mobile",
        "has_touch": True,
        "has_camera": True,
        "has_microphone": True,
        "has_geolocation": True,
        "has_vibration": True,
    }

    print("📱 Creating mobile session...")
    session_result = await mobile_interface.create_mobile_session(
        "student_123", device_info
    )
    print(f"Session created: {session_result}")

    session_id = session_result["session_id"]

    # Render different components
    print("\n🎮 Rendering player dashboard...")
    dashboard = await mobile_interface.render_mobile_component(
        session_id, UIComponent.PLAYER_DASHBOARD
    )
    print(json.dumps(dashboard, indent=2, default=str))

    print("\n🐾 Rendering pet companion...")
    pet_ui = await mobile_interface.render_mobile_component(
        session_id, UIComponent.PET_COMPANION
    )
    print(json.dumps(pet_ui, indent=2, default=str))

    # Send push notification
    print("\n📲 Sending push notification...")
    notification_result = await mobile_interface.send_push_notification(
        "student_123",
        "quest_completed",
        {"quest_name": "Linear Transformations Master"},
    )
    print(f"Notification sent: {notification_result}")

    # Get session status
    session_status = mobile_interface.get_session_status(session_id)
    print(f"\n📊 Session Status: {json.dumps(session_status, indent=2, default=str)}")

    # Get system status
    system_status = mobile_interface.get_system_status()
    print(f"\n🎯 System Status: {json.dumps(system_status, indent=2, default=str)}")


if __name__ == "__main__":
    asyncio.run(main())
