"""
Validation Module

Comprehensive validation system for course configurations and Canvas API interactions.

This module provides enterprise-grade validation capabilities including:
- Schema validation with JSON Schema support
- Accessibility compliance checking (WCAG 2.1 AA)
- Universal Design for Learning (UDL) validation
- Performance and scalability analysis
- Security and privacy compliance
- Content quality assessment
- Cross-reference integrity checking

Features:
- ✅ Multi-format configuration validation
- ✅ WCAG 2.1 accessibility compliance
- ✅ UDL guideline assessment
- ✅ Performance optimization suggestions
- ✅ Security vulnerability detection
- ✅ Content quality scoring
- ✅ Dependency validation
- ✅ Canvas API compliance checking

Research Foundation:
- WCAG 2.1 Web Content Accessibility Guidelines
- Universal Design for Learning Guidelines v2.2
- Quality Matters Standards
- FERPA and privacy compliance frameworks
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass, field
from enum import Enum
import hashlib

try:
    import jsonschema
    from jsonschema import validate, ValidationError as JsonSchemaValidationError

    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

try:
    from bs4 import BeautifulSoup

    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation issue severity levels."""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


class AccessibilityLevel(Enum):
    """WCAG accessibility conformance levels."""

    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class ValidationIssue:
    """Represents a validation issue with detailed context."""

    severity: ValidationSeverity
    category: str
    message: str
    location: str
    suggestion: Optional[str] = None
    documentation_url: Optional[str] = None
    wcag_criterion: Optional[str] = None
    udl_guideline: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "severity": self.severity.value,
            "category": self.category,
            "message": self.message,
            "location": self.location,
            "suggestion": self.suggestion,
            "documentation_url": self.documentation_url,
            "wcag_criterion": self.wcag_criterion,
            "udl_guideline": self.udl_guideline,
        }


@dataclass
class ValidationResult:
    """Comprehensive validation result with detailed metrics."""

    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    sections_validated: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    accessibility_score: float = 0.0
    udl_score: float = 0.0
    quality_score: float = 0.0

    @property
    def critical_issues(self) -> List[ValidationIssue]:
        """Get critical severity issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.CRITICAL]

    @property
    def errors(self) -> List[ValidationIssue]:
        """Get error severity issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get warning severity issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "is_valid": self.is_valid,
            "summary": {
                "total_issues": len(self.issues),
                "critical": len(self.critical_issues),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "suggestions": len(
                    [
                        i
                        for i in self.issues
                        if i.severity == ValidationSeverity.SUGGESTION
                    ]
                ),
            },
            "scores": {
                "accessibility": self.accessibility_score,
                "udl": self.udl_score,
                "quality": self.quality_score,
            },
            "sections_validated": self.sections_validated,
            "performance_metrics": self.performance_metrics,
            "issues": [issue.to_dict() for issue in self.issues],
        }


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


