#!/usr/bin/env python3
"""
Canvas Data Importer
Imports Canvas course data from JSON files and integrates with skill tree system
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging


@dataclass
class CanvasAssignment:
    """Canvas assignment data structure"""

    id: int
    name: str
    description: str
    points_possible: float
    due_at: Optional[str]
    submission_types: List[str]
    grading_type: str
    assignment_group_id: int
    course_id: int
    position: int
    created_at: str
    updated_at: str


@dataclass
class CanvasModule:
    """Canvas module data structure"""

    id: int
    name: str
    position: int
    prerequisite_module_ids: List[int]
    require_sequential_progress: bool
    workflow_state: str
    items: List[Dict]


@dataclass
class CanvasCourse:
    """Canvas course data structure"""

    id: int
    name: str
    course_code: str
    workflow_state: str
    account_id: int
    start_at: Optional[str]
    end_at: Optional[str]
    enrollments: List[Dict]
    assignments: List[CanvasAssignment]
    modules: List[CanvasModule]


class CanvasDataImporter:
    """Imports and processes Canvas course data"""

    def __init__(self, data_directory: str, skill_tree_path: str):
        """Initialize importer with data directory and skill tree"""
        self.data_dir = Path(data_directory)
        self.skill_tree_path = Path(skill_tree_path)

        # Load skill tree for mapping
        if self.skill_tree_path.exists():
            with open(self.skill_tree_path, "r") as f:
                self.skill_tree = yaml.safe_load(f)
        else:
            self.skill_tree = None

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.courses = {}
        self.imported_data = {}

    def import_course_data(self, course_id: str) -> Optional[CanvasCourse]:
        """Import course data from JSON file"""
        course_file = self.data_dir / f"course_{course_id}.json"

        if not course_file.exists():
            self.logger.error(f"Course file not found: {course_file}")
            return None

        try:
            with open(course_file, "r") as f:
                data = json.load(f)

            # Extract course metadata
            course_info = data.get("course", {})
            if not course_info:
                # If no course key, assume the whole object is course data
                course_info = {
                    "id": int(course_id),
                    "name": f"Course {course_id}",
                    "course_code": f"COURSE_{course_id}",
                    "workflow_state": "available",
                    "account_id": 1,
                }

            # Parse assignments
            assignments = []
            for assignment_data in data.get("assignments", []):
                assignment = CanvasAssignment(
                    id=assignment_data["id"],
                    name=assignment_data["name"],
                    description=assignment_data.get("description", ""),
                    points_possible=assignment_data.get("points_possible", 0.0),
                    due_at=assignment_data.get("due_at"),
                    submission_types=assignment_data.get("submission_types", []),
                    grading_type=assignment_data.get("grading_type", "points"),
                    assignment_group_id=assignment_data.get("assignment_group_id"),
                    course_id=assignment_data["course_id"],
                    position=assignment_data.get("position", 1),
                    created_at=assignment_data["created_at"],
                    updated_at=assignment_data["updated_at"],
                )
                assignments.append(assignment)

            # Parse modules (if available)
            modules = []
            for module_data in data.get("modules", []):
                module = CanvasModule(
                    id=module_data["id"],
                    name=module_data["name"],
                    position=module_data.get("position", 1),
                    prerequisite_module_ids=module_data.get(
                        "prerequisite_module_ids", []
                    ),
                    require_sequential_progress=module_data.get(
                        "require_sequential_progress", False
                    ),
                    workflow_state=module_data.get("workflow_state", "active"),
                    items=module_data.get("items", []),
                )
                modules.append(module)

            # Create course object
            course = CanvasCourse(
                id=course_info.get("id", int(course_id)),
                name=course_info.get("name", f"Course {course_id}"),
                course_code=course_info.get("course_code", f"COURSE_{course_id}"),
                workflow_state=course_info.get("workflow_state", "available"),
                account_id=course_info.get("account_id", 1),
                start_at=course_info.get("start_at"),
                end_at=course_info.get("end_at"),
                enrollments=data.get("enrollments", []),
                assignments=assignments,
                modules=modules,
            )

            self.courses[course_id] = course
            self.logger.info(f"Imported course {course_id}: {course.name}")
            self.logger.info(f"  - {len(assignments)} assignments")
            self.logger.info(f"  - {len(modules)} modules")

            return course

        except Exception as e:
            self.logger.error(f"Error importing course {course_id}: {e}")
            return None

    def import_all_courses(self) -> Dict[str, CanvasCourse]:
        """Import all course JSON files in the data directory"""
        course_files = list(self.data_dir.glob("course_*.json"))

        for course_file in course_files:
            # Extract course ID from filename
            course_id = course_file.stem.replace("course_", "")
            self.import_course_data(course_id)

        return self.courses

    def analyze_course_structure(self, course_id: str) -> Dict:
        """Analyze course structure and suggest skill tree mappings"""
        if course_id not in self.courses:
            return {}

        course = self.courses[course_id]
        analysis = {
            "course_info": {
                "id": course.id,
                "name": course.name,
                "code": course.course_code,
                "assignment_count": len(course.assignments),
                "module_count": len(course.modules),
            },
            "assignment_analysis": self._analyze_assignments(course.assignments),
            "module_analysis": self._analyze_modules(course.modules),
            "skill_mapping_suggestions": self._suggest_skill_mappings(course),
        }

        return analysis

    def _analyze_assignments(self, assignments: List[CanvasAssignment]) -> Dict:
        """Analyze assignment patterns"""
        if not assignments:
            return {"total": 0}

        # Group by type and characteristics
        by_type = {}
        by_points = {}
        total_points = 0

        for assignment in assignments:
            # Group by submission types
            sub_types = ", ".join(assignment.submission_types)
            by_type[sub_types] = by_type.get(sub_types, 0) + 1

            # Group by point values
            points = assignment.points_possible
            total_points += points
            if points not in by_points:
                by_points[points] = []
            by_points[points].append(assignment.name)

        return {
            "total": len(assignments),
            "total_points": total_points,
            "avg_points": total_points / len(assignments),
            "by_submission_type": by_type,
            "by_point_value": by_points,
            "sample_names": [a.name for a in assignments[:5]],
        }

    def _analyze_modules(self, modules: List[CanvasModule]) -> Dict:
        """Analyze module structure"""
        if not modules:
            return {"total": 0}

        sequential_count = sum(1 for m in modules if m.require_sequential_progress)
        prereq_count = sum(1 for m in modules if m.prerequisite_module_ids)

        return {
            "total": len(modules),
            "sequential_modules": sequential_count,
            "modules_with_prerequisites": prereq_count,
            "module_names": [m.name for m in modules],
        }

    def _suggest_skill_mappings(self, course: CanvasCourse) -> List[Dict]:
        """Suggest mappings between Canvas content and skill tree"""
        suggestions = []

        if not self.skill_tree:
            return suggestions

        # Look for patterns that match skill tree concepts
        for assignment in course.assignments:
            # Simple keyword matching for demonstration
            suggestions.extend(self._match_assignment_to_skills(assignment))

        for module in course.modules:
            suggestions.extend(self._match_module_to_skills(module))

        return suggestions

    def _match_assignment_to_skills(self, assignment: CanvasAssignment) -> List[Dict]:
        """Match assignment to potential skills"""
        suggestions = []
        name_lower = assignment.name.lower()

        # Look for mathematical concepts
        math_keywords = {
            "vector": ["vector_representation", "vector_addition_subtraction"],
            "matrix": ["matrix_notation", "matrix_multiplication"],
            "equation": ["linear_equations_1var", "system_representation"],
            "quiz": ["knowledge_check"],
            "exam": ["comprehensive_assessment"],
            "homework": ["practice_problems"],
        }

        for keyword, skills in math_keywords.items():
            if keyword in name_lower:
                for skill in skills:
                    suggestions.append(
                        {
                            "type": "assignment",
                            "canvas_id": assignment.id,
                            "canvas_name": assignment.name,
                            "suggested_skill": skill,
                            "confidence": 0.7,
                            "reason": f"Contains keyword '{keyword}'",
                        }
                    )

        return suggestions

    def _match_module_to_skills(self, module: CanvasModule) -> List[Dict]:
        """Match module to potential skill groups"""
        suggestions = []
        name_lower = module.name.lower()

        # Look for skill group patterns
        skill_groups = {
            "vector": "vector_geometry",
            "matrix": "matrix_algebra",
            "system": "linear_systems",
            "determinant": "determinants",
            "space": "vector_spaces",
            "transformation": "linear_transformations",
            "eigenvalue": "eigenvalues_eigenvectors",
        }

        for keyword, skill_group in skill_groups.items():
            if keyword in name_lower:
                suggestions.append(
                    {
                        "type": "module",
                        "canvas_id": module.id,
                        "canvas_name": module.name,
                        "suggested_skill_group": skill_group,
                        "confidence": 0.8,
                        "reason": f"Module name suggests '{skill_group}'",
                    }
                )

        return suggestions

    def export_analysis(self, course_id: str, output_path: str):
        """Export course analysis to YAML file"""
        analysis = self.analyze_course_structure(course_id)

        with open(output_path, "w") as f:
            yaml.dump(analysis, f, default_flow_style=False, indent=2)

        self.logger.info(f"Exported analysis for course {course_id} to {output_path}")

    def export_skill_mappings(self, course_id: str, output_path: str):
        """Export suggested skill mappings to implementation file"""
        analysis = self.analyze_course_structure(course_id)
        mappings = analysis.get("skill_mapping_suggestions", [])

        # Create implementation structure
        implementation = {
            "canvas_skill_mappings": {
                "course_id": course_id,
                "generated_at": datetime.now().isoformat(),
                "total_suggestions": len(mappings),
                "mappings": mappings,
            }
        }

        with open(output_path, "w") as f:
            yaml.dump(implementation, f, default_flow_style=False, indent=2)

        self.logger.info(f"Exported {len(mappings)} skill mappings to {output_path}")

    def generate_integration_report(self, output_dir: str):
        """Generate comprehensive integration report"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Summary report
        summary = {
            "integration_summary": {
                "generated_at": datetime.now().isoformat(),
                "courses_processed": len(self.courses),
                "total_assignments": sum(
                    len(c.assignments) for c in self.courses.values()
                ),
                "total_modules": sum(len(c.modules) for c in self.courses.values()),
                "courses": {},
            }
        }

        # Process each course
        for course_id, course in self.courses.items():
            analysis = self.analyze_course_structure(course_id)
            summary["integration_summary"]["courses"][course_id] = {
                "name": course.name,
                "code": course.code,
                "analysis": analysis,
            }

            # Export individual course analysis
            self.export_analysis(
                course_id, output_path / f"course_{course_id}_analysis.yml"
            )
            self.export_skill_mappings(
                course_id, output_path / f"course_{course_id}_mappings.yml"
            )

        # Export summary
        with open(output_path / "integration_summary.yml", "w") as f:
            yaml.dump(summary, f, default_flow_style=False, indent=2)

        self.logger.info(f"Generated integration report in {output_dir}")


def main():
    """Main function for command line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Import Canvas course data and map to skill tree"
    )
    parser.add_argument("data_dir", help="Directory containing Canvas JSON files")
    parser.add_argument(
        "--skill-tree",
        help="Path to skill tree YAML file",
        default="config/math231_skill_tree.yml",
    )
    parser.add_argument(
        "--output",
        help="Output directory for analysis",
        default="analytics/canvas_integration",
    )
    parser.add_argument("--course-id", help="Specific course ID to process")

    args = parser.parse_args()

    # Create importer
    importer = CanvasDataImporter(args.data_dir, args.skill_tree)

    # Import data
    if args.course_id:
        importer.import_course_data(args.course_id)
    else:
        importer.import_all_courses()

    # Generate reports
    importer.generate_integration_report(args.output)

    print(f"Canvas data import complete! Reports generated in {args.output}")


if __name__ == "__main__":
    main()
