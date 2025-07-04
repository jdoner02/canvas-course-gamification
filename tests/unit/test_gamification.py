"""
Unit tests for the gamification module.
"""

import pytest
from src.gamification import SkillLevel, SkillNode, Badge, SkillTree


class TestSkillLevel:
    """Test the SkillLevel enum."""
    
    def test_skill_level_values(self):
        """Test that skill levels have correct values."""
        assert SkillLevel.RECOGNITION.value == 1
        assert SkillLevel.APPLICATION.value == 2
        assert SkillLevel.INTUITION.value == 3
        assert SkillLevel.SYNTHESIS.value == 4
        assert SkillLevel.MASTERY.value == 5
    
    def test_skill_level_ordering(self):
        """Test that skill levels can be compared."""
        assert SkillLevel.RECOGNITION < SkillLevel.APPLICATION
        assert SkillLevel.APPLICATION < SkillLevel.INTUITION
        assert SkillLevel.MASTERY > SkillLevel.RECOGNITION


class TestBadge:
    """Test the Badge class."""
    
    def test_badge_creation(self):
        """Test basic badge creation."""
        badge = Badge(
            id="test_badge",
            name="Test Badge",
            description="A test badge",
            criteria="Complete a test",
            xp_value=50
        )
        
        assert badge.id == "test_badge"
        assert badge.name == "Test Badge"
        assert badge.xp_value == 50
    
    def test_badge_to_canvas_format(self):
        """Test conversion to Canvas format."""
        badge = Badge(
            id="canvas_badge",
            name="Canvas Badge",
            description="Badge for Canvas",
            criteria="Use Canvas API",
            xp_value=75,
            image_url="https://example.com/badge.png"
        )
        
        canvas_format = badge.to_canvas_format()
        
        assert canvas_format["id"] == "canvas_badge"
        assert canvas_format["name"] == "Canvas Badge"
        assert canvas_format["points_possible"] == 75
        assert canvas_format["image_url"] == "https://example.com/badge.png"
    
    def test_badge_with_optional_fields(self):
        """Test badge creation with optional fields."""
        badge = Badge(
            id="full_badge",
            name="Full Badge",
            description="Badge with all fields",
            criteria="Complete everything",
            xp_value=100,
            image_url="https://example.com/full.png",
            category="achievement",
            unlock_requirements=["prerequisite_1", "prerequisite_2"]
        )
        
        assert badge.category == "achievement"
        assert len(badge.unlock_requirements) == 2
        assert "prerequisite_1" in badge.unlock_requirements