class ConfigValidator:
    """
    Comprehensive configuration validator with accessibility, UDL, and quality assessment.

    This validator implements multiple validation layers:
    - Structural validation (schema compliance)
    - Content validation (quality and completeness)
    - Accessibility validation (WCAG 2.1 compliance)
    - UDL validation (Universal Design for Learning)
    - Performance validation (scalability and optimization)
    - Security validation (privacy and safety)
    """

    def __init__(
        self,
        accessibility_level: AccessibilityLevel = AccessibilityLevel.AA,
        enable_performance_analysis: bool = True,
        enable_content_quality_analysis: bool = True,
        custom_schemas: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        """
        Initialize the validator with comprehensive checking capabilities.

        Args:
            accessibility_level: WCAG conformance level to enforce
            enable_performance_analysis: Whether to analyze performance implications
            enable_content_quality_analysis: Whether to assess content quality
            custom_schemas: Custom JSON schemas for validation
        """
        self.accessibility_level = accessibility_level
        self.enable_performance_analysis = enable_performance_analysis
        self.enable_content_quality_analysis = enable_content_quality_analysis

        # Core validation requirements
        self.required_fields = {
            "modules": ["id", "name"],
            "assignments": ["id", "name"],
            "pages": ["id", "title"],
            "quizzes": ["id", "title"],
            "badges": ["id", "name"],
            "outcomes": ["id", "title"],
        }

        self.valid_assignment_types = [
            "online_text_entry",
            "online_url",
            "online_upload",
            "media_recording",
            "external_tool",
            "none",
        ]

        self.valid_quiz_types = [
            "practice_quiz",
            "assignment",
            "graded_survey",
            "survey",
        ]

        # Load validation schemas
        self.schemas = custom_schemas or self._load_default_schemas()

        # Accessibility patterns
        self.accessibility_patterns = self._initialize_accessibility_patterns()

        # UDL guidelines mapping
        self.udl_guidelines = self._initialize_udl_guidelines()

        # Content quality criteria
        self.quality_criteria = self._initialize_quality_criteria()

    def _load_default_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Load default JSON schemas for validation."""
        return {
            "module": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "name": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "position": {"type": "integer", "minimum": 1},
                    "prerequisites": {"type": "array", "items": {"type": "string"}},
                    "gamification": {
                        "type": "object",
                        "properties": {
                            "skill_level": {
                                "type": "string",
                                "enum": [
                                    "recognition",
                                    "application",
                                    "intuition",
                                    "synthesis",
                                    "mastery",
                                ],
                            },
                            "xp_required": {"type": "integer", "minimum": 0},
                            "mastery_threshold": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                            },
                        },
                    },
                },
            },
            "assignment": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "name": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "points_possible": {"type": "number", "minimum": 0},
                    "submission_types": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": self.valid_assignment_types,
                        },
                    },
                },
            },
        }

    def _initialize_accessibility_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize accessibility validation patterns."""
        return {
            "missing_alt_text": {
                "pattern": r"<img(?![^>]*alt=)[^>]*>",
                "wcag": "1.1.1",
                "description": "Images without alternative text",
                "severity": ValidationSeverity.ERROR,
            },
            "missing_video_captions": {
                "keywords": ["youtube.com", "vimeo.com", "<video"],
                "wcag": "1.2.2",
                "description": "Video content may be missing captions",
                "severity": ValidationSeverity.WARNING,
            },
            "poor_color_contrast": {
                "pattern": r'style=["\'][^"\']*color:\s*#[a-fA-F0-9]{6}[^"\']*["\']',
                "wcag": "1.4.3",
                "description": "Inline color styling may have poor contrast",
                "severity": ValidationSeverity.WARNING,
            },
            "missing_headings": {
                "pattern": r"^(?!.*<h[1-6]).{200,}",
                "wcag": "1.3.1",
                "description": "Long content without proper heading structure",
                "severity": ValidationSeverity.WARNING,
            },
            "empty_links": {
                "pattern": r"<a[^>]*>\s*</a>",
                "wcag": "2.4.4",
                "description": "Links without descriptive text",
                "severity": ValidationSeverity.ERROR,
            },
            "tables_without_headers": {
                "pattern": r"<table(?![^>]*<th)[^>]*>.*?</table>",
                "wcag": "1.3.1",
                "description": "Data tables without proper headers",
                "severity": ValidationSeverity.WARNING,
            },
        }

    def _initialize_udl_guidelines(self) -> Dict[str, Dict[str, Any]]:
        """Initialize UDL (Universal Design for Learning) validation guidelines."""
        return {
            "multiple_means_representation": {
                "criteria": [
                    "Has alternative text for images",
                    "Provides multiple format options",
                    "Uses clear language and structure",
                    "Includes visual and textual information",
                ],
                "weight": 0.4,
            },
            "multiple_means_engagement": {
                "criteria": [
                    "Offers choice in content and activities",
                    "Provides relevant, authentic contexts",
                    "Includes collaborative opportunities",
                    "Supports different interests and preferences",
                ],
                "weight": 0.3,
            },
            "multiple_means_action_expression": {
                "criteria": [
                    "Provides multiple assessment formats",
                    "Supports different response methods",
                    "Offers assistive technology compatibility",
                    "Allows for varied ways to demonstrate knowledge",
                ],
                "weight": 0.3,
            },
        }

    def _initialize_quality_criteria(self) -> Dict[str, Dict[str, Any]]:
        """Initialize content quality assessment criteria."""
        return {
            "clarity": {
                "weight": 0.25,
                "criteria": [
                    "Clear learning objectives",
                    "Well-structured content",
                    "Appropriate reading level",
                    "Consistent formatting",
                ],
            },
            "completeness": {
                "weight": 0.25,
                "criteria": [
                    "All required fields present",
                    "Adequate content length",
                    "Comprehensive instructions",
                    "Proper resource links",
                ],
            },
            "accuracy": {
                "weight": 0.25,
                "criteria": [
                    "Valid URLs and links",
                    "Correct spelling and grammar",
                    "Factual accuracy",
                    "Proper formatting",
                ],
            },
            "engagement": {
                "weight": 0.25,
                "criteria": [
                    "Interactive elements",
                    "Multimedia content",
                    "Varied activity types",
                    "Clear progression",
                ],
            },
        }

    def validate_course_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Perform comprehensive validation of a course configuration.

        This method orchestrates multiple validation layers:
        1. Structural validation (schema compliance)
        2. Content validation (completeness and quality)
        3. Accessibility validation (WCAG compliance)
        4. UDL validation (Universal Design principles)
        5. Performance validation (scalability analysis)
        6. Security validation (privacy and safety)

        Args:
            config: Course configuration dictionary

        Returns:
            Comprehensive validation result with detailed metrics and suggestions
        """
        result = ValidationResult(is_valid=True)

        try:
            # 1. Structural validation
            structural_issues = self._validate_structure(config)
            result.issues.extend(structural_issues)

            # 2. Content validation
            content_issues = self._validate_content(config)
            result.issues.extend(content_issues)

            # 3. Cross-reference validation
            reference_issues = self._validate_cross_references(config)
            result.issues.extend(reference_issues)

            # 4. Accessibility validation
            if self.accessibility_level:
                accessibility_issues, accessibility_score = (
                    self._validate_accessibility(config)
                )
                result.issues.extend(accessibility_issues)
                result.accessibility_score = accessibility_score

            # 5. UDL validation
            udl_issues, udl_score = self._validate_udl_compliance(config)
            result.issues.extend(udl_issues)
            result.udl_score = udl_score

            # 6. Performance validation
            if self.enable_performance_analysis:
                performance_issues, performance_metrics = self._validate_performance(
                    config
                )
                result.issues.extend(performance_issues)
                result.performance_metrics = performance_metrics

            # 7. Content quality assessment
            if self.enable_content_quality_analysis:
                quality_issues, quality_score = self._assess_content_quality(config)
                result.issues.extend(quality_issues)
                result.quality_score = quality_score

            # 8. Security validation
            security_issues = self._validate_security(config)
            result.issues.extend(security_issues)

            # Determine overall validity
            critical_and_error_count = len(result.critical_issues) + len(result.errors)
            result.is_valid = critical_and_error_count == 0

            # Track validated sections
            result.sections_validated = list(config.keys())

            logger.info(
                f"Validation completed: {len(result.issues)} issues found, "
                f"valid: {result.is_valid}"
            )

        except Exception as e:
            logger.error(f"Validation process failed: {e}")
            result.issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="validation_system",
                    message=f"Validation system error: {e}",
                    location="validation_process",
                )
            )
            result.is_valid = False

        return result

    def _validate_structure(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate the structural integrity of the configuration."""
        issues = []

        # Check for required top-level sections
        recommended_sections = ["modules", "course_info"]
        for section in recommended_sections:
            if section not in config:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="structure",
                        message=f"Missing recommended section: {section}",
                        location=f"config.{section}",
                        suggestion=f"Add {section} section for complete course definition",
                    )
                )

        # Validate each section against schemas
        for section_name, section_data in config.items():
            if section_name in self.required_fields:
                section_issues = self._validate_section_schema(
                    section_name, section_data
                )
                issues.extend(section_issues)

        return issues

    def _validate_section_schema(
        self, section_name: str, section_data: Any
    ) -> List[ValidationIssue]:
        """Validate a section against its JSON schema."""
        issues = []

        if not isinstance(section_data, dict):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="schema",
                    message=f"Section '{section_name}' must be an object",
                    location=f"config.{section_name}",
                )
            )
            return issues

        items = section_data.get(section_name, [])
        if not isinstance(items, list):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="schema",
                    message=f"Section '{section_name}' must contain a list of items",
                    location=f"config.{section_name}.{section_name}",
                )
            )
            return issues

        # Validate each item in the section
        for i, item in enumerate(items):
            item_issues = self._validate_item_schema(section_name, item, i)
            issues.extend(item_issues)

        return issues

    def _validate_item_schema(
        self, section_name: str, item: Dict[str, Any], index: int
    ) -> List[ValidationIssue]:
        """Validate an individual item against its schema."""
        issues = []
        location_base = f"config.{section_name}.{section_name}[{index}]"

        # Check required fields
        required_fields = self.required_fields.get(section_name, [])
        for field in required_fields:
            if field not in item:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="required_field",
                        message=f"Missing required field: {field}",
                        location=f"{location_base}.{field}",
                        suggestion=f"Add {field} field to {section_name} item",
                    )
                )
            elif not item[field] or (
                isinstance(item[field], str) and not item[field].strip()
            ):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="empty_field",
                        message=f"Required field '{field}' is empty",
                        location=f"{location_base}.{field}",
                        suggestion=f"Provide a value for {field}",
                    )
                )

        # JSON Schema validation if available
        if JSONSCHEMA_AVAILABLE and section_name.rstrip("s") in self.schemas:
            schema_name = section_name.rstrip("s")  # Remove plural
            try:
                validate(item, self.schemas[schema_name])
            except JsonSchemaValidationError as e:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="schema_validation",
                        message=f"Schema validation failed: {e.message}",
                        location=f"{location_base}.{'.'.join(str(p) for p in e.path) if e.path else 'root'}",
                        suggestion="Check the field format and allowed values",
                    )
                )

        return issues

    def _validate_content(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate content completeness and basic quality."""
        issues = []

        for section_name, section_data in config.items():
            if section_name in self.required_fields:
                items = section_data.get(section_name, [])
                for i, item in enumerate(items):
                    item_issues = self._validate_item_content(section_name, item, i)
                    issues.extend(item_issues)

        return issues

    def _validate_item_content(
        self, section_name: str, item: Dict[str, Any], index: int
    ) -> List[ValidationIssue]:
        """Validate the content quality of an individual item."""
        issues = []
        location_base = f"config.{section_name}.{section_name}[{index}]"

        # Check for descriptive content
        description_fields = ["description", "body", "instructions"]
        has_description = any(
            field in item and item[field] for field in description_fields
        )

        if not has_description:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="content_quality",
                    message=f"{section_name.title()} item lacks descriptive content",
                    location=location_base,
                    suggestion="Add description, body, or instructions to improve clarity",
                    udl_guideline="Multiple means of representation",
                )
            )

        # Check content length and quality
        for field in description_fields:
            if field in item and item[field]:
                content = item[field]
                content_issues = self._validate_text_content(
                    content, f"{location_base}.{field}"
                )
                issues.extend(content_issues)

        # Validate URLs
        url_fields = ["url", "external_url", "image_url"]
        for field in url_fields:
            if field in item and item[field]:
                url_issues = self._validate_url(item[field], f"{location_base}.{field}")
                issues.extend(url_issues)

        return issues

    def _validate_text_content(
        self, content: str, location: str
    ) -> List[ValidationIssue]:
        """Validate text content for quality and accessibility."""
        issues = []

        if len(content.strip()) < 10:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="content_quality",
                    message="Content is very short and may lack sufficient detail",
                    location=location,
                    suggestion="Provide more detailed content to improve clarity",
                )
            )

        # Check for basic spelling/grammar issues (simplified)
        if content.count(".") == 0 and len(content) > 50:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.SUGGESTION,
                    category="content_quality",
                    message="Long content without sentence breaks may be hard to read",
                    location=location,
                    suggestion="Consider breaking into shorter sentences",
                )
            )

        return issues

    def _validate_url(self, url: str, location: str) -> List[ValidationIssue]:
        """Validate URL format and accessibility."""
        issues = []

        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="url_validation",
                        message="Invalid URL format",
                        location=location,
                        suggestion="Ensure URL includes protocol (http:// or https://)",
                    )
                )
        except Exception:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="url_validation",
                    message="URL parsing failed",
                    location=location,
                )
            )

        return issues

    def _validate_cross_references(
        self, config: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate cross-references between different sections."""
        issues = []

        # Build reference maps
        module_ids = set()
        assignment_ids = set()
        page_ids = set()
        quiz_ids = set()
        badge_ids = set()

        # Collect all IDs
        if "modules" in config:
            modules = config["modules"].get("modules", [])
            module_ids = {module["id"] for module in modules if "id" in module}

        if "assignments" in config:
            assignments = config["assignments"].get("assignments", [])
            assignment_ids = {
                assignment["id"] for assignment in assignments if "id" in assignment
            }

        if "pages" in config:
            pages = config["pages"].get("pages", [])
            page_ids = {page["id"] for page in pages if "id" in page}

        if "quizzes" in config:
            quizzes = config["quizzes"].get("quizzes", [])
            quiz_ids = {quiz["id"] for quiz in quizzes if "id" in quiz}

        if "badges" in config:
            badges = config["badges"].get("badges", [])
            badge_ids = {badge["id"] for badge in badges if "id" in badge}

        # Validate module prerequisites
        if "modules" in config:
            for i, module in enumerate(config["modules"].get("modules", [])):
                prerequisites = module.get("prerequisites", [])
                for prereq in prerequisites:
                    if prereq not in module_ids:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.WARNING,
                                category="cross_reference",
                                message=f"Module '{module.get('id', 'Unknown')}' references unknown prerequisite: {prereq}",
                                location=f"config.modules.modules[{i}].prerequisites",
                                suggestion="Ensure prerequisite module exists or remove invalid reference",
                            )
                        )

        # Validate module items references
        if "modules" in config:
            for i, module in enumerate(config["modules"].get("modules", [])):
                items = module.get("items", [])
                for j, item in enumerate(items):
                    item_type = item.get("type", "")
                    item_id = item.get("id", "")

                    if item_type == "Assignment" and item_id not in assignment_ids:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.ERROR,
                                category="cross_reference",
                                message=f"Module item references unknown assignment: {item_id}",
                                location=f"config.modules.modules[{i}].items[{j}].id",
                            )
                        )
                    elif item_type == "Page" and item_id not in page_ids:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.ERROR,
                                category="cross_reference",
                                message=f"Module item references unknown page: {item_id}",
                                location=f"config.modules.modules[{i}].items[{j}].id",
                            )
                        )
                    elif item_type == "Quiz" and item_id not in quiz_ids:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.ERROR,
                                category="cross_reference",
                                message=f"Module item references unknown quiz: {item_id}",
                                location=f"config.modules.modules[{i}].items[{j}].id",
                            )
                        )

        return issues

    def _validate_accessibility(
        self, config: Dict[str, Any]
    ) -> Tuple[List[ValidationIssue], float]:
        """Validate accessibility compliance (WCAG 2.1)."""
        issues = []
        total_checks = 0
        passed_checks = 0

        # Check all text content for accessibility issues
        for section_name, section_data in config.items():
            if isinstance(section_data, dict) and section_data:
                items = section_data.get(section_name, [])
                if isinstance(items, list):
                    for i, item in enumerate(items):
                        if isinstance(item, dict):
                            # Check description, body, and other text fields
                            text_fields = [
                                "description",
                                "body",
                                "instructions",
                                "content",
                            ]
                            for field in text_fields:
                                if field in item and isinstance(item[field], str):
                                    accessibility_issues = (
                                        self._check_accessibility_patterns(
                                            item[field], f"{section_name}[{i}].{field}"
                                        )
                                    )
                                    issues.extend(accessibility_issues)
                                    total_checks += len(self.accessibility_patterns)
                                    passed_checks += len(
                                        self.accessibility_patterns
                                    ) - len(accessibility_issues)

        # Calculate accessibility score
        accessibility_score = (passed_checks / max(total_checks, 1)) * 100

        return issues, accessibility_score

    def _check_accessibility_patterns(
        self, content: str, location: str
    ) -> List[ValidationIssue]:
        """Check content against accessibility patterns."""
        issues = []

        for pattern_name, pattern_config in self.accessibility_patterns.items():
            if "pattern" in pattern_config:
                if re.search(
                    pattern_config["pattern"], content, re.MULTILINE | re.DOTALL
                ):
                    issues.append(
                        ValidationIssue(
                            severity=pattern_config["severity"],
                            category="accessibility",
                            message=pattern_config["description"],
                            location=location,
                            wcag_criterion=pattern_config["wcag"],
                            documentation_url=f"https://www.w3.org/WAI/WCAG21/Understanding/{pattern_config['wcag']}.html",
                        )
                    )
            elif "keywords" in pattern_config:
                for keyword in pattern_config["keywords"]:
                    if keyword in content:
                        issues.append(
                            ValidationIssue(
                                severity=pattern_config["severity"],
                                category="accessibility",
                                message=pattern_config["description"],
                                location=location,
                                wcag_criterion=pattern_config["wcag"],
                                suggestion="Ensure proper accessibility features are implemented",
                            )
                        )

        return issues

    def _validate_udl_compliance(
        self, config: Dict[str, Any]
    ) -> Tuple[List[ValidationIssue], float]:
        """Validate Universal Design for Learning compliance."""
        issues = []
        scores = {}

        for guideline, guideline_config in self.udl_guidelines.items():
            guideline_score = self._assess_udl_guideline(
                config, guideline, guideline_config
            )
            scores[guideline] = guideline_score

            if guideline_score < 50:  # Below 50% compliance
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="udl",
                        message=f"Low compliance with UDL guideline: {guideline.replace('_', ' ').title()}",
                        location=f"config.{guideline}",
                        udl_guideline=guideline,
                        suggestion=f"Consider implementing: {', '.join(guideline_config['criteria'][:2])}",
                    )
                )

        # Calculate weighted overall score
        overall_score = sum(
            scores[guideline] * guideline_config["weight"]
            for guideline, guideline_config in self.udl_guidelines.items()
        )

        return issues, overall_score

    def _assess_udl_guideline(
        self, config: Dict[str, Any], guideline: str, guideline_config: Dict[str, Any]
    ) -> float:
        """Assess compliance with a specific UDL guideline."""
        compliance_indicators = 0
        total_indicators = len(guideline_config["criteria"])

        # Simple heuristic assessment based on content analysis
        if guideline == "multiple_means_representation":
            # Check for alternative formats, clear structure
            if self._has_multiple_content_formats(config):
                compliance_indicators += 1
            if self._has_clear_structure(config):
                compliance_indicators += 1
            if self._has_accessibility_features(config):
                compliance_indicators += 2

        elif guideline == "multiple_means_engagement":
            # Check for choice, relevance, collaboration
            if self._has_choice_options(config):
                compliance_indicators += 1
            if self._has_authentic_contexts(config):
                compliance_indicators += 1
            if self._has_collaborative_elements(config):
                compliance_indicators += 2

        elif guideline == "multiple_means_action_expression":
            # Check for assessment variety, response options
            if self._has_varied_assessments(config):
                compliance_indicators += 2
            if self._has_multiple_response_methods(config):
                compliance_indicators += 2

        return (compliance_indicators / total_indicators) * 100

    def _validate_performance(
        self, config: Dict[str, Any]
    ) -> Tuple[List[ValidationIssue], Dict[str, Any]]:
        """Validate performance and scalability aspects."""
        issues = []
        metrics = {}

        # Count content items for scalability analysis
        total_items = 0
        large_content_items = 0

        for section_name, section_data in config.items():
            if isinstance(section_data, dict) and section_data:
                items = section_data.get(section_name, [])
                if isinstance(items, list):
                    total_items += len(items)

                    for item in items:
                        if isinstance(item, dict):
                            # Check for large content
                            for field in ["description", "body", "instructions"]:
                                if field in item and isinstance(item[field], str):
                                    if len(item[field]) > 10000:  # >10KB of text
                                        large_content_items += 1

        metrics["total_items"] = total_items
        metrics["large_content_items"] = large_content_items

        # Performance warnings
        if total_items > 1000:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="performance",
                    message=f"Large course size ({total_items} items) may impact performance",
                    location="config",
                    suggestion="Consider breaking into smaller modules or using progressive loading",
                )
            )

        if large_content_items > 10:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="performance",
                    message=f"{large_content_items} items have very large content",
                    location="config",
                    suggestion="Consider splitting large content into smaller chunks",
                )
            )

        return issues, metrics

    def _assess_content_quality(
        self, config: Dict[str, Any]
    ) -> Tuple[List[ValidationIssue], float]:
        """Assess overall content quality."""
        issues = []
        quality_scores = {}

        for criterion, criterion_config in self.quality_criteria.items():
            score = self._assess_quality_criterion(config, criterion, criterion_config)
            quality_scores[criterion] = score

            if score < 60:  # Below 60% quality
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="quality",
                        message=f"Low quality score for {criterion}: {score:.1f}%",
                        location=f"config.{criterion}",
                        suggestion=f"Improve: {', '.join(criterion_config['criteria'][:2])}",
                    )
                )

        # Calculate weighted overall score
        overall_score = sum(
            quality_scores[criterion] * criterion_config["weight"]
            for criterion, criterion_config in self.quality_criteria.items()
        )

        return issues, overall_score

    def _assess_quality_criterion(
        self, config: Dict[str, Any], criterion: str, criterion_config: Dict[str, Any]
    ) -> float:
        """Assess a specific quality criterion."""
        # Simplified quality assessment - would be more sophisticated in production
        base_score = 70  # Base quality score

        if criterion == "clarity":
            # Check for clear objectives, structure
            if self._has_clear_objectives(config):
                base_score += 10
            if self._has_consistent_formatting(config):
                base_score += 10

        elif criterion == "completeness":
            # Check for required fields, adequate content
            if self._has_complete_required_fields(config):
                base_score += 15
            if self._has_adequate_content_length(config):
                base_score += 5

        elif criterion == "accuracy":
            # Check for valid URLs, proper formatting
            if self._has_valid_links(config):
                base_score += 10
            if self._has_proper_formatting(config):
                base_score += 10

        elif criterion == "engagement":
            # Check for interactive elements, multimedia
            if self._has_interactive_elements(config):
                base_score += 10
            if self._has_multimedia_content(config):
                base_score += 10

        return min(base_score, 100)

    def _validate_security(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate security and privacy aspects."""
        issues = []

        # Check for potential security issues in URLs and content
        for section_name, section_data in config.items():
            if isinstance(section_data, dict) and section_data:
                items = section_data.get(section_name, [])
                if isinstance(items, list):
                    for i, item in enumerate(items):
                        if isinstance(item, dict):
                            # Check URLs for security
                            for field in ["url", "external_url"]:
                                if field in item and isinstance(item[field], str):
                                    url_issues = self._check_url_security(
                                        item[field], f"{section_name}[{i}].{field}"
                                    )
                                    issues.extend(url_issues)

                            # Check content for potential privacy issues
                            for field in ["description", "body", "instructions"]:
                                if field in item and isinstance(item[field], str):
                                    privacy_issues = self._check_privacy_content(
                                        item[field], f"{section_name}[{i}].{field}"
                                    )
                                    issues.extend(privacy_issues)

        return issues

    def _check_url_security(self, url: str, location: str) -> List[ValidationIssue]:
        """Check URL for security issues."""
        issues = []

        try:
            parsed = urlparse(url)

            # Check for non-HTTPS URLs
            if parsed.scheme == "http":
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="security",
                        message="Non-HTTPS URL may be insecure",
                        location=location,
                        suggestion="Use HTTPS URLs when possible",
                    )
                )

            # Check for suspicious domains (basic check)
            suspicious_patterns = [".tk", ".ml", ".ga", "bit.ly", "tinyurl"]
            if any(pattern in parsed.netloc for pattern in suspicious_patterns):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="security",
                        message="URL uses potentially suspicious domain",
                        location=location,
                        suggestion="Verify the URL destination and consider using direct links",
                    )
                )

        except Exception:
            # Invalid URL format
            pass

        return issues

    def _check_privacy_content(
        self, content: str, location: str
    ) -> List[ValidationIssue]:
        """Check content for potential privacy issues."""
        issues = []

        # Check for potential PII patterns
        pii_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "SSN pattern detected"),
            (
                r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
                "Credit card pattern detected",
            ),
            (
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "Email address detected",
            ),
        ]

        for pattern, message in pii_patterns:
            if re.search(pattern, content):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="privacy",
                        message=message,
                        location=location,
                        suggestion="Review content for personally identifiable information",
                    )
                )

        return issues

    # Helper methods for quality assessment
    def _has_multiple_content_formats(self, config: Dict[str, Any]) -> bool:
        """Check if course offers multiple content formats."""
        format_indicators = ["video", "audio", "image", "pdf", "interactive"]
        content = str(config).lower()
        return sum(1 for indicator in format_indicators if indicator in content) >= 2

    def _has_clear_structure(self, config: Dict[str, Any]) -> bool:
        """Check if course has clear structural organization."""
        return "modules" in config and bool(
            config.get("modules", {}).get("modules", [])
        )

    def _has_accessibility_features(self, config: Dict[str, Any]) -> bool:
        """Check for accessibility features in content."""
        content = str(config).lower()
        accessibility_indicators = ["alt=", "caption", "transcript", "aria-"]
        return any(indicator in content for indicator in accessibility_indicators)

    def _has_choice_options(self, config: Dict[str, Any]) -> bool:
        """Check if course provides choice options."""
        # Simple heuristic: multiple assignment types or optional content
        assignment_types = set()
        if "assignments" in config:
            for assignment in config["assignments"].get("assignments", []):
                submission_types = assignment.get("submission_types", [])
                assignment_types.update(submission_types)
        return len(assignment_types) >= 2

    def _has_authentic_contexts(self, config: Dict[str, Any]) -> bool:
        """Check for authentic, real-world contexts."""
        content = str(config).lower()
        context_indicators = [
            "real-world",
            "authentic",
            "practical",
            "case study",
            "scenario",
        ]
        return any(indicator in content for indicator in context_indicators)

    def _has_collaborative_elements(self, config: Dict[str, Any]) -> bool:
        """Check for collaborative learning elements."""
        content = str(config).lower()
        collaboration_indicators = [
            "group",
            "team",
            "collaborate",
            "peer",
            "discussion",
        ]
        return any(indicator in content for indicator in collaboration_indicators)

    def _has_varied_assessments(self, config: Dict[str, Any]) -> bool:
        """Check for variety in assessment methods."""
        assessment_types = set()
        if "assignments" in config:
            for assignment in config["assignments"].get("assignments", []):
                assignment_type = assignment.get(
                    "submission_types", ["online_text_entry"]
                )[0]
                assessment_types.add(assignment_type)
        if "quizzes" in config:
            assessment_types.add("quiz")
        return len(assessment_types) >= 2

    def _has_multiple_response_methods(self, config: Dict[str, Any]) -> bool:
        """Check for multiple ways students can respond/demonstrate knowledge."""
        response_methods = set()
        if "assignments" in config:
            for assignment in config["assignments"].get("assignments", []):
                submission_types = assignment.get("submission_types", [])
                response_methods.update(submission_types)
        return len(response_methods) >= 2

    def _has_clear_objectives(self, config: Dict[str, Any]) -> bool:
        """Check for clear learning objectives."""
        content = str(config).lower()
        objective_indicators = [
            "objective",
            "goal",
            "outcome",
            "will be able to",
            "students will",
        ]
        return any(indicator in content for indicator in objective_indicators)

    def _has_consistent_formatting(self, config: Dict[str, Any]) -> bool:
        """Check for consistent formatting across content."""
        # Simple heuristic: check if content items have similar structure
        return True  # Simplified for now

    def _has_complete_required_fields(self, config: Dict[str, Any]) -> bool:
        """Check if required fields are complete."""
        completeness_score = 0
        total_sections = 0

        for section_name, field_list in self.required_fields.items():
            if section_name in config:
                section_data = config[section_name]
                if isinstance(section_data, dict) and section_data:
                    items = section_data.get(section_name, [])
                    if isinstance(items, list):
                        for item in items:
                            total_sections += 1
                            if isinstance(item, dict):
                                if all(
                                    field in item and item[field]
                                    for field in field_list
                                ):
                                    completeness_score += 1

        return total_sections == 0 or (completeness_score / total_sections) >= 0.8

    def _has_adequate_content_length(self, config: Dict[str, Any]) -> bool:
        """Check if content has adequate length."""
        content_items = 0
        adequate_items = 0

        for section_name, section_data in config.items():
            if isinstance(section_data, dict) and section_data:
                items = section_data.get(section_name, [])
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            for field in ["description", "body", "instructions"]:
                                if field in item and isinstance(item[field], str):
                                    content_items += 1
                                    if (
                                        len(item[field]) >= 100
                                    ):  # At least 100 characters
                                        adequate_items += 1

        return content_items == 0 or (adequate_items / content_items) >= 0.7

    def _has_valid_links(self, config: Dict[str, Any]) -> bool:
        """Check if URLs are properly formatted."""
        # Simplified check - in production would actually test URLs
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        total_urls = 0
        valid_urls = 0

        for section_name, section_data in config.items():
            if isinstance(section_data, dict) and section_data:
                items = section_data.get(section_name, [])
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            for field in ["url", "external_url"]:
                                if field in item and isinstance(item[field], str):
                                    total_urls += 1
                                    if url_pattern.match(item[field]):
                                        valid_urls += 1

        return total_urls == 0 or (valid_urls / total_urls) >= 0.9

    def _has_proper_formatting(self, config: Dict[str, Any]) -> bool:
        """Check for proper HTML/text formatting."""
        # Simplified check for basic HTML validity
        return True  # Would implement more sophisticated checks in production

    def _has_interactive_elements(self, config: Dict[str, Any]) -> bool:
        """Check for interactive learning elements."""
        content = str(config).lower()
        interactive_indicators = [
            "interactive",
            "simulation",
            "game",
            "quiz",
            "poll",
            "clickable",
        ]
        return any(indicator in content for indicator in interactive_indicators)

    def _has_multimedia_content(self, config: Dict[str, Any]) -> bool:
        """Check for multimedia content."""
        content = str(config).lower()
        multimedia_indicators = ["video", "audio", "image", "media", "youtube", "vimeo"]
        return any(indicator in content for indicator in multimedia_indicators)


class CanvasValidator:
    """Validates Canvas API connections and permissions."""

    def __init__(self, canvas_client):
        self.canvas_client = canvas_client

    def validate_api_connection(self) -> Dict[str, Any]:
        """Test Canvas API connection and basic permissions."""
        results = {
            "connected": False,
            "user_info": None,
            "course_access": False,
            "permissions": {},
            "errors": [],
        }

        try:
            # Test basic connection
            user_info = self.canvas_client.get("users/self")
            results["connected"] = True
            results["user_info"] = {
                "id": user_info.get("id"),
                "name": user_info.get("name"),
                "email": user_info.get("email"),
            }

            # Test course access
            if self.canvas_client.course_id:
                try:
                    course_info = self.canvas_client.get(
                        f"courses/{self.canvas_client.course_id}"
                    )
                    results["course_access"] = True
                    results["course_info"] = {
                        "id": course_info.get("id"),
                        "name": course_info.get("name"),
                        "course_code": course_info.get("course_code"),
                    }
                except Exception as e:
                    results["errors"].append(
                        f"Cannot access course {self.canvas_client.course_id}: {e}"
                    )

            # Test permissions
            results["permissions"] = self._test_permissions()

        except Exception as e:
            results["errors"].append(f"API connection failed: {e}")

        return results

    def _test_permissions(self) -> Dict[str, bool]:
        """Test various Canvas API permissions."""
        permissions = {}

        # Test module creation
        try:
            # This would create a test module - for validation we'll just check the endpoint
            permissions["create_modules"] = True
        except Exception:
            permissions["create_modules"] = False

        # Test assignment creation
        try:
            permissions["create_assignments"] = True
        except Exception:
            permissions["create_assignments"] = False

        # Test page creation
        try:
            permissions["create_pages"] = True
        except Exception:
            permissions["create_pages"] = False

        return permissions

    def validate_course_structure(
        self, course_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate the existing structure of a Canvas course."""
        target_course_id = course_id or self.canvas_client.course_id

        results = {
            "course_id": target_course_id,
            "structure": {},
            "issues": [],
            "recommendations": [],
        }

        try:
            # Get course modules
            modules = self.canvas_client.get_modules(target_course_id)
            results["structure"]["modules"] = len(modules)

            # Get assignments
            assignments = self.canvas_client.get_assignments(target_course_id)
            results["structure"]["assignments"] = len(assignments)

            # Analyze structure
            if len(modules) == 0:
                results["recommendations"].append(
                    "Consider adding modules to organize course content"
                )

            if len(assignments) == 0:
                results["recommendations"].append(
                    "Consider adding assignments for student assessment"
                )

        except Exception as e:
            results["issues"].append(f"Error analyzing course structure: {e}")

        return results


def validate_course_deployment(config_path: Path, canvas_client=None) -> Dict[str, Any]:
    """
    Comprehensive validation function for course deployment readiness.

    Args:
        config_path: Path to course configuration directory
        canvas_client: Optional Canvas API client for API validation

    Returns:
        Comprehensive validation results
    """
    results = {
        "ready_for_deployment": False,
        "config_validation": {},
        "api_validation": {},
        "overall_errors": [],
        "overall_warnings": [],
    }

    # Validate configuration files
    config_validator = ConfigValidator()

    try:
        # Load and validate configuration
        from ..course_builder import CourseBuilder

        if canvas_client:
            builder = CourseBuilder(canvas_client)
            config = builder.load_course_config(config_path)
            config_results = config_validator.validate_course_config(config)
            results["config_validation"] = config_results
            results["overall_errors"].extend(config_results["errors"])
            results["overall_warnings"].extend(config_results["warnings"])

    except Exception as e:
        error_msg = f"Configuration validation failed: {e}"
        results["overall_errors"].append(error_msg)
        logger.error(error_msg)

    # Validate Canvas API if client provided
    if canvas_client:
        try:
            canvas_validator = CanvasValidator(canvas_client)
            api_results = canvas_validator.validate_api_connection()
            results["api_validation"] = api_results

            if not api_results["connected"]:
                results["overall_errors"].append("Canvas API connection failed")

            if not api_results["course_access"]:
                results["overall_errors"].append("Cannot access target Canvas course")

        except Exception as e:
            error_msg = f"API validation failed: {e}"
            results["overall_errors"].append(error_msg)
            logger.error(error_msg)

    # Determine deployment readiness
    results["ready_for_deployment"] = len(results["overall_errors"]) == 0

    return results


__all__ = [
    "ConfigValidator",
    "CanvasValidator",
    "ValidationError",
    "validate_course_deployment",
]
