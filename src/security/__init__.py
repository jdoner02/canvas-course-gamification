#!/usr/bin/env python3
"""
Security Module for Eagle Adventures 2
======================================

Comprehensive security automation system providing:
- OAuth management for Canvas LMS integration
- Privacy protection and FERPA compliance
- API rate limiting and abuse prevention
- Secure data handling and encryption

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

from .oauth_manager import OAuthManager, OAuthToken, OAuthStatus, CanvasInstance
from .privacy_protection import (
    PrivacyProtectionSystem,
    DataClassification,
    ConsentStatus,
    ConsentRecord,
    PrivacyIncident,
    PrivacyIncidentSeverity,
)
from .api_rate_limiter import APIRateLimiter, RateLimitStatus, Priority, rate_limited

__version__ = "1.0.0"

__all__ = [
    # OAuth Management
    "OAuthManager",
    "OAuthToken",
    "OAuthStatus",
    "CanvasInstance",
    # Privacy Protection
    "PrivacyProtectionSystem",
    "DataClassification",
    "ConsentStatus",
    "ConsentRecord",
    "PrivacyIncident",
    "PrivacyIncidentSeverity",
    # Rate Limiting
    "APIRateLimiter",
    "RateLimitStatus",
    "Priority",
    "rate_limited",
]


def get_security_system_status():
    """Get status of all security systems"""
    try:
        oauth_manager = OAuthManager()
        privacy_system = PrivacyProtectionSystem()
        rate_limiter = APIRateLimiter()

        return {
            "oauth_status": oauth_manager.get_system_status(),
            "privacy_status": privacy_system.get_privacy_status(),
            "rate_limiter_status": rate_limiter.get_rate_limit_status(),
        }
    except Exception as e:
        return {"error": f"Failed to get security status: {e}", "status": "error"}


async def get_security_status():
    """Get async security status for all systems"""
    try:
        oauth_manager = OAuthManager()
        privacy_system = PrivacyProtectionSystem()
        rate_limiter = APIRateLimiter()

        return {
            "overall_status": "healthy",
            "oauth_status": oauth_manager.get_system_status(),
            "privacy_status": privacy_system.get_privacy_status(),
            "rate_limiter_status": rate_limiter.get_rate_limit_status(),
            "system_health": "operational",
        }
    except Exception as e:
        return {
            "overall_status": "unhealthy",
            "error": f"Failed to get security status: {e}",
            "system_health": "error",
        }
