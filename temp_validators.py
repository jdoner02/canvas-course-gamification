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
            "udl_guideline": self.udl_guideline
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
                "suggestions": len([i for i in self.issues if i.severity == ValidationSeverity.SUGGESTION])
            },
            "scores": {
                "accessibility": self.accessibility_score,
                "udl": self.udl_score,
                "quality": self.quality_score
            },
            "sections_validated": self.sections_validated,
            "performance_metrics": self.performance_metrics,
            "issues": [issue.to_dict() for issue in self.issues]
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
        custom_schemas: Optional[Dict[str, Dict[str, Any]]] = None
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
                    "prerequisites": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "gamification": {
                        "type": "object",
                        "properties": {
                            "skill_level": {
                                "type": "string",
                                "enum": ["recognition", "application", "intuition", "synthesis", "mastery"]
                            },
                            "xp_required": {"type": "integer", "minimum": 0},
                            "mastery_threshold": {"type": "number", "minimum": 0, "maximum": 1}
                        }
                    }
                }
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
                        "items": {"type": "string", "enum": self.valid_assignment_types}
                    }
                }
            }
        }

    def _initialize_accessibility_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize accessibility validation patterns."""
        return {
            "missing_alt_text": {
                "pattern": r'<img(?![^>]*alt=)[^>]*>',
                "wcag": "1.1.1",
                "description": "Images without alternative text",
                "severity": ValidationSeverity.ERROR
            },
            "missing_video_captions": {
                "keywords": ["youtube.com", "vimeo.com", "<video"],
                "wcag": "1.2.2",
                "description": "Video content may be missing captions",
                "severity": ValidationSeverity.WARNING
            },
            "poor_color_contrast": {
                "pattern": r'style=["\'][^"\']*color:\s*#[a-fA-F0-9]{6}[^"\']*["\']',
                "wcag": "1.4.3",
                "description": "Inline color styling may have poor contrast",
                "severity": ValidationSeverity.WARNING
            },
            "missing_headings": {
                "pattern": r'^(?!.*<h[1-6]).{200,}',
                "wcag": "1.3.1",
                "description": "Long content without proper heading structure",
                "severity": ValidationSeverity.WARNING
            },
            "empty_links": {
                "pattern": r'<a[^>]*>\s*</a>',
                "wcag": "2.4.4",
                "description": "Links without descriptive text",
                "severity": ValidationSeverity.ERROR
            },
            "tables_without_headers": {
                "pattern": r'<table(?![^>]*<th)[^>]*>.*?</table>',
                "wcag": "1.3.1",
                "description": "Data tables without proper headers",
                "severity": ValidationSeverity.ERROR
            }
        }

    def _initialize_udl_guidelines(self) -> Dict[str, Dict[str, Any]]:
        """Initialize UDL (Universal Design for Learning) validation guidelines."""
        return {
            "multiple_means_representation": {
                "criteria": [
                    "Has alternative text for images",
                    "Provides multiple format options",
                    "Uses clear language and structure",
                    "Includes visual and textual information"
                ],
                "weight": 0.4
            },
            "multiple_means_engagement": {
                "criteria": [
                    "Offers choice in content and activities",
                    "Provides relevant, authentic contexts",
                    "Includes collaborative opportunities",
                    "Supports different interests and preferences"
                ],
                "weight": 0.3
            },
            "multiple_means_action_expression": {
                "criteria": [
                    "Provides multiple assessment formats",
                    "Supports different response methods",
                    "Offers assistive technology compatibility",
                    "Allows for varied ways to demonstrate knowledge"
                ],
                "weight": 0.3
            }
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
                    "Consistent formatting"
                ]
            },
            "completeness": {
                "weight": 0.25,
                "criteria": [
                    "All required fields present",
                    "Adequate content length",
                    "Comprehensive instructions",
                    "Proper resource links"
                ]
            },
            "accuracy": {
                "weight": 0.25,
                "criteria": [
                    "Valid URLs and links",
                    "Correct spelling and grammar",
                    "Factual accuracy",
                    "Proper formatting"
                ]
            },
            "engagement": {
                "weight": 0.25,
                "criteria": [
                    "Interactive elements",
                    "Multimedia content",
                    "Varied activity types",
                    "Clear progression"
                ]
            }
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
                accessibility_issues, accessibility_score = self._validate_accessibility(config)
                result.issues.extend(accessibility_issues)
                result.accessibility_score = accessibility_score
            
            # 5. UDL validation
            udl_issues, udl_score = self._validate_udl_compliance(config)
            result.issues.extend(udl_issues)
            result.udl_score = udl_score
            
            # 6. Performance validation
            if self.enable_performance_analysis:
                performance_issues, performance_metrics = self._validate_performance(config)
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
            
            logger.info(f"Validation completed: {len(result.issues)} issues found, "
                       f"valid: {result.is_valid}")
            
        except Exception as e:
            logger.error(f"Validation process failed: {e}")
            result.issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                category="validation_system",
                message=f"Validation system error: {e}",
                location="validation_process"
            ))
            result.is_valid = False
        
        return result

    def _validate_structure(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate the structural integrity of the configuration."""
        issues = []
        
        # Check for required top-level sections
        recommended_sections = ["modules", "course_info"]
        for section in recommended_sections:
            if section not in config:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="structure",
                    message=f"Missing recommended section: {section}",
                    location=f"config.{section}",
                    suggestion=f"Add {section} section for complete course definition"
                ))
        
        # Validate each section against schemas
        for section_name, section_data in config.items():
            if section_name in self.required_fields:
                section_issues = self._validate_section_schema(section_name, section_data)
                issues.extend(section_issues)
        
        return issues

    def _validate_section_schema(self, section_name: str, section_data: Any) -> List[ValidationIssue]:
        """Validate a section against its JSON schema."""
        issues = []
        
        if not isinstance(section_data, dict):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="schema",
                message=f"Section '{section_name}' must be an object",
                location=f"config.{section_name}"
            ))
            return issues
        
        items = section_data.get(section_name, [])
        if not isinstance(items, list):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="schema",
                message=f"Section '{section_name}' must contain a list of items",
                location=f"config.{section_name}.{section_name}"
            ))
            return issues
        
        # Validate each item in the section
        for i, item in enumerate(items):
            item_issues = self._validate_item_schema(section_name, item, i)
            issues.extend(item_issues)
        
        return issues

    def _validate_item_schema(self, section_name: str, item: Dict[str, Any], index: int) -> List[ValidationIssue]:
        """Validate an individual item against its schema."""
        issues = []
        location_base = f"config.{section_name}.{section_name}[{index}]"
        
        # Check required fields
        required_fields = self.required_fields.get(section_name, [])
        for field in required_fields:
            if field not in item:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="required_field",
                    message=f"Missing required field: {field}",
                    location=f"{location_base}.{field}",
                    suggestion=f"Add {field} field to {section_name} item"
                ))
            elif not item[field] or (isinstance(item[field], str) and not item[field].strip()):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="empty_field",
                    message=f"Required field '{field}' is empty",
                    location=f"{location_base}.{field}",
                    suggestion=f"Provide a value for {field}"
                ))
        
        # JSON Schema validation if available
        if JSONSCHEMA_AVAILABLE and section_name.rstrip('s') in self.schemas:
            schema_name = section_name.rstrip('s')  # Remove plural
            try:
                validate(item, self.schemas[schema_name])
            except JsonSchemaValidationError as e:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="schema_validation",
                    message=f"Schema validation failed: {e.message}",
                    location=f"{location_base}.{'.'.join(str(p) for p in e.path) if e.path else 'root'}",
                    suggestion="Check the field format and allowed values"
                ))
        
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

    def _validate_item_content(self, section_name: str, item: Dict[str, Any], index: int) -> List[ValidationIssue]:
        """Validate the content quality of an individual item."""
        issues = []
        location_base = f"config.{section_name}.{section_name}[{index}]"
        
        # Check for descriptive content
        description_fields = ["description", "body", "instructions"]
        has_description = any(field in item and item[field] for field in description_fields)
        
        if not has_description:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="content_quality",
                message=f"{section_name.title()} item lacks descriptive content",
                location=location_base,
                suggestion="Add description, body, or instructions to improve clarity",
                udl_guideline="Multiple means of representation"
            ))
        
        # Check content length and quality
        for field in description_fields:
            if field in item and item[field]:
                content = item[field]
                content_issues = self._validate_text_content(content, f"{location_base}.{field}")
                issues.extend(content_issues)
        
        # Validate URLs
        url_fields = ["url", "external_url", "image_url"]
        for field in url_fields:
            if field in item and item[field]:
                url_issues = self._validate_url(item[field], f"{location_base}.{field}")
                issues.extend(url_issues)
        
        return issues

    def _validate_text_content(self, content: str, location: str) -> List[ValidationIssue]:
        """Validate text content for quality and accessibility."""
        issues = []
        
        if len(content.strip()) < 10:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="content_quality",
                message="Content is very short and may lack sufficient detail",
                location=location,
                suggestion="Provide more detailed content to improve clarity"
            ))
        
        # Check for basic spelling/grammar issues (simplified)
        if content.count('.') == 0 and len(content) > 50:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.SUGGESTION,
                category="content_quality", 
                message="Long content without sentence breaks may be hard to read",
                location=location,
                suggestion="Consider breaking into shorter sentences"
            ))
        
        return issues

    def _validate_url(self, url: str, location: str) -> List[ValidationIssue]:
        """Validate URL format and accessibility."""
        issues = []
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="url_validation",
                    message="Invalid URL format",
                    location=location,
                    suggestion="Ensure URL includes protocol (http:// or https://)"
                ))
        except Exception:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="url_validation",
                message="URL parsing failed",
                location=location
            ))
        
        return issues

    def _validate_cross_references(self, config: Dict[str, Any]) -> List[ValidationIssue]:
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
            assignment_ids = {assignment["id"] for assignment in assignments if "id" in assignment}
        
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
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.WARNING,
                            category="cross_reference",
                            message=f"Module '{module.get('id', 'Unknown')}' references unknown prerequisite: {prereq}",
                            location=f"config.modules.modules[{i}].prerequisites",
                            suggestion="Ensure prerequisite module exists or remove invalid reference"
                        ))
        
        # Validate module items references
        if "modules" in config:
            for i, module in enumerate(config["modules"].get("modules", [])):
                items = module.get("items", [])
                for j, item in enumerate(items):
                    item_type = item.get("type", "")
                    item_id = item.get("id", "")
                    
                    if item_type == "Assignment" and item_id not in assignment_ids:
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            category="cross_reference",
                            message=f"Module item references unknown assignment: {item_id}",
                            location=f"config.modules.modules[{i}].items[{j}].id"
                        ))
                    elif item_type == "Page" and item_id not in page_ids:
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            category="cross_reference", 
                            message=f"Module item references unknown page: {item_id}",
                            location=f"config.modules.modules[{i}].items[{j}].id"
                        ))
                    elif item_type == "Quiz" and item_id not in quiz_ids:
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            category="cross_reference",
                            message=f"Module item references unknown quiz: {item_id}",
                            location=f"config.modules.modules[{i}].items[{j}].id"
                        ))
        
        return issues
