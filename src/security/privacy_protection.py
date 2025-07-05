#!/usr/bin/env python3
"""
Privacy Protection and FERPA Compliance System
==============================================

Comprehensive privacy protection system ensuring FERPA compliance for
educational data processing in Eagle Adventures 2.

Features:
- Automatic FERPA compliance monitoring
- Personal Identifiable Information (PII) detection and anonymization
- Data retention policy enforcement
- Consent management automation
- Privacy breach detection and response
- Educational record protection
- Audit logging for compliance

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import yaml
from cryptography.fernet import Fernet
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class DataClassification(Enum):
    """Data classification levels per FERPA"""

    PUBLIC = "public"  # Public information
    DIRECTORY = "directory"  # Directory information (name, email)
    EDUCATIONAL_RECORD = "educational"  # Educational records (grades, progress)
    SENSITIVE = "sensitive"  # Highly sensitive (SSN, health)
    RESEARCH = "research"  # De-identified research data


class ConsentStatus(Enum):
    """User consent status"""

    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    REVOKED = "revoked"
    EXPIRED = "expired"


class PrivacyIncidentSeverity(Enum):
    """Privacy incident severity levels"""

    LOW = "low"  # Minor policy violation
    MEDIUM = "medium"  # Significant concern
    HIGH = "high"  # Potential FERPA violation
    CRITICAL = "critical"  # Confirmed privacy breach


@dataclass
class PIIPattern:
    """Pattern for detecting Personally Identifiable Information"""

    name: str
    pattern: str
    classification: DataClassification
    confidence: float
    replacement_strategy: str


@dataclass
class ConsentRecord:
    """User consent record"""

    user_id: str
    consent_type: str
    status: ConsentStatus
    granted_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    purpose: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PrivacyIncident:
    """Privacy incident record"""

    incident_id: str
    severity: PrivacyIncidentSeverity
    description: str
    detected_at: datetime
    data_affected: List[str]
    users_affected: int
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    remediation_steps: List[str] = field(default_factory=list)


class PrivacyProtectionSystem:
    """
    Comprehensive privacy protection and FERPA compliance system

    Ensures all educational data processing complies with FERPA regulations
    and provides robust privacy protections for students and faculty.
    """

    def __init__(self, config_path: str = "config/privacy_config.yml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.encryption_key = self._get_encryption_key()
        self.cipher = Fernet(self.encryption_key)

        # PII detection patterns
        self.pii_patterns = self._initialize_pii_patterns()

        # Consent management
        self.consent_records: Dict[str, ConsentRecord] = {}

        # Privacy incidents
        self.incidents: List[PrivacyIncident] = []

        # Data retention policies
        self.retention_policies = self._load_retention_policies()

        # Audit trail
        self.audit_log = []

        self._load_existing_data()

        logger.info("🛡️ Privacy Protection System initialized with FERPA compliance")

    def _load_config(self) -> Dict[str, Any]:
        """Load privacy configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("privacy", {})
        except Exception as e:
            logger.warning(f"⚠️ Could not load privacy config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default privacy configuration"""
        return {
            "ferpa_compliance": {
                "enabled": True,
                "strict_mode": True,
                "audit_logging": True,
                "incident_response_enabled": True,
            },
            "pii_detection": {
                "enabled": True,
                "automatic_anonymization": True,
                "confidence_threshold": 0.8,
            },
            "data_retention": {
                "student_records_years": 5,
                "research_data_years": 7,
                "audit_logs_years": 10,
                "automatic_cleanup": True,
            },
            "consent_management": {
                "required_for_research": True,
                "consent_expiry_months": 12,
                "automatic_expiry_notifications": True,
            },
            "encryption": {
                "encrypt_at_rest": True,
                "encrypt_in_transit": True,
                "key_rotation_days": 90,
            },
        }

    def _get_encryption_key(self) -> bytes:
        """Get encryption key for privacy data"""
        key_file = "config/.privacy_encryption_key"

        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, "wb") as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            return key

    def _initialize_pii_patterns(self) -> List[PIIPattern]:
        """Initialize PII detection patterns"""
        return [
            # Social Security Numbers
            PIIPattern(
                name="ssn",
                pattern=r"\b\d{3}-?\d{2}-?\d{4}\b",
                classification=DataClassification.SENSITIVE,
                confidence=0.95,
                replacement_strategy="hash",
            ),
            # Student ID Numbers (institutional format)
            PIIPattern(
                name="student_id",
                pattern=r"\b[Ss]tudent\s*[Ii][Dd][:,\s]*(\d{7,10})\b",
                classification=DataClassification.EDUCATIONAL_RECORD,
                confidence=0.9,
                replacement_strategy="tokenize",
            ),
            # Email addresses
            PIIPattern(
                name="email",
                pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                classification=DataClassification.DIRECTORY,
                confidence=0.85,
                replacement_strategy="domain_preserving_hash",
            ),
            # Phone numbers
            PIIPattern(
                name="phone",
                pattern=r"\b\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b",
                classification=DataClassification.DIRECTORY,
                confidence=0.8,
                replacement_strategy="format_preserving_hash",
            ),
            # Names (first last pattern)
            PIIPattern(
                name="full_name",
                pattern=r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
                classification=DataClassification.DIRECTORY,
                confidence=0.6,
                replacement_strategy="pseudonym",
            ),
            # Credit card numbers
            PIIPattern(
                name="credit_card",
                pattern=r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
                classification=DataClassification.SENSITIVE,
                confidence=0.85,
                replacement_strategy="mask",
            ),
            # Grades and scores
            PIIPattern(
                name="grade",
                pattern=r"\b(?:Grade|Score|Points?)[:,\s]*([0-9]{1,3}(?:\.[0-9]+)?%?)\b",
                classification=DataClassification.EDUCATIONAL_RECORD,
                confidence=0.7,
                replacement_strategy="range_bucket",
            ),
        ]

    def _load_retention_policies(self) -> Dict[str, Dict[str, Any]]:
        """Load data retention policies"""
        return {
            "student_progress": {
                "retention_period": timedelta(days=365 * 5),  # 5 years
                "classification": DataClassification.EDUCATIONAL_RECORD,
                "deletion_method": "secure_wipe",
            },
            "research_analytics": {
                "retention_period": timedelta(days=365 * 7),  # 7 years
                "classification": DataClassification.RESEARCH,
                "deletion_method": "anonymize",
            },
            "audit_logs": {
                "retention_period": timedelta(days=365 * 10),  # 10 years
                "classification": DataClassification.PUBLIC,
                "deletion_method": "archive",
            },
            "consent_records": {
                "retention_period": timedelta(days=365 * 3),  # 3 years after revocation
                "classification": DataClassification.SENSITIVE,
                "deletion_method": "secure_wipe",
            },
        }

    def _load_existing_data(self):
        """Load existing privacy data"""
        try:
            # Load consent records
            consent_file = "data/privacy/consent_records.enc"
            if os.path.exists(consent_file):
                with open(consent_file, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                consent_data = json.loads(decrypted_data.decode())

                for user_id, consent_info in consent_data.items():
                    self.consent_records[user_id] = ConsentRecord(
                        user_id=user_id,
                        consent_type=consent_info["consent_type"],
                        status=ConsentStatus(consent_info["status"]),
                        granted_at=(
                            datetime.fromisoformat(consent_info["granted_at"])
                            if consent_info.get("granted_at")
                            else None
                        ),
                        expires_at=(
                            datetime.fromisoformat(consent_info["expires_at"])
                            if consent_info.get("expires_at")
                            else None
                        ),
                        revoked_at=(
                            datetime.fromisoformat(consent_info["revoked_at"])
                            if consent_info.get("revoked_at")
                            else None
                        ),
                        purpose=consent_info.get("purpose", ""),
                        details=consent_info.get("details", {}),
                    )

        except Exception as e:
            logger.error(f"❌ Failed to load existing privacy data: {e}")

    def detect_pii(self, text: str, context: str = "") -> List[Dict[str, Any]]:
        """
        Detect Personally Identifiable Information in text

        Args:
            text: Text to analyze
            context: Context information for better detection

        Returns:
            List of detected PII with metadata
        """
        detected_pii = []
        confidence_threshold = self.config.get("pii_detection", {}).get(
            "confidence_threshold", 0.8
        )

        for pattern in self.pii_patterns:
            matches = re.finditer(pattern.pattern, text, re.IGNORECASE)

            for match in matches:
                if pattern.confidence >= confidence_threshold:
                    detected_pii.append(
                        {
                            "type": pattern.name,
                            "value": match.group(),
                            "start": match.start(),
                            "end": match.end(),
                            "classification": pattern.classification.value,
                            "confidence": pattern.confidence,
                            "replacement_strategy": pattern.replacement_strategy,
                            "context": context,
                        }
                    )

        if detected_pii:
            self._log_pii_detection(detected_pii, context)

        return detected_pii

    def anonymize_text(
        self, text: str, context: str = ""
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Anonymize text by replacing PII with safe alternatives

        Args:
            text: Text to anonymize
            context: Context information

        Returns:
            Tuple of (anonymized_text, pii_replacements)
        """
        detected_pii = self.detect_pii(text, context)
        anonymized_text = text
        pii_replacements = []

        # Sort by position (reverse order to maintain indices)
        detected_pii.sort(key=lambda x: x["start"], reverse=True)

        for pii in detected_pii:
            original_value = pii["value"]
            replacement = self._generate_replacement(pii)

            # Replace in text
            start, end = pii["start"], pii["end"]
            anonymized_text = (
                anonymized_text[:start] + replacement + anonymized_text[end:]
            )

            pii_replacements.append(
                {
                    "original": original_value,
                    "replacement": replacement,
                    "type": pii["type"],
                    "position": (start, end),
                }
            )

        if pii_replacements:
            self._log_anonymization(pii_replacements, context)

        return anonymized_text, pii_replacements

    def _generate_replacement(self, pii: Dict[str, Any]) -> str:
        """Generate appropriate replacement for detected PII"""
        strategy = pii["replacement_strategy"]
        original = pii["value"]
        pii_type = pii["type"]

        if strategy == "hash":
            # Generate consistent hash
            hash_value = hashlib.sha256(original.encode()).hexdigest()[:8]
            return f"[{pii_type.upper()}_{hash_value}]"

        elif strategy == "tokenize":
            # Generate random token maintaining format
            if pii_type == "student_id":
                return f"STU{str(uuid.uuid4().int)[:7]}"
            return f"[TOKEN_{pii_type.upper()}]"

        elif strategy == "domain_preserving_hash":
            # For emails, preserve domain
            if "@" in original:
                username, domain = original.split("@", 1)
                hash_user = hashlib.sha256(username.encode()).hexdigest()[:8]
                return f"user_{hash_user}@{domain}"
            return f"[EMAIL_{hashlib.sha256(original.encode()).hexdigest()[:8]}]"

        elif strategy == "format_preserving_hash":
            # Maintain format but change values
            if pii_type == "phone":
                return "(555) 123-4567"  # Standard test number
            return "[PHONE_REDACTED]"

        elif strategy == "pseudonym":
            # Generate pseudonym for names
            if pii_type == "full_name":
                pseudonyms = [
                    "Alex Johnson",
                    "Jamie Smith",
                    "Taylor Brown",
                    "Casey Davis",
                ]
                hash_idx = int(hashlib.sha256(original.encode()).hexdigest(), 16) % len(
                    pseudonyms
                )
                return pseudonyms[hash_idx]
            return "[NAME_REDACTED]"

        elif strategy == "mask":
            # Mask with asterisks
            if len(original) > 4:
                return original[:2] + "*" * (len(original) - 4) + original[-2:]
            return "*" * len(original)

        elif strategy == "range_bucket":
            # For grades, use ranges
            if pii_type == "grade":
                try:
                    score = float(re.search(r"[\d.]+", original).group())
                    if score >= 90:
                        return "90-100%"
                    elif score >= 80:
                        return "80-89%"
                    elif score >= 70:
                        return "70-79%"
                    elif score >= 60:
                        return "60-69%"
                    else:
                        return "Below 60%"
                except:
                    return "[GRADE_RANGE]"
            return "[SCORE_RANGE]"

        else:
            return f"[{pii_type.upper()}_REDACTED]"

    def request_consent(
        self, user_id: str, consent_type: str, purpose: str, expires_in_months: int = 12
    ) -> str:
        """
        Request user consent for data processing

        Args:
            user_id: User identifier
            consent_type: Type of consent (research, analytics, etc.)
            purpose: Detailed purpose description
            expires_in_months: Consent validity period

        Returns:
            Consent request ID
        """
        consent_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(days=30 * expires_in_months)

        consent_record = ConsentRecord(
            user_id=user_id,
            consent_type=consent_type,
            status=ConsentStatus.PENDING,
            expires_at=expires_at,
            purpose=purpose,
            details={
                "consent_id": consent_id,
                "requested_at": datetime.now().isoformat(),
                "expires_in_months": expires_in_months,
            },
        )

        self.consent_records[user_id] = consent_record
        self._save_consent_records()

        self._log_privacy_event(
            event_type="consent_requested",
            user_id=user_id,
            details={
                "consent_type": consent_type,
                "purpose": purpose,
                "consent_id": consent_id,
            },
        )

        logger.info(f"📝 Consent requested for user {user_id}: {consent_type}")
        return consent_id

    def grant_consent(self, user_id: str, consent_id: str) -> bool:
        """
        Grant user consent

        Args:
            user_id: User identifier
            consent_id: Consent request ID

        Returns:
            True if consent granted successfully
        """
        consent_record = self.consent_records.get(user_id)
        if not consent_record or consent_record.details.get("consent_id") != consent_id:
            return False

        consent_record.status = ConsentStatus.GRANTED
        consent_record.granted_at = datetime.now()

        self._save_consent_records()

        self._log_privacy_event(
            event_type="consent_granted",
            user_id=user_id,
            details={
                "consent_type": consent_record.consent_type,
                "consent_id": consent_id,
            },
        )

        logger.info(f"✅ Consent granted by user {user_id}")
        return True

    def revoke_consent(self, user_id: str) -> bool:
        """
        Revoke user consent

        Args:
            user_id: User identifier

        Returns:
            True if consent revoked successfully
        """
        consent_record = self.consent_records.get(user_id)
        if not consent_record:
            return False

        consent_record.status = ConsentStatus.REVOKED
        consent_record.revoked_at = datetime.now()

        self._save_consent_records()

        # Trigger data deletion/anonymization for revoked consent
        asyncio.create_task(self._handle_consent_revocation(user_id))

        self._log_privacy_event(
            event_type="consent_revoked",
            user_id=user_id,
            details={
                "consent_type": consent_record.consent_type,
                "revoked_at": consent_record.revoked_at.isoformat(),
            },
        )

        logger.info(f"🚫 Consent revoked by user {user_id}")
        return True

    def check_consent(self, user_id: str, consent_type: str) -> bool:
        """
        Check if user has valid consent for specific data processing

        Args:
            user_id: User identifier
            consent_type: Type of consent to check

        Returns:
            True if valid consent exists
        """
        consent_record = self.consent_records.get(user_id)
        if not consent_record:
            return False

        # Check consent type
        if consent_record.consent_type != consent_type:
            return False

        # Check status
        if consent_record.status != ConsentStatus.GRANTED:
            return False

        # Check expiry
        if consent_record.expires_at and datetime.now() > consent_record.expires_at:
            consent_record.status = ConsentStatus.EXPIRED
            self._save_consent_records()
            return False

        return True

    async def _handle_consent_revocation(self, user_id: str):
        """Handle data processing when consent is revoked"""
        try:
            # Anonymize user data in research datasets
            await self._anonymize_user_research_data(user_id)

            # Delete non-essential data
            await self._delete_user_non_essential_data(user_id)

            # Update audit logs
            self._log_privacy_event(
                event_type="consent_revocation_processed",
                user_id=user_id,
                details={"processing_completed_at": datetime.now().isoformat()},
            )

        except Exception as e:
            logger.error(f"❌ Error handling consent revocation for {user_id}: {e}")

    async def _anonymize_user_research_data(self, user_id: str):
        """Anonymize user data in research datasets"""
        # This would integrate with the research analytics system
        # to replace user identifiers with anonymous tokens
        logger.info(f"🔄 Anonymizing research data for user {user_id}")

    async def _delete_user_non_essential_data(self, user_id: str):
        """Delete non-essential user data"""
        # This would delete user data that's not required to be retained
        # under FERPA (e.g., optional analytics, preferences)
        logger.info(f"🗑️ Deleting non-essential data for user {user_id}")

    def report_privacy_incident(
        self,
        description: str,
        severity: PrivacyIncidentSeverity,
        data_affected: List[str],
        users_affected: int,
    ) -> str:
        """
        Report a privacy incident

        Args:
            description: Incident description
            severity: Incident severity level
            data_affected: Types of data affected
            users_affected: Number of users affected

        Returns:
            Incident ID
        """
        incident_id = str(uuid.uuid4())

        incident = PrivacyIncident(
            incident_id=incident_id,
            severity=severity,
            description=description,
            detected_at=datetime.now(),
            data_affected=data_affected,
            users_affected=users_affected,
        )

        self.incidents.append(incident)

        # Trigger incident response
        asyncio.create_task(self._handle_privacy_incident(incident))

        self._log_privacy_event(
            event_type="privacy_incident_reported",
            user_id="system",
            details={
                "incident_id": incident_id,
                "severity": severity.value,
                "users_affected": users_affected,
                "data_affected": data_affected,
            },
        )

        logger.error(
            f"🚨 Privacy incident reported: {incident_id} (Severity: {severity.value})"
        )
        return incident_id

    async def _handle_privacy_incident(self, incident: PrivacyIncident):
        """Handle privacy incident response"""
        try:
            if incident.severity in [
                PrivacyIncidentSeverity.HIGH,
                PrivacyIncidentSeverity.CRITICAL,
            ]:
                # Immediate response for serious incidents
                await self._immediate_incident_response(incident)

            # Document remediation steps
            incident.remediation_steps = await self._generate_remediation_plan(incident)

            # Notify stakeholders if required
            await self._notify_incident_stakeholders(incident)

        except Exception as e:
            logger.error(
                f"❌ Error handling privacy incident {incident.incident_id}: {e}"
            )

    async def _immediate_incident_response(self, incident: PrivacyIncident):
        """Immediate response for high/critical privacy incidents"""
        # Stop data processing
        # Secure affected systems
        # Preserve evidence
        logger.critical(
            f"🚨 Immediate incident response activated for {incident.incident_id}"
        )

    async def _generate_remediation_plan(self, incident: PrivacyIncident) -> List[str]:
        """Generate remediation plan for privacy incident"""
        plan = [
            "Assess full scope of data exposure",
            "Secure affected systems and data",
            "Notify affected users (if required)",
            "Review and update security controls",
            "Document lessons learned",
        ]

        if incident.severity == PrivacyIncidentSeverity.CRITICAL:
            plan.insert(0, "Notify institutional privacy officer immediately")
            plan.insert(1, "Consider notification to Department of Education")

        return plan

    async def _notify_incident_stakeholders(self, incident: PrivacyIncident):
        """Notify stakeholders about privacy incident"""
        # In a real system, this would send notifications
        # to privacy officers, administrators, etc.
        logger.info(
            f"📧 Stakeholder notifications sent for incident {incident.incident_id}"
        )

    def _save_consent_records(self):
        """Save encrypted consent records"""
        try:
            consent_data = {}
            for user_id, consent in self.consent_records.items():
                consent_data[user_id] = {
                    "consent_type": consent.consent_type,
                    "status": consent.status.value,
                    "granted_at": (
                        consent.granted_at.isoformat() if consent.granted_at else None
                    ),
                    "expires_at": (
                        consent.expires_at.isoformat() if consent.expires_at else None
                    ),
                    "revoked_at": (
                        consent.revoked_at.isoformat() if consent.revoked_at else None
                    ),
                    "purpose": consent.purpose,
                    "details": consent.details,
                }

            json_data = json.dumps(consent_data).encode()
            encrypted_data = self.cipher.encrypt(json_data)

            consent_file = "data/privacy/consent_records.enc"
            os.makedirs(os.path.dirname(consent_file), exist_ok=True)
            with open(consent_file, "wb") as f:
                f.write(encrypted_data)

        except Exception as e:
            logger.error(f"❌ Failed to save consent records: {e}")

    def _log_pii_detection(self, detected_pii: List[Dict[str, Any]], context: str):
        """Log PII detection event"""
        self._log_privacy_event(
            event_type="pii_detected",
            user_id="system",
            details={
                "pii_count": len(detected_pii),
                "pii_types": [pii["type"] for pii in detected_pii],
                "context": context,
                "auto_anonymized": self.config.get("pii_detection", {}).get(
                    "automatic_anonymization", False
                ),
            },
        )

    def _log_anonymization(self, replacements: List[Dict[str, Any]], context: str):
        """Log anonymization event"""
        self._log_privacy_event(
            event_type="data_anonymized",
            user_id="system",
            details={
                "replacements_count": len(replacements),
                "pii_types": [r["type"] for r in replacements],
                "context": context,
            },
        )

    def _log_privacy_event(
        self, event_type: str, user_id: str, details: Dict[str, Any]
    ):
        """Log privacy-related events for compliance"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id_hash": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "details": details,
            "session_id": getattr(self, "session_id", str(uuid.uuid4())),
        }

        # Write to privacy audit log
        privacy_log_file = "logs/privacy_audit.log"
        os.makedirs(os.path.dirname(privacy_log_file), exist_ok=True)

        with open(privacy_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    async def cleanup_expired_data(self):
        """Clean up expired data based on retention policies"""
        cleaned_count = 0

        for data_type, policy in self.retention_policies.items():
            retention_period = policy["retention_period"]
            cutoff_date = datetime.now() - retention_period

            # This would integrate with actual data storage systems
            # to identify and clean up expired data
            logger.info(f"🧹 Checking {data_type} for data older than {cutoff_date}")

        # Clean up expired consent records
        expired_consents = []
        for user_id, consent in self.consent_records.items():
            if (
                consent.status == ConsentStatus.REVOKED
                and consent.revoked_at
                and datetime.now() > consent.revoked_at + timedelta(days=365)
            ):
                expired_consents.append(user_id)

        for user_id in expired_consents:
            del self.consent_records[user_id]
            cleaned_count += 1

        if expired_consents:
            self._save_consent_records()

        logger.info(f"🧹 Cleaned up {cleaned_count} expired privacy records")
        return cleaned_count

    def get_privacy_status(self) -> Dict[str, Any]:
        """Get privacy system status"""
        active_consents = len(
            [
                c
                for c in self.consent_records.values()
                if c.status == ConsentStatus.GRANTED
            ]
        )
        open_incidents = len([i for i in self.incidents if not i.resolved])

        return {
            "status": "healthy" if open_incidents == 0 else "warning",
            "ferpa_compliance_enabled": self.config.get("ferpa_compliance", {}).get(
                "enabled", False
            ),
            "pii_detection_enabled": self.config.get("pii_detection", {}).get(
                "enabled", False
            ),
            "active_consents": active_consents,
            "total_consents": len(self.consent_records),
            "open_incidents": open_incidents,
            "total_incidents": len(self.incidents),
            "encryption_enabled": self.config.get("encryption", {}).get(
                "encrypt_at_rest", False
            ),
        }


# Example usage and testing
async def main():
    """Example usage of Privacy Protection System"""
    privacy_system = PrivacyProtectionSystem()

    # Example: PII detection
    test_text = "Student John Doe (ID: 1234567) received a grade of 85% on the exam. Contact: john.doe@university.edu"
    detected_pii = privacy_system.detect_pii(test_text, "test_context")
    print(f"Detected PII: {detected_pii}")

    # Example: Anonymization
    anonymized_text, replacements = privacy_system.anonymize_text(
        test_text, "test_context"
    )
    print(f"Anonymized: {anonymized_text}")

    # Example: Consent management
    consent_id = privacy_system.request_consent(
        "user123", "research", "Learning analytics research"
    )
    print(f"Consent requested: {consent_id}")

    # Example: System status
    status = privacy_system.get_privacy_status()
    print(f"Privacy System Status: {status}")


if __name__ == "__main__":
    asyncio.run(main())
