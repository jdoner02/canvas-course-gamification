#!/usr/bin/env python3
"""
Canvas Course Preview Generator
==============================

Generates interactive HTML previews of gamified Canvas courses for stakeholder
review and validation before deployment. Creates self-contained demos that
showcase the full gamification experience.

Features:
- Interactive skill tree visualization
- Badge and XP system preview
- Module progression simulation
- Responsive design with accessibility features
- No Canvas API required - works with JSON data only

Usage:
    python -m src.preview_generator data/math231 output/preview.html

Author: Canvas Course Gamification Framework
Version: 1.0
"""

import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import base64

from .course_builder.data_loader import CourseDataLoader
from .gamification import SkillTree, SkillNode, Badge, SkillLevel

logger = logging.getLogger(__name__)


class PreviewGenerator:
    """
    Generates interactive HTML previews of gamified Canvas courses.

    This class creates comprehensive, self-contained HTML previews that demonstrate
    the full gamification experience including skill trees, badges, and progressive
    unlocking without requiring Canvas API access.
    """

    def __init__(self, data_path: str, output_path: str):
        """
        Initialize preview generator.

        Args:
            data_path: Path to course JSON data directory
            output_path: Output path for generated preview HTML
        """
        self.data_path = Path(data_path)
        self.output_path = Path(output_path)
        self.data_loader = CourseDataLoader(str(data_path))
        self.course_data = {}

        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
        if not template_dir.exists():
            template_dir.mkdir(parents=True, exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def load_course_data(self) -> None:
        """Load and validate course data."""
        logger.info(f"Loading course data from {self.data_path}")
        self.data_loader.load_all_data()

        # Validate data integrity
        validation_result = self.data_loader.validate_data()
        if not validation_result.is_valid:
            logger.warning(
                f"Data validation found {len(validation_result.errors)} errors"
            )
            for error in validation_result.errors[:5]:  # Show first 5 errors
                logger.warning(f"  - {error}")

        self.course_data = self.data_loader.data
        logger.info("Course data loaded successfully")

    def build_skill_tree(self) -> SkillTree:
        """Build skill tree from course modules and outcomes."""
        logger.info("Building skill tree from course data")

        # Create skill tree
        skill_tree = SkillTree(
            name="MATH 231 Linear Algebra Mastery Journey",
            description="Interactive skill progression through linear algebra concepts",
        )

        # Process modules to create skill nodes
        modules = self.course_data.get("modules", {}).get("modules", [])
        outcomes = self.course_data.get("outcomes", {}).get("outcomes", [])

        # Create skill nodes from outcomes
        for outcome in outcomes:
            if outcome.get("level") == "Meta-Badge":
                continue  # Skip meta-badge outcomes

            # Map level string to SkillLevel enum
            level_map = {
                "Recognition": SkillLevel.RECOGNITION,
                "Application": SkillLevel.APPLICATION,
                "Intuition": SkillLevel.INTUITION,
                "Synthesis": SkillLevel.SYNTHESIS,
                "Mastery": SkillLevel.MASTERY,
            }

            skill_level = level_map.get(outcome.get("level"), SkillLevel.APPLICATION)

            # Create skill node
            node = SkillNode(
                id=outcome["id"],
                name=outcome["name"],
                description=outcome["description"],
                level=skill_level,
                xp_required=skill_level.value * 50,  # Scale XP by level
                tags=[outcome.get("badge", "general")],
                learning_objectives=[outcome["description"]],
            )

            skill_tree.add_node(node)
            logger.debug(f"Added skill node: {node.name}")

        # Add badges
        badge_names = set()
        for outcome in outcomes:
            if "badge" in outcome and outcome["badge"] not in badge_names:
                badge = Badge(
                    id=outcome["badge"],
                    name=outcome["badge"].replace("_", " ").title(),
                    description=f"Mastery badge for {outcome['badge'].replace('_', ' ')}",
                    criteria=f"Complete all skills in {outcome['badge'].replace('_', ' ')}",
                    xp_value=100,
                )
                skill_tree.add_badge(badge)
                badge_names.add(outcome["badge"])

        logger.info(
            f"Built skill tree with {len(skill_tree.nodes)} nodes and {len(skill_tree.badges)} badges"
        )
        return skill_tree

    def generate_preview_data(self) -> Dict[str, Any]:
        """Generate comprehensive data structure for preview template."""
        skill_tree = self.build_skill_tree()

        # Simulate different student progress states
        progress_scenarios = {
            "beginner": {
                "name": "Beginning Student",
                "description": "Just starting the course",
                "progress": {"total_xp": 0, "completed_skills": []},
                "completion_percentage": 0.0,
            },
            "intermediate": {
                "name": "Intermediate Student",
                "description": "Halfway through the course",
                "progress": {
                    "total_xp": 400,
                    "completed_skills": ["vector_recognition", "vector_operations"],
                },
                "completion_percentage": 0.4,
            },
            "advanced": {
                "name": "Advanced Student",
                "description": "Nearly complete with course",
                "progress": {
                    "total_xp": 800,
                    "completed_skills": [
                        "vector_recognition",
                        "vector_operations",
                        "dot_product_computation",
                    ],
                },
                "completion_percentage": 0.8,
            },
        }

        # Build module progression data
        modules = self.course_data.get("modules", {}).get("modules", [])
        module_data = []

        for i, module in enumerate(modules):
            module_info = {
                "id": f"module_{i}",
                "name": module.get("name", f"Module {i}"),
                "description": module.get("overview", ""),
                "items": module.get("items", []),
                "unlock_requirements": module.get("unlock_requirements", []),
                "mastery_criteria": module.get("mastery_criteria", {}),
                "gamification": module.get("gamification", {}),
                "position": i + 1,
            }
            module_data.append(module_info)

        return {
            "course_title": "MATH 231: Linear Algebra - Gamified Experience Preview",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "skill_tree": {
                "name": skill_tree.name,
                "description": skill_tree.description,
                "nodes": [
                    self._serialize_skill_node(node)
                    for node in skill_tree.nodes.values()
                ],
                "badges": [
                    self._serialize_badge(badge) for badge in skill_tree.badges.values()
                ],
                "total_nodes": len(skill_tree.nodes),
                "total_badges": len(skill_tree.badges),
            },
            "modules": module_data,
            "progress_scenarios": progress_scenarios,
            "pages": self.course_data.get("pages", {}).get("pages", [])[
                :5
            ],  # Sample pages
            "assignments": self.course_data.get("assignments", {}).get(
                "assignments", []
            )[
                :5
            ],  # Sample assignments
            "statistics": {
                "total_modules": len(modules),
                "total_outcomes": len(
                    self.course_data.get("outcomes", {}).get("outcomes", [])
                ),
                "total_pages": len(self.course_data.get("pages", {}).get("pages", [])),
                "total_assignments": len(
                    self.course_data.get("assignments", {}).get("assignments", [])
                ),
                "total_quizzes": len(
                    self.course_data.get("quizzes", {}).get("quizzes", [])
                ),
            },
        }

    def _serialize_skill_node(self, node: SkillNode) -> Dict[str, Any]:
        """Serialize skill node for JSON/template usage."""
        return {
            "id": node.id,
            "name": node.name,
            "description": node.description,
            "level": node.level.name,
            "level_value": node.level.value,
            "xp_required": node.xp_required,
            "prerequisites": node.prerequisites,
            "tags": node.tags,
            "estimated_time": node.estimated_time_minutes,
            "learning_objectives": node.learning_objectives,
        }

    def _serialize_badge(self, badge: Badge) -> Dict[str, Any]:
        """Serialize badge for JSON/template usage."""
        return {
            "id": badge.id,
            "name": badge.name,
            "description": badge.description,
            "icon": badge.image_url or "🏆",
            "category": badge.category.value if badge.category else "achievement",
            "rarity": badge.rarity if badge.rarity else "common",
            "xp_value": badge.xp_value,
        }

    def create_html_template(self) -> None:
        """Create the HTML template file if it doesn't exist."""
        template_path = Path(__file__).parent / "templates" / "course_preview.html"

        if template_path.exists():
            return  # Template already exists

        template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ course_title }}</title>
    <style>
        /* Modern, accessible styling for course preview */
        :root {
            --primary-color: #2563eb;
            --secondary-color: #7c3aed;
            --success-color: #059669;
            --warning-color: #d97706;
            --danger-color: #dc2626;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 12px;
            box-shadow: var(--shadow);
        }
        
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
        }
        
        .skill-tree {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .skill-node {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .skill-node:hover {
            border-color: var(--primary-color);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
            transform: translateY(-2px);
        }
        
        .skill-level {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .level-1 { background: #fef3c7; color: #92400e; }
        .level-2 { background: #dbeafe; color: #1e40af; }
        .level-3 { background: #d1fae5; color: #065f46; }
        .level-4 { background: #e0e7ff; color: #5b21b6; }
        .level-5 { background: #fce7f3; color: #be185d; }
        
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: var(--success-color);
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            margin: 4px;
        }
        
        .progress-scenario {
            border-left: 4px solid var(--primary-color);
            margin-bottom: 20px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--border-color);
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--success-color), var(--primary-color));
            transition: width 0.3s ease;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            text-align: center;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 24px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1em;
            color: var(--text-secondary);
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active, .tab:hover {
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .module-item {
            padding: 16px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 12px;
            background: var(--card-bg);
        }
        
        .module-item h4 {
            color: var(--primary-color);
            margin-bottom: 8px;
        }
        
        .xp-badge {
            background: var(--warning-color);
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .skill-tree {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ course_title }}</h1>
        <p>Interactive Preview Generated on {{ generation_date }}</p>
        <p><em>Experience the gamified learning journey before Canvas deployment</em></p>
    </div>
    
    <div class="container">
        <!-- Course Statistics -->
        <div class="card">
            <h2>📊 Course Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ statistics.total_modules }}</div>
                    <div>Learning Modules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ skill_tree.total_nodes }}</div>
                    <div>Skill Nodes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ skill_tree.total_badges }}</div>
                    <div>Achievement Badges</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ statistics.total_assignments }}</div>
                    <div>Assignments</div>
                </div>
            </div>
        </div>
        
        <!-- Progress Scenarios -->
        <div class="card">
            <h2>🎯 Student Progress Scenarios</h2>
            <p>See how different students would experience the gamified course:</p>
            
            {% for scenario_key, scenario in progress_scenarios.items() %}
            <div class="progress-scenario card">
                <h3>{{ scenario.name }}</h3>
                <p>{{ scenario.description }}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (scenario.completion_percentage * 100)|int }}%"></div>
                </div>
                <p><strong>Progress:</strong> {{ (scenario.completion_percentage * 100)|int }}% complete 
                   | <strong>XP:</strong> {{ scenario.progress.total_xp }} points</p>
            </div>
            {% endfor %}
        </div>
        
        <!-- Tabbed Content -->
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="showTab('skill-tree')">🌳 Skill Tree</button>
                <button class="tab" onclick="showTab('badges')">🏆 Badges</button>
                <button class="tab" onclick="showTab('modules')">📚 Modules</button>
                <button class="tab" onclick="showTab('sample-content')">📄 Sample Content</button>
            </div>
            
            <!-- Skill Tree Tab -->
            <div id="skill-tree" class="tab-content active">
                <h3>Interactive Skill Tree</h3>
                <p>Students progress through interconnected skills, unlocking new concepts as they master prerequisites.</p>
                <div class="skill-tree">
                    {% for node in skill_tree.nodes %}
                    <div class="skill-node">
                        <span class="skill-level level-{{ node.level_value }}">{{ node.level }}</span>
                        <h4>{{ node.name }}</h4>
                        <p>{{ node.description }}</p>
                        {% if node.xp_required > 0 %}
                        <span class="xp-badge">{{ node.xp_required }} XP</span>
                        {% endif %}
                        {% if node.prerequisites %}
                        <p><small><strong>Prerequisites:</strong> {{ node.prerequisites|join(', ') }}</small></p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Badges Tab -->
            <div id="badges" class="tab-content">
                <h3>Achievement Badges</h3>
                <p>Students earn badges for mastering skills and demonstrating competencies.</p>
                <div style="margin-top: 20px;">
                    {% for badge in skill_tree.badges %}
                    <div class="badge">
                        <span>{{ badge.icon }}</span>
                        <span><strong>{{ badge.name }}</strong>: {{ badge.description }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Modules Tab -->
            <div id="modules" class="tab-content">
                <h3>Learning Modules</h3>
                <p>Course content organized into progressive modules with gamification elements.</p>
                {% for module in modules[:5] %}
                <div class="module-item">
                    <h4>{{ module.name }}</h4>
                    <p>{{ module.description }}</p>
                    {% if module.gamification.xp_value %}
                    <span class="xp-badge">{{ module.gamification.xp_value }} XP Reward</span>
                    {% endif %}
                    {% if module.gamification.theme %}
                    <p><em>Theme: {{ module.gamification.theme }}</em></p>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            
            <!-- Sample Content Tab -->
            <div id="sample-content" class="tab-content">
                <h3>Sample Course Pages</h3>
                <p>Preview of actual course content with gamification integration.</p>
                {% for page in pages %}
                <div class="module-item">
                    <h4>{{ page.title }}</h4>
                    <div>{{ page.body|safe|truncate(200) }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by Canvas Course Gamification Framework</p>
        <p>🎮 Transforming education through evidence-based gamification</p>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        // Add interactive hover effects
        document.querySelectorAll('.skill-node').forEach(node => {
            node.addEventListener('click', function() {
                alert('In the full Canvas experience, this would open detailed skill information and progress tracking!');
            });
        });
        
        // Animate progress bars on load
        window.addEventListener('load', function() {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 500);
            });
        });
    </script>
</body>
</html>"""

        template_path.parent.mkdir(parents=True, exist_ok=True)
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        logger.info(f"Created HTML template at {template_path}")

    def generate_preview(self) -> str:
        """Generate the complete HTML preview."""
        logger.info("Generating course preview")

        # Load course data
        self.load_course_data()

        # Create template if needed
        self.create_html_template()

        # Generate preview data
        preview_data = self.generate_preview_data()

        # Render template
        template = self.jinja_env.get_template("course_preview.html")
        html_content = template.render(**preview_data)

        # Write to output file
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"Preview generated successfully: {self.output_path}")
        logger.info(f"Open {self.output_path} in your browser to view the preview")

        return str(self.output_path)


def main():
    """Command-line interface for preview generator."""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m src.preview_generator <data_path> <output_path>")
        print(
            "Example: python -m src.preview_generator data/math231 output/math231_preview.html"
        )
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        generator = PreviewGenerator(data_path, output_path)
        preview_file = generator.generate_preview()
        print(f"\n✅ Preview generated successfully!")
        print(f"📁 Output: {preview_file}")
        print(f"🌐 Open in browser to view the gamified course preview")
    except Exception as e:
        logger.error(f"Failed to generate preview: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
