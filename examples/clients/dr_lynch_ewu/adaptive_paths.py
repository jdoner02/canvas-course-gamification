"""
Dr. Lynch MATH 231 - Multi-Major Learning Path Implementation
Adaptive skill tree generator for different academic tracks
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import yaml
import json

class LearningTrack(Enum):
    ENGINEERING = "engineering"
    COMPUTER_SCIENCE = "computer_science"
    MATHEMATICS = "mathematics"
    DATA_SCIENCE = "data_science"

@dataclass
class SkillNode:
    """Individual skill node in the learning tree"""
    skill_id: str
    name: str
    description: str
    prerequisites: List[str] = field(default_factory=list)
    xp_value: int = 100
    level: int = 1
    track_variations: Dict[str, str] = field(default_factory=dict)
    sub_skills: List[str] = field(default_factory=list)
    assessment_config: Dict[str, Any] = field(default_factory=dict)
    youtube_content: List[str] = field(default_factory=list)
    bonus_content: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class LearningPath:
    """Complete learning path for a specific academic track"""
    track: LearningTrack
    name: str
    description: str
    target_majors: List[str]
    skill_sequence: List[str]
    mastery_threshold: float = 0.75
    bonus_modules: List[str] = field(default_factory=list)
    assessment_weights: Dict[str, float] = field(default_factory=dict)

class DrLynchMath231PathGenerator:
    """
    Generates customized learning paths for Dr. Lynch's MATH 231 course
    based on student's declared major and learning preferences
    """
    
    def __init__(self, config_path: str = "prerequisite_tree.yml"):
        self.config = self._load_config(config_path)
        self.skill_nodes = self._build_skill_nodes()
        self.learning_paths = self._build_learning_paths()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load the prerequisite tree configuration"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Fallback configuration for demonstration
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration if file not found"""
        return {
            "dr_lynch_math231": {
                "learning_paths": {
                    "engineering": {
                        "name": "Engineering Applications Track",
                        "target_majors": ["Mechanical Engineering", "Electrical Engineering"],
                        "emphasis": ["computational_efficiency", "real_world_applications"]
                    },
                    "computer_science": {
                        "name": "Computer Science Track",
                        "target_majors": ["Computer Science", "Data Science"],
                        "emphasis": ["algorithmic_complexity", "programming_applications"]
                    },
                    "mathematics": {
                        "name": "Pure Mathematics Track",
                        "target_majors": ["Mathematics", "Applied Mathematics"],
                        "emphasis": ["proof_techniques", "abstract_reasoning"]
                    },
                    "data_science": {
                        "name": "Data Science Applications Track",
                        "target_majors": ["Data Science", "Statistics"],
                        "emphasis": ["statistical_applications", "machine_learning_foundations"]
                    }
                }
            }
        }
    
    def _build_skill_nodes(self) -> Dict[str, SkillNode]:
        """Build skill nodes from configuration"""
        nodes = {}
        
        # Extract skill tree from config
        skill_tree = self.config.get("dr_lynch_math231", {}).get("skill_tree", {})
        
        for level_key, level_data in skill_tree.items():
            if isinstance(level_data, dict):
                for skill_key, skill_data in level_data.items():
                    if isinstance(skill_data, dict) and "name" in skill_data:
                        node = SkillNode(
                            skill_id=skill_key,
                            name=skill_data.get("name", skill_key),
                            description=skill_data.get("description", ""),
                            prerequisites=skill_data.get("prerequisites", []),
                            xp_value=skill_data.get("xp_value", 100),
                            track_variations=skill_data.get("path_variations", {}),
                            sub_skills=skill_data.get("sub_skills", [])
                        )
                        nodes[skill_key] = node
        
        return nodes
    
    def _build_learning_paths(self) -> Dict[LearningTrack, LearningPath]:
        """Build learning paths for each track"""
        paths = {}
        
        path_configs = self.config.get("dr_lynch_math231", {}).get("learning_paths", {})
        
        for track_key, track_config in path_configs.items():
            try:
                track = LearningTrack(track_key)
                path = LearningPath(
                    track=track,
                    name=track_config.get("name", f"{track_key.title()} Track"),
                    description=track_config.get("description", ""),
                    target_majors=track_config.get("target_majors", []),
                    skill_sequence=self._generate_skill_sequence(track),
                    mastery_threshold=self._get_mastery_threshold(track)
                )
                paths[track] = path
            except ValueError:
                # Skip unknown track types
                continue
                
        return paths
    
    def _generate_skill_sequence(self, track: LearningTrack) -> List[str]:
        """Generate optimal skill sequence for a given track"""
        # This would implement a topological sort of the skill dependency graph
        # For now, return a basic sequence
        base_sequence = [
            "basic_algebra",
            "coordinate_geometry", 
            "vector_introduction",
            "vector_operations",
            "linear_equations",
            "matrix_basics",
            "matrix_algebra",
            "determinant_computation",
            "vector_space_theory",
            "linear_independence",
            "linear_transformations",
            "eigenvalue_theory",
            "rank_nullity",
            "real_world_applications"
        ]
        
        # Filter based on available skill nodes
        return [skill for skill in base_sequence if skill in self.skill_nodes]
    
    def _get_mastery_threshold(self, track: LearningTrack) -> float:
        """Get mastery threshold for specific track"""
        thresholds = {
            LearningTrack.ENGINEERING: 0.75,
            LearningTrack.COMPUTER_SCIENCE: 0.80,
            LearningTrack.MATHEMATICS: 0.85,
            LearningTrack.DATA_SCIENCE: 0.75
        }
        return thresholds.get(track, 0.75)
    
    def generate_adaptive_curriculum(self, 
                                   student_major: str, 
                                   student_preferences: Dict[str, Any] = None) -> LearningPath:
        """
        Generate an adaptive curriculum based on student's major and preferences
        """
        if student_preferences is None:
            student_preferences = {}
            
        # Determine best matching track
        track = self._match_student_to_track(student_major)
        
        # Get base learning path
        base_path = self.learning_paths.get(track)
        if not base_path:
            # Fallback to mathematics track
            track = LearningTrack.MATHEMATICS
            base_path = self.learning_paths[track]
        
        # Customize based on preferences
        customized_path = self._customize_path(base_path, student_preferences)
        
        return customized_path
    
    def _match_student_to_track(self, student_major: str) -> LearningTrack:
        """Match student's major to appropriate learning track"""
        major_lower = student_major.lower()
        
        # Engineering majors
        if any(eng in major_lower for eng in ["engineering", "mechanical", "electrical", "civil"]):
            return LearningTrack.ENGINEERING
            
        # Computer Science majors  
        if any(cs in major_lower for cs in ["computer science", "information technology", "software"]):
            return LearningTrack.COMPUTER_SCIENCE
            
        # Data Science majors
        if any(ds in major_lower for ds in ["data science", "statistics", "analytics", "economics"]):
            return LearningTrack.DATA_SCIENCE
            
        # Default to mathematics track
        return LearningTrack.MATHEMATICS
    
    def _customize_path(self, base_path: LearningPath, preferences: Dict[str, Any]) -> LearningPath:
        """Customize learning path based on student preferences"""
        # This could modify the path based on:
        # - Learning style preferences
        # - Time constraints
        # - Prior knowledge assessment
        # - Career goals
        
        # For now, return the base path
        return base_path
    
    def get_skill_content_for_track(self, skill_id: str, track: LearningTrack) -> Dict[str, Any]:
        """Get track-specific content for a skill"""
        skill_node = self.skill_nodes.get(skill_id)
        if not skill_node:
            return {}
            
        content = {
            "name": skill_node.name,
            "description": skill_node.description,
            "xp_value": skill_node.xp_value,
            "prerequisites": skill_node.prerequisites,
            "sub_skills": skill_node.sub_skills
        }
        
        # Add track-specific variation if available
        if track.value in skill_node.track_variations:
            content["track_description"] = skill_node.track_variations[track.value]
            
        return content
    
    def export_path_configuration(self, track: LearningTrack, output_file: str):
        """Export learning path configuration to JSON file"""
        path = self.learning_paths.get(track)
        if not path:
            raise ValueError(f"No path found for track: {track}")
            
        config = {
            "track": track.value,
            "name": path.name,
            "description": path.description,
            "target_majors": path.target_majors,
            "mastery_threshold": path.mastery_threshold,
            "skills": []
        }
        
        for skill_id in path.skill_sequence:
            skill_content = self.get_skill_content_for_track(skill_id, track)
            if skill_content:
                config["skills"].append(skill_content)
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)

# Example usage and testing
if __name__ == "__main__":
    # Initialize the path generator
    generator = DrLynchMath231PathGenerator()
    
    # Test different majors
    test_majors = [
        "Mechanical Engineering",
        "Computer Science", 
        "Mathematics",
        "Data Science",
        "Business Administration"  # Should default to mathematics
    ]
    
    print("🌳 Dr. Lynch MATH 231 - Adaptive Learning Path Generator")
    print("=" * 60)
    
    for major in test_majors:
        print(f"\n📚 Student Major: {major}")
        path = generator.generate_adaptive_curriculum(major)
        print(f"   Recommended Track: {path.track.value}")
        print(f"   Track Name: {path.name}")
        print(f"   Mastery Threshold: {path.mastery_threshold}")
        print(f"   Target Majors: {', '.join(path.target_majors)}")
        print(f"   Skills in Path: {len(path.skill_sequence)}")
    
    # Export sample configurations
    print(f"\n💾 Exporting sample track configurations...")
    for track in LearningTrack:
        if track in generator.learning_paths:
            filename = f"dr_lynch_{track.value}_path.json"
            generator.export_path_configuration(track, filename)
            print(f"   ✅ Exported: {filename}")
