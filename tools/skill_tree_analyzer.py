#!/usr/bin/env python3
"""
MATH 231 Skill Tree Visualization Tool
Generates dependency graphs and analytics for the linear algebra skill tree
"""

import yaml
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, List, Set, Tuple
import argparse
from pathlib import Path

class SkillTreeAnalyzer:
    """Analyzes and visualizes the MATH 231 skill tree"""
    
    def __init__(self, config_path: str):
        """Initialize with skill tree configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.skills = {}
        self.graph = nx.DiGraph()
        self._parse_skills()
        self._build_graph()
    
    def _parse_skills(self):
        """Parse all skills from the configuration"""
        def parse_skill_group(group_data, parent_path=""):
            """Recursively parse skills from nested structure"""
            if isinstance(group_data, dict):
                for key, value in group_data.items():
                    if key == 'sub_skills' and isinstance(value, list):
                        for skill in value:
                            skill_id = skill.get('skill_id')
                            if skill_id:
                                self.skills[skill_id] = skill
                    elif isinstance(value, dict) and 'skill_id' in value:
                        skill_id = value['skill_id']
                        self.skills[skill_id] = value
                        # Also parse sub_skills if they exist
                        if 'sub_skills' in value and isinstance(value['sub_skills'], list):
                            for sub_skill in value['sub_skills']:
                                sub_skill_id = sub_skill.get('skill_id')
                                if sub_skill_id:
                                    self.skills[sub_skill_id] = sub_skill
                    elif isinstance(value, dict):
                        parse_skill_group(value, f"{parent_path}.{key}" if parent_path else key)
        
        # Parse foundational skills
        if 'foundational_skills' in self.config.get('math231_skill_tree', {}):
            parse_skill_group(self.config['math231_skill_tree']['foundational_skills'])
        
        # Parse core linear algebra skills
        if 'linear_algebra_core' in self.config.get('math231_skill_tree', {}):
            parse_skill_group(self.config['math231_skill_tree']['linear_algebra_core'])
        
        # Parse applications and advanced topics
        if 'applications_advanced' in self.config.get('math231_skill_tree', {}):
            parse_skill_group(self.config['math231_skill_tree']['applications_advanced'])
    
    def _build_graph(self):
        """Build NetworkX graph from skill dependencies"""
        # Add all skills as nodes
        for skill_id, skill_data in self.skills.items():
            self.graph.add_node(skill_id, **skill_data)
        
        # Add prerequisite edges
        for skill_id, skill_data in self.skills.items():
            prerequisites = skill_data.get('prerequisites', [])
            for prereq in prerequisites:
                if prereq in self.skills:
                    self.graph.add_edge(prereq, skill_id)
    
    def analyze_dependencies(self) -> Dict:
        """Analyze skill tree dependencies"""
        analysis = {
            'total_skills': len(self.skills),
            'total_edges': self.graph.number_of_edges(),
            'leaf_skills': [],
            'root_skills': [],
            'critical_path_length': 0,
            'skill_levels': {},
            'xp_distribution': {}
        }
        
        # Find leaf and root skills
        for skill_id in self.skills:
            in_degree = self.graph.in_degree(skill_id)
            out_degree = self.graph.out_degree(skill_id)
            
            if out_degree == 0:
                analysis['leaf_skills'].append(skill_id)
            if in_degree == 0:
                analysis['root_skills'].append(skill_id)
        
        # Calculate longest path (critical path)
        if nx.is_directed_acyclic_graph(self.graph):
            analysis['critical_path_length'] = nx.dag_longest_path_length(self.graph)
        
        # Group skills by level
        level_counts = {}
        xp_by_level = {}
        
        for skill_id, skill_data in self.skills.items():
            level = skill_data.get('level', 'unknown')
            xp = skill_data.get('xp_value', 0)
            
            level_counts[level] = level_counts.get(level, 0) + 1
            xp_by_level[level] = xp_by_level.get(level, 0) + xp
        
        analysis['skill_levels'] = level_counts
        analysis['xp_distribution'] = xp_by_level
        
        return analysis
    
    def generate_dependency_graph(self, output_path: str = None, layout: str = 'hierarchical'):
        """Generate a visual dependency graph"""
        plt.figure(figsize=(20, 16))
        
        # Choose layout
        if layout == 'hierarchical':
            # Use topological sort for hierarchical layout
            try:
                levels = {}
                for node in nx.topological_sort(self.graph):
                    if not list(self.graph.predecessors(node)):
                        levels[node] = 0
                    else:
                        levels[node] = max(levels[pred] for pred in self.graph.predecessors(node)) + 1
                
                # Position nodes by level
                pos = {}
                level_counts = {}
                for node, level in levels.items():
                    level_counts[level] = level_counts.get(level, 0) + 1
                    x = level_counts[level] - 1
                    y = -level  # Negative to have roots at top
                    pos[node] = (x, y)
                    
            except nx.NetworkXError:
                pos = nx.spring_layout(self.graph, k=3, iterations=50)
        else:
            pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Color nodes by level
        level_colors = {
            'foundational': '#e3f2fd',
            'core': '#bbdefb', 
            'advanced': '#90caf9',
            'expert': '#64b5f6'
        }
        
        node_colors = []
        for node in self.graph.nodes():
            level = self.skills[node].get('level', 'foundational')
            node_colors.append(level_colors.get(level, '#f5f5f5'))
        
        # Draw the graph
        nx.draw(self.graph, pos, 
                node_color=node_colors,
                node_size=300,
                with_labels=True,
                labels={node: node.replace('_', '\n') for node in self.graph.nodes()},
                font_size=6,
                font_weight='bold',
                arrows=True,
                arrowsize=10,
                edge_color='gray',
                alpha=0.8)
        
        plt.title("MATH 231 Linear Algebra Skill Tree Dependency Graph", 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Add legend
        legend_elements = [patches.Patch(facecolor=color, label=level.title()) 
                          for level, color in level_colors.items()]
        plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Dependency graph saved to {output_path}")
        else:
            plt.show()
    
    def generate_analytics_report(self, output_path: str = None):
        """Generate detailed analytics report"""
        analysis = self.analyze_dependencies()
        
        report = f"""