class TestSkillNode:
    """Test the SkillNode class."""
    
    def test_skill_node_creation(self):
        """Test basic skill node creation."""
        node = SkillNode(
            id="test_node",
            name="Test Node",
            description="A test node",
            level=SkillLevel.APPLICATION,
            xp_required=100
        )
        
        assert node.id == "test_node"
        assert node.name == "Test Node"
        assert node.level == SkillLevel.APPLICATION
        assert node.xp_required == 100
        assert node.mastery_threshold == 0.8  # default value
    
    def test_skill_node_with_prerequisites(self):
        """Test skill node with prerequisites."""
        node = SkillNode(
            id="advanced_node",
            name="Advanced Node",
            description="Advanced concepts",
            level=SkillLevel.SYNTHESIS,
            xp_required=500,
            prerequisites=["basic_node", "intermediate_node"]
        )
        
        assert len(node.prerequisites) == 2
        assert "basic_node" in node.prerequisites
        assert "intermediate_node" in node.prerequisites
    
    def test_skill_node_unlock_with_sufficient_progress(self):
        """Test node unlocking with sufficient progress."""
        node = SkillNode(
            id="unlockable_node",
            name="Unlockable Node",
            description="Can be unlocked",
            level=SkillLevel.APPLICATION,
            xp_required=100,
            prerequisites=["basic_node"]
        )
        
        progress = {
            "total_xp": 150,
            "basic_node": {"completed": True}
        }
        
        assert node.is_unlocked(progress)
    
    def test_skill_node_unlock_with_insufficient_xp(self):
        """Test node not unlocking with insufficient XP."""
        node = SkillNode(
            id="locked_node",
            name="Locked Node",
            description="Cannot be unlocked yet",
            level=SkillLevel.APPLICATION,
            xp_required=200,
            prerequisites=["basic_node"]
        )
        
        progress = {
            "total_xp": 100,  # Insufficient XP
            "basic_node": {"completed": True}
        }
        
        assert not node.is_unlocked(progress)
    
    def test_skill_node_unlock_with_missing_prerequisites(self):
        """Test node not unlocking with missing prerequisites."""
        node = SkillNode(
            id="blocked_node",
            name="Blocked Node", 
            description="Blocked by prerequisites",
            level=SkillLevel.APPLICATION,
            xp_required=100,
            prerequisites=["missing_prerequisite"]
        )
        
        progress = {
            "total_xp": 200  # Sufficient XP but missing prerequisite
        }
        
        assert not node.is_unlocked(progress)
    
    def test_skill_node_unlock_with_quiz_requirement(self):
        """Test node unlocking with quiz score requirement."""
        node = SkillNode(
            id="quiz_gated_node",
            name="Quiz Gated Node",
            description="Requires quiz score",
            level=SkillLevel.APPLICATION,
            xp_required=100,
            unlock_requirements={
                "quiz_score": ["prerequisite_quiz", 0.8]
            }
        )
        
        # Test with sufficient quiz score
        progress = {
            "total_xp": 150,
            "quiz_scores": {
                "prerequisite_quiz": 0.9
            }
        }
        assert node.is_unlocked(progress)
        
        # Test with insufficient quiz score
        progress["quiz_scores"]["prerequisite_quiz"] = 0.7
        assert not node.is_unlocked(progress)


class TestSkillTree:
    """Test the SkillTree class."""
    
    def test_skill_tree_creation(self):
        """Test basic skill tree creation."""
        tree = SkillTree("Test Tree", "A test skill tree")
        
        assert tree.name == "Test Tree"
        assert tree.description == "A test skill tree"
        assert len(tree.nodes) == 0
        assert len(tree.badges) == 0
    
    def test_add_node_to_tree(self):
        """Test adding nodes to skill tree."""
        tree = SkillTree("Test Tree", "A test tree")
        
        node1 = SkillNode(
            id="node_1",
            name="First Node",
            description="The first node",
            level=SkillLevel.RECOGNITION,
            xp_required=0
        )
        
        node2 = SkillNode(
            id="node_2",
            name="Second Node", 
            description="The second node",
            level=SkillLevel.APPLICATION,
            xp_required=100
        )
        
        tree.add_node(node1)
        tree.add_node(node2)
        
        assert len(tree.nodes) == 2
        assert tree.get_node("node_1") == node1
        assert tree.get_node("node_2") == node2
    
    def test_add_badge_to_tree(self):
        """Test adding badges to skill tree."""
        tree = SkillTree("Test Tree", "A test tree")
        
        badge = Badge(
            id="tree_badge",
            name="Tree Badge",
            description="Badge for the tree",
            criteria="Complete the tree",
            xp_value=100
        )
        
        tree.add_badge(badge)
        
        assert len(tree.badges) == 1
        assert tree.get_badge("tree_badge") == badge
    
    def test_get_available_nodes(self):
        """Test getting available nodes based on progress.""" 
        tree = SkillTree("Progressive Tree", "A tree with progression")
        
        # Add nodes with progression
        basic_node = SkillNode(
            id="basic",
            name="Basic",
            description="Basic concepts",
            level=SkillLevel.RECOGNITION,
            xp_required=0
        )
        
        intermediate_node = SkillNode(
            id="intermediate",
            name="Intermediate",
            description="Intermediate concepts", 
            level=SkillLevel.APPLICATION,
            xp_required=100,
            prerequisites=["basic"]
        )
        
        advanced_node = SkillNode(
            id="advanced",
            name="Advanced",
            description="Advanced concepts",
            level=SkillLevel.SYNTHESIS,
            xp_required=300,
            prerequisites=["intermediate"]
        )
        
        tree.add_node(basic_node)
        tree.add_node(intermediate_node)
        tree.add_node(advanced_node)
        
        # Test with beginner progress
        beginner_progress = {"total_xp": 50}
        available = tree.get_available_nodes(beginner_progress)
        assert len(available) == 1
        assert available[0].id == "basic"
        
        # Test with intermediate progress
        intermediate_progress = {
            "total_xp": 150,
            "basic": {"completed": True}
        }
        available = tree.get_available_nodes(intermediate_progress)
        assert len(available) == 2
        node_ids = [node.id for node in available]
        assert "basic" in node_ids
        assert "intermediate" in node_ids
        
        # Test with advanced progress
        advanced_progress = {
            "total_xp": 400,
            "basic": {"completed": True},
            "intermediate": {"completed": True}
        }
        available = tree.get_available_nodes(advanced_progress)
        assert len(available) == 3
    
    def test_calculate_completion_percentage(self):
        """Test calculation of completion percentage."""
        tree = SkillTree("Completion Tree", "Tree for testing completion")
        
        # Add 3 nodes
        for i in range(3):
            node = SkillNode(
                id=f"node_{i}",
                name=f"Node {i}",
                description=f"Node number {i}",
                level=SkillLevel.APPLICATION,
                xp_required=i * 100
            )
            tree.add_node(node)
        
        # Test with no completion
        no_progress = {}
        completion = tree.calculate_completion_percentage(no_progress)
        assert completion == 0.0
        
        # Test with partial completion
        partial_progress = {
            "node_0": {"completed": True},
            "node_1": {"completed": True}
        }
        completion = tree.calculate_completion_percentage(partial_progress)
        assert completion == pytest.approx(0.667, rel=1e-2)
        
        # Test with full completion
        full_progress = {
            "node_0": {"completed": True},
            "node_1": {"completed": True},
            "node_2": {"completed": True}
        }
        completion = tree.calculate_completion_percentage(full_progress)
        assert completion == 1.0


