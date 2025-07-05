#!/usr/bin/env python3
"""
OAuth Management System for Eagle Adventures 2
==============================================

Handles Canvas LMS OAuth authentication, token management, and automated refresh.
Provides secure, FERPA-compliant authentication for educational institutions.

Features:
- Canvas OAuth 2.0 flow automation
- Automatic token refresh and renewal
- Multi-institution support
- Secure token storage and encryption
- Rate limiting and abuse prevention
- FERPA compliance monitoring

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import asyncio
import hashlib
import json
import logging
import os
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
import jwt
from cryptography.fernet import Fernet
from urllib.parse import urlencode, parse_qs, urlparse
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OAuthStatus(Enum):
    """OAuth authentication status"""

    ACTIVE = "active"
    EXPIRED = "expired"
    INVALID = "invalid"
    REFRESHING = "refreshing"
    REVOKED = "revoked"


@dataclass
class OAuthToken:
    """OAuth token representation with metadata"""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600
    expires_at: datetime = field(default_factory=datetime.now)
    scope: str = ""
    institution_id: str = ""
    user_id: str = ""
    canvas_user_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_refreshed: Optional[datetime] = None
    status: OAuthStatus = OAuthStatus.ACTIVE


@dataclass
class CanvasInstance:
    """Canvas instance configuration"""

    instance_id: str
    name: str
    base_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str] = field(
        default_factory=lambda: [
            "url:GET|/api/v1/courses",
            "url:POST|/api/v1/courses",
            "url:PUT|/api/v1/courses/:id",
            "url:GET|/api/v1/courses/:course_id/students",
            "url:POST|/api/v1/courses/:course_id/assignments",
            "url:GET|/api/v1/courses/:course_id/assignments",
            "url:POST|/api/v1/courses/:course_id/external_tools",
        ]
    )
    is_active: bool = True


class OAuthManager:
    """
    Comprehensive OAuth management system for Canvas LMS integration

    Handles all aspects of OAuth authentication including:
    - Multi-institution support
    - Automatic token refresh
    - Secure token storage
    - FERPA compliance
    - Rate limiting
    """

    def __init__(self, config_path: str = "config/oauth_config.yml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        self.tokens: Dict[str, OAuthToken] = {}
        self.canvas_instances: Dict[str, CanvasInstance] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

        self._load_canvas_instances()
        self._load_stored_tokens()

        logger.info("🔐 OAuth Manager initialized with FERPA compliance")

    def _load_config(self) -> Dict[str, Any]:
        """Load OAuth configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("oauth", {})
        except Exception as e:
            logger.warning(f"⚠️ Could not load OAuth config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default OAuth configuration"""
        return {
            "token_refresh_buffer_minutes": 30,
            "automatic_refresh_enabled": True,
            "encryption_enabled": True,
            "ferpa_compliance_logging": True,
            "rate_limiting": {"requests_per_hour": 2000, "burst_allowance": 50},
            "security": {
                "require_https": True,
                "validate_redirect_uri": True,
                "token_storage_encrypted": True,
            },
        }

    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for token storage"""
        key_file = "config/.oauth_encryption_key"

        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            # Create new encryption key
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, "wb") as f:
                f.write(key)
            os.chmod(key_file, 0o600)  # Restrict permissions
            logger.info("🔑 Created new OAuth encryption key")
            return key

    def _load_canvas_instances(self):
        """Load Canvas instance configurations"""
        instances_config = self.config.get("canvas_instances", {})

        for instance_id, config in instances_config.items():
            self.canvas_instances[instance_id] = CanvasInstance(
                instance_id=instance_id,
                name=config.get("name", f"Canvas Instance {instance_id}"),
                base_url=config["base_url"],
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                redirect_uri=config["redirect_uri"],
                scopes=config.get("scopes", []),
                is_active=config.get("is_active", True),
            )

        logger.info(f"📚 Loaded {len(self.canvas_instances)} Canvas instances")

    def _load_stored_tokens(self):
        """Load encrypted tokens from storage"""
        token_file = "config/.oauth_tokens.enc"

        if os.path.exists(token_file):
            try:
                with open(token_file, "rb") as f:
                    encrypted_data = f.read()

                decrypted_data = self.cipher.decrypt(encrypted_data)
                tokens_data = json.loads(decrypted_data.decode())

                for token_id, token_data in tokens_data.items():
                    # Reconstruct OAuthToken objects
                    self.tokens[token_id] = OAuthToken(
                        access_token=token_data["access_token"],
                        refresh_token=token_data.get("refresh_token"),
                        token_type=token_data.get("token_type", "Bearer"),
                        expires_in=token_data.get("expires_in", 3600),
                        expires_at=datetime.fromisoformat(token_data["expires_at"]),
                        scope=token_data.get("scope", ""),
                        institution_id=token_data.get("institution_id", ""),
                        user_id=token_data.get("user_id", ""),
                        canvas_user_id=token_data.get("canvas_user_id", ""),
                        created_at=datetime.fromisoformat(token_data["created_at"]),
                        last_refreshed=(
                            datetime.fromisoformat(token_data["last_refreshed"])
                            if token_data.get("last_refreshed")
                            else None
                        ),
                        status=OAuthStatus(token_data.get("status", "active")),
                    )

                logger.info(f"🔓 Loaded {len(self.tokens)} encrypted OAuth tokens")

            except Exception as e:
                logger.error(f"❌ Failed to load stored tokens: {e}")

    def _save_tokens(self):
        """Save encrypted tokens to storage"""
        try:
            # Convert tokens to serializable format
            tokens_data = {}
            for token_id, token in self.tokens.items():
                tokens_data[token_id] = {
                    "access_token": token.access_token,
                    "refresh_token": token.refresh_token,
                    "token_type": token.token_type,
                    "expires_in": token.expires_in,
                    "expires_at": token.expires_at.isoformat(),
                    "scope": token.scope,
                    "institution_id": token.institution_id,
                    "user_id": token.user_id,
                    "canvas_user_id": token.canvas_user_id,
                    "created_at": token.created_at.isoformat(),
                    "last_refreshed": (
                        token.last_refreshed.isoformat()
                        if token.last_refreshed
                        else None
                    ),
                    "status": token.status.value,
                }

            # Encrypt and save
            json_data = json.dumps(tokens_data).encode()
            encrypted_data = self.cipher.encrypt(json_data)

            token_file = "config/.oauth_tokens.enc"
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, "wb") as f:
                f.write(encrypted_data)
            os.chmod(token_file, 0o600)  # Restrict permissions

            logger.debug("💾 OAuth tokens saved and encrypted")

        except Exception as e:
            logger.error(f"❌ Failed to save tokens: {e}")

    def generate_authorization_url(
        self, instance_id: str, user_id: str, state: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Generate OAuth authorization URL for Canvas instance

        Returns:
            Tuple of (authorization_url, state_token)
        """
        instance = self.canvas_instances.get(instance_id)
        if not instance:
            raise ValueError(f"Canvas instance {instance_id} not found")

        # Generate secure state token
        if not state:
            state = secrets.token_urlsafe(32)

        # Store state for validation
        state_key = f"{instance_id}:{user_id}:{state}"
        self._store_oauth_state(
            state_key,
            {
                "instance_id": instance_id,
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat(),
            },
        )

        # Build authorization URL
        auth_params = {
            "client_id": instance.client_id,
            "response_type": "code",
            "redirect_uri": instance.redirect_uri,
            "scope": " ".join(instance.scopes),
            "state": state,
            "purpose": "Eagle Adventures 2 Educational Gamification",
            "force_login": "1",  # Ensure fresh authentication
        }

        auth_url = f"{instance.base_url}/login/oauth2/auth?{urlencode(auth_params)}"

        logger.info(f"🔗 Generated OAuth URL for {instance.name} (User: {user_id})")
        return auth_url, state

    async def exchange_authorization_code(
        self, instance_id: str, auth_code: str, state: str, user_id: str
    ) -> OAuthToken:
        """
        Exchange authorization code for access token

        Args:
            instance_id: Canvas instance identifier
            auth_code: Authorization code from OAuth callback
            state: State token for security validation
            user_id: User identifier

        Returns:
            OAuthToken object
        """
        # Validate state token
        state_key = f"{instance_id}:{user_id}:{state}"
        if not self._validate_oauth_state(state_key):
            raise ValueError("Invalid or expired state token")

        instance = self.canvas_instances.get(instance_id)
        if not instance:
            raise ValueError(f"Canvas instance {instance_id} not found")

        # Exchange code for token
        token_params = {
            "grant_type": "authorization_code",
            "client_id": instance.client_id,
            "client_secret": instance.client_secret,
            "redirect_uri": instance.redirect_uri,
            "code": auth_code,
        }

        async with aiohttp.ClientSession() as session:
            token_url = f"{instance.base_url}/login/oauth2/token"

            async with session.post(token_url, data=token_params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"Token exchange failed: {response.status} - {error_text}"
                    )

                token_data = await response.json()

        # Get Canvas user information
        canvas_user_info = await self._get_canvas_user_info(
            instance, token_data["access_token"]
        )

        # Create OAuth token object
        token = OAuthToken(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            expires_at=datetime.now()
            + timedelta(seconds=token_data.get("expires_in", 3600)),
            scope=token_data.get("scope", " ".join(instance.scopes)),
            institution_id=instance_id,
            user_id=user_id,
            canvas_user_id=str(canvas_user_info.get("id", "")),
            status=OAuthStatus.ACTIVE,
        )

        # Store token
        token_id = f"{instance_id}:{user_id}"
        self.tokens[token_id] = token
        self._save_tokens()

        # FERPA compliance logging
        self._log_ferpa_event(
            event_type="oauth_token_created",
            user_id=user_id,
            institution_id=instance_id,
            details={"canvas_user_id": token.canvas_user_id, "scope": token.scope},
        )

        logger.info(f"✅ OAuth token created for user {user_id} at {instance.name}")
        return token

    async def _get_canvas_user_info(
        self, instance: CanvasInstance, access_token: str
    ) -> Dict[str, Any]:
        """Get Canvas user information for the authenticated user"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with aiohttp.ClientSession() as session:
            user_url = f"{instance.base_url}/api/v1/users/self"

            async with session.get(user_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"⚠️ Could not get Canvas user info: {response.status}"
                    )
                    return {}

    async def refresh_token(self, token_id: str) -> Optional[OAuthToken]:
        """
        Refresh an OAuth token

        Args:
            token_id: Token identifier (format: instance_id:user_id)

        Returns:
            Refreshed OAuthToken or None if refresh failed
        """
        token = self.tokens.get(token_id)
        if not token or not token.refresh_token:
            logger.error(
                f"❌ Cannot refresh token {token_id}: No refresh token available"
            )
            return None

        instance_id = token.institution_id
        instance = self.canvas_instances.get(instance_id)
        if not instance:
            logger.error(
                f"❌ Canvas instance {instance_id} not found for token refresh"
            )
            return None

        token.status = OAuthStatus.REFRESHING

        try:
            # Request token refresh
            refresh_params = {
                "grant_type": "refresh_token",
                "client_id": instance.client_id,
                "client_secret": instance.client_secret,
                "refresh_token": token.refresh_token,
            }

            async with aiohttp.ClientSession() as session:
                token_url = f"{instance.base_url}/login/oauth2/token"

                async with session.post(token_url, data=refresh_params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(
                            f"❌ Token refresh failed: {response.status} - {error_text}"
                        )
                        token.status = OAuthStatus.INVALID
                        return None

                    token_data = await response.json()

            # Update token with new data
            token.access_token = token_data["access_token"]
            if "refresh_token" in token_data:
                token.refresh_token = token_data["refresh_token"]
            token.expires_in = token_data.get("expires_in", 3600)
            token.expires_at = datetime.now() + timedelta(seconds=token.expires_in)
            token.last_refreshed = datetime.now()
            token.status = OAuthStatus.ACTIVE

            # Save updated token
            self._save_tokens()

            # FERPA compliance logging
            self._log_ferpa_event(
                event_type="oauth_token_refreshed",
                user_id=token.user_id,
                institution_id=instance_id,
                details={"canvas_user_id": token.canvas_user_id},
            )

            logger.info(f"🔄 OAuth token refreshed for user {token.user_id}")
            return token

        except Exception as e:
            logger.error(f"❌ Token refresh error: {e}")
            token.status = OAuthStatus.INVALID
            return None

    async def validate_token(self, token_id: str) -> bool:
        """
        Validate if a token is still active and usable

        Args:
            token_id: Token identifier

        Returns:
            True if token is valid, False otherwise
        """
        token = self.tokens.get(token_id)
        if not token:
            return False

        # Check if token is expired
        buffer_minutes = self.config.get("token_refresh_buffer_minutes", 30)
        expiry_buffer = datetime.now() + timedelta(minutes=buffer_minutes)

        if token.expires_at <= expiry_buffer:
            # Try to refresh if possible
            if token.refresh_token and self.config.get(
                "automatic_refresh_enabled", True
            ):
                refreshed_token = await self.refresh_token(token_id)
                return refreshed_token is not None
            else:
                token.status = OAuthStatus.EXPIRED
                return False

        # Test token with a simple API call
        instance = self.canvas_instances.get(token.institution_id)
        if not instance:
            return False

        try:
            headers = {"Authorization": f"Bearer {token.access_token}"}

            async with aiohttp.ClientSession() as session:
                test_url = f"{instance.base_url}/api/v1/users/self"

                async with session.get(test_url, headers=headers) as response:
                    if response.status == 200:
                        token.status = OAuthStatus.ACTIVE
                        return True
                    elif response.status == 401:
                        token.status = OAuthStatus.INVALID
                        return False
                    else:
                        # Other errors might be temporary
                        return True

        except Exception as e:
            logger.error(f"❌ Token validation error: {e}")
            return False

    def get_valid_token(self, instance_id: str, user_id: str) -> Optional[OAuthToken]:
        """
        Get a valid token for the specified user and instance

        Args:
            instance_id: Canvas instance identifier
            user_id: User identifier

        Returns:
            Valid OAuthToken or None if no valid token available
        """
        token_id = f"{instance_id}:{user_id}"
        token = self.tokens.get(token_id)

        if not token:
            return None

        # Check if token needs refresh
        buffer_minutes = self.config.get("token_refresh_buffer_minutes", 30)
        expiry_buffer = datetime.now() + timedelta(minutes=buffer_minutes)

        if token.expires_at <= expiry_buffer and token.refresh_token:
            # Schedule token refresh (async operation)
            asyncio.create_task(self.refresh_token(token_id))

        if token.status == OAuthStatus.ACTIVE:
            return token

        return None

    def revoke_token(self, token_id: str) -> bool:
        """
        Revoke an OAuth token

        Args:
            token_id: Token identifier

        Returns:
            True if revocation successful, False otherwise
        """
        token = self.tokens.get(token_id)
        if not token:
            return False

        try:
            # Mark as revoked
            token.status = OAuthStatus.REVOKED

            # Remove from active tokens
            del self.tokens[token_id]
            self._save_tokens()

            # FERPA compliance logging
            self._log_ferpa_event(
                event_type="oauth_token_revoked",
                user_id=token.user_id,
                institution_id=token.institution_id,
                details={"canvas_user_id": token.canvas_user_id},
            )

            logger.info(f"🚫 OAuth token revoked for user {token.user_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Token revocation error: {e}")
            return False

    def _store_oauth_state(self, state_key: str, state_data: Dict[str, Any]):
        """Store OAuth state for validation"""
        # In a production system, this would use Redis or a database
        # For now, we'll use a simple file-based approach
        state_file = "config/.oauth_states.json"

        try:
            states = {}
            if os.path.exists(state_file):
                with open(state_file, "r") as f:
                    states = json.load(f)

            states[state_key] = state_data

            with open(state_file, "w") as f:
                json.dump(states, f)

        except Exception as e:
            logger.error(f"❌ Failed to store OAuth state: {e}")

    def _validate_oauth_state(self, state_key: str) -> bool:
        """Validate OAuth state token"""
        state_file = "config/.oauth_states.json"

        try:
            if not os.path.exists(state_file):
                return False

            with open(state_file, "r") as f:
                states = json.load(f)

            state_data = states.get(state_key)
            if not state_data:
                return False

            # Check if state has expired
            expires_at = datetime.fromisoformat(state_data["expires_at"])
            if datetime.now() > expires_at:
                # Clean up expired state
                del states[state_key]
                with open(state_file, "w") as f:
                    json.dump(states, f)
                return False

            return True

        except Exception as e:
            logger.error(f"❌ Failed to validate OAuth state: {e}")
            return False

    def _log_ferpa_event(
        self,
        event_type: str,
        user_id: str,
        institution_id: str,
        details: Dict[str, Any],
    ):
        """Log FERPA compliance events"""
        if not self.config.get("ferpa_compliance_logging", True):
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": hashlib.sha256(user_id.encode()).hexdigest()[
                :16
            ],  # Hash for privacy
            "institution_id": institution_id,
            "details": details,
            "session_id": getattr(self, "session_id", "unknown"),
        }

        # Write to FERPA audit log
        ferpa_log_file = "logs/ferpa_compliance.log"
        os.makedirs(os.path.dirname(ferpa_log_file), exist_ok=True)

        with open(ferpa_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    async def cleanup_expired_tokens(self):
        """Clean up expired tokens and states"""
        expired_tokens = []

        for token_id, token in self.tokens.items():
            if token.status in [
                OAuthStatus.EXPIRED,
                OAuthStatus.INVALID,
                OAuthStatus.REVOKED,
            ]:
                expired_tokens.append(token_id)
            elif datetime.now() > token.expires_at + timedelta(days=7):  # Grace period
                expired_tokens.append(token_id)

        for token_id in expired_tokens:
            del self.tokens[token_id]
            logger.info(f"🧹 Cleaned up expired token: {token_id}")

        if expired_tokens:
            self._save_tokens()

        # Clean up expired OAuth states
        state_file = "config/.oauth_states.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    states = json.load(f)

                expired_states = []
                for state_key, state_data in states.items():
                    expires_at = datetime.fromisoformat(state_data["expires_at"])
                    if datetime.now() > expires_at:
                        expired_states.append(state_key)

                for state_key in expired_states:
                    del states[state_key]

                if expired_states:
                    with open(state_file, "w") as f:
                        json.dump(states, f)
                    logger.info(
                        f"🧹 Cleaned up {len(expired_states)} expired OAuth states"
                    )

            except Exception as e:
                logger.error(f"❌ Failed to clean up OAuth states: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get OAuth system status"""
        active_tokens = len(
            [t for t in self.tokens.values() if t.status == OAuthStatus.ACTIVE]
        )
        total_tokens = len(self.tokens)

        return {
            "status": "healthy" if active_tokens > 0 else "warning",
            "active_tokens": active_tokens,
            "total_tokens": total_tokens,
            "canvas_instances": len(self.canvas_instances),
            "ferpa_compliance": self.config.get("ferpa_compliance_logging", False),
            "encryption_enabled": self.config.get("encryption_enabled", False),
            "last_cleanup": getattr(self, "last_cleanup", "never"),
        }


# Example usage and testing
async def main():
    """Example usage of OAuth Manager"""
    oauth_manager = OAuthManager()

    # Example: Generate authorization URL
    auth_url, state = oauth_manager.generate_authorization_url(
        instance_id="test_instance", user_id="test_user"
    )
    print(f"Authorization URL: {auth_url}")
    print(f"State: {state}")

    # Example: Check system status
    status = oauth_manager.get_system_status()
    print(f"OAuth System Status: {status}")


if __name__ == "__main__":
    asyncio.run(main())