MATH 231 Linear Algebra Skill Tree Analytics Report
==================================================

## Overview
- Total Skills: {analysis['total_skills']}
- Total Prerequisites: {analysis['total_edges']}
- Critical Path Length: {analysis['critical_path_length']}

## Skill Distribution by Level
"""
        
        for level, count in analysis['skill_levels'].items():
            xp = analysis['xp_distribution'].get(level, 0)
            report += f"- {level.title()}: {count} skills ({xp} total XP)\n"
        
        report += f"\n## Root Skills (No Prerequisites)\n"
        for skill in analysis['root_skills']:
            skill_name = self.skills[skill].get('name', skill)
            report += f"- {skill}: {skill_name}\n"
        
        report += f"\n## Leaf Skills (No Dependents)\n"
        for skill in analysis['leaf_skills']:
            skill_name = self.skills[skill].get('name', skill)
            report += f"- {skill}: {skill_name}\n"
        
        # Find skills with most prerequisites
        prereq_counts = [(skill_id, len(self.skills[skill_id].get('prerequisites', []))) 
                        for skill_id in self.skills]
        prereq_counts.sort(key=lambda x: x[1], reverse=True)
        
        report += f"\n## Most Complex Skills (Most Prerequisites)\n"
        for skill_id, count in prereq_counts[:10]:
            skill_name = self.skills[skill_id].get('name', skill_id)
            report += f"- {skill_id}: {skill_name} ({count} prerequisites)\n"
        
        # Find skills with most dependents
        dependent_counts = [(skill_id, self.graph.out_degree(skill_id)) 
                           for skill_id in self.skills]
        dependent_counts.sort(key=lambda x: x[1], reverse=True)
        
        report += f"\n## Most Important Skills (Most Dependents)\n"
        for skill_id, count in dependent_counts[:10]:
            skill_name = self.skills[skill_id].get('name', skill_id)
            report += f"- {skill_id}: {skill_name} ({count} dependents)\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Analytics report saved to {output_path}")
        else:
            print(report)
    
    def find_learning_paths(self, start_skill: str, end_skill: str) -> List[List[str]]:
        """Find all possible learning paths between two skills"""
        try:
            paths = list(nx.all_simple_paths(self.graph, start_skill, end_skill))
            return paths
        except nx.NetworkXNoPath:
            return []
    
    def get_immediate_prerequisites(self, skill_id: str) -> List[str]:
        """Get direct prerequisites for a skill"""
        return list(self.graph.predecessors(skill_id))
    
    def get_all_prerequisites(self, skill_id: str) -> Set[str]:
        """Get all prerequisites (transitive closure) for a skill"""
        return set(nx.ancestors(self.graph, skill_id))
    
    def validate_skill_tree(self) -> Dict:
        """Validate the skill tree for common issues"""
        issues = {
            'missing_prerequisites': [],
            'circular_dependencies': [],
            'orphaned_skills': [],
            'invalid_references': []
        }
        
        # Check for circular dependencies
        if not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            issues['circular_dependencies'] = cycles
        
        # Check for missing prerequisite references
        for skill_id, skill_data in self.skills.items():
            prerequisites = skill_data.get('prerequisites', [])
            for prereq in prerequisites:
                if prereq not in self.skills:
                    issues['missing_prerequisites'].append((skill_id, prereq))
        
        # Check for orphaned skills (no path from roots)
        roots = [skill for skill in self.skills if self.graph.in_degree(skill) == 0]
        reachable = set()
        for root in roots:
            reachable.update(nx.descendants(self.graph, root))
            reachable.add(root)
        
        for skill_id in self.skills:
            if skill_id not in reachable:
                issues['orphaned_skills'].append(skill_id)
        
        return issues

def main():
    """Command line interface for skill tree analysis"""
    parser = argparse.ArgumentParser(description='Analyze MATH 231 skill tree')
    parser.add_argument('config', help='Path to skill tree YAML configuration')
    parser.add_argument('--graph', help='Generate dependency graph (PNG output path)')
    parser.add_argument('--report', help='Generate analytics report (TXT output path)')
    parser.add_argument('--layout', default='hierarchical', 
                       choices=['hierarchical', 'spring'],
                       help='Graph layout algorithm')
    parser.add_argument('--validate', action='store_true', 
                       help='Validate skill tree for issues')
    
    args = parser.parse_args()
    
    analyzer = SkillTreeAnalyzer(args.config)
    
    if args.validate:
        issues = analyzer.validate_skill_tree()
        if any(issues.values()):
            print("Skill tree validation issues found:")
            for issue_type, items in issues.items():
                if items:
                    print(f"\n{issue_type.replace('_', ' ').title()}:")
                    for item in items:
                        print(f"  - {item}")
        else:
            print("Skill tree validation passed - no issues found!")
    
    if args.graph:
        analyzer.generate_dependency_graph(args.graph, args.layout)
    
    if args.report:
        analyzer.generate_analytics_report(args.report)
    
    if not any([args.graph, args.report, args.validate]):
        # Default: show basic analytics
        analysis = analyzer.analyze_dependencies()
        print(f"MATH 231 Skill Tree Summary:")
        print(f"  Total skills: {analysis['total_skills']}")
        print(f"  Total prerequisites: {analysis['total_edges']}")
        print(f"  Critical path length: {analysis['critical_path_length']}")
        print(f"  Skill levels: {analysis['skill_levels']}")

if __name__ == "__main__":
    main()