class TestGamificationIntegration:
    """Test integration between gamification components."""
    
    def test_skill_tree_with_badges_and_progression(self, sample_skill_tree):
        """Test a complete skill tree with progression and badges."""
        tree = sample_skill_tree
        
        # Test initial state
        beginner_progress = {"total_xp": 0}
        available = tree.get_available_nodes(beginner_progress)
        assert len(available) == 1
        assert available[0].id == "basic_node"
        
        # Test progression
        intermediate_progress = {
            "total_xp": 150,
            "basic_node": {"completed": True}
        }
        available = tree.get_available_nodes(intermediate_progress)
        assert len(available) == 2
        
        # Test badge availability
        badges = tree.badges
        assert len(badges) == 1
        badge_list = list(badges.values())
        assert badge_list[0].id == "completion_badge"
    
    def test_xp_and_level_progression(self):
        """Test XP accumulation and level progression."""
        # This would test XP system if implemented
        # For now, test the concept with skill nodes
        
        nodes = []
        xp_levels = [0, 100, 300, 600, 1000]
        
        for i, xp in enumerate(xp_levels):
            node = SkillNode(
                id=f"level_{i}",
                name=f"Level {i}",
                description=f"Requires {xp} XP",
                level=list(SkillLevel)[i],
                xp_required=xp
            )
            nodes.append(node)
        
        # Test progression through levels
        progress_stages = [
            {"total_xp": 50},    # Can access level 0 only
            {"total_xp": 150},   # Can access levels 0-1
            {"total_xp": 400},   # Can access levels 0-2
            {"total_xp": 700},   # Can access levels 0-3
            {"total_xp": 1200},  # Can access all levels
        ]
        
        for stage_idx, progress in enumerate(progress_stages):
            accessible_count = 0
            for node in nodes:
                if node.is_unlocked(progress):
                    accessible_count += 1
            
            # Should be able to access stage_idx + 1 levels
            assert accessible_count == stage_idx + 1
