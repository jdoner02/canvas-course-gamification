"""
📊 LEARNING ANALYTICS ENGINE
Comprehensive analytics for student learning patterns and course effectiveness
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Union, Tuple, Any
import json
import statistics
from collections import defaultdict, Counter


class AnalyticsMetric(Enum):
    """Types of analytics metrics"""
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    LEARNING_VELOCITY = "learning_velocity"
    RETENTION = "retention"
    DIFFICULTY_PROGRESSION = "difficulty_progression"
    TIME_DISTRIBUTION = "time_distribution"
    SOCIAL_INTERACTION = "social_interaction"
    GAMIFICATION_EFFECTIVENESS = "gamification_effectiveness"


class TimeGranularity(Enum):
    """Time granularity for analytics"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SEMESTER = "semester"


@dataclass
class AnalyticsSnapshot:
    """A snapshot of analytics data at a point in time"""
    timestamp: datetime
    student_id: str
    metric_type: AnalyticsMetric
    value: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class LearningTrend:
    """Represents a learning trend over time"""
    metric: AnalyticsMetric
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0-1, how strong the trend is
    confidence: float  # 0-1, confidence in the trend
    data_points: List[Tuple[datetime, float]]
    insights: List[str] = field(default_factory=list)


@dataclass
class CourseAnalytics:
    """Analytics summary for an entire course"""
    course_id: str
    total_students: int
    active_students: int
    completion_rate: float
    average_engagement: float
    concept_mastery_rates: Dict[str, float]
    difficulty_distribution: Dict[str, int]
    peak_activity_hours: List[int]
    generated_date: datetime = field(default_factory=datetime.now)


@dataclass
class StudentInsight:
    """AI-generated insight about a student"""
    student_id: str
    insight_type: str
    title: str
    description: str
    actionable_recommendations: List[str]
    confidence_score: float
    priority: str  # "high", "medium", "low"
    metadata: Dict = field(default_factory=dict)


class LearningAnalyticsEngine:
    """
    📊 LEARNING ANALYTICS ENGINE
    
    Comprehensive analytics system for understanding learning patterns
    Features:
    - Real-time performance tracking
    - Predictive learning analytics
    - Course effectiveness measurement
    - Student risk identification
    - Engagement pattern analysis
    - Gamification ROI measurement
    - Automated insight generation
    """
    
    def __init__(self):
        self.analytics_data: List[AnalyticsSnapshot] = []
        self.student_sessions: Dict[str, List[Dict]] = {}
        self.course_data: Dict[str, Dict] = {}
        self.insights_cache: Dict[str, List[StudentInsight]] = {}
        self.trend_cache: Dict[str, List[LearningTrend]] = {}
        
    def record_analytics_event(self, student_id: str, event_type: str, 
                              event_data: Dict, timestamp: datetime = None):
        """Record an analytics event"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Store raw event data
        if student_id not in self.student_sessions:
            self.student_sessions[student_id] = []
        
        event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": event_data
        }
        self.student_sessions[student_id].append(event)
        
        # Generate analytics snapshots from the event
        self._process_event_for_analytics(student_id, event)
        
        # Keep session data manageable (last 1000 events per student)
        if len(self.student_sessions[student_id]) > 1000:
            self.student_sessions[student_id] = self.student_sessions[student_id][-1000:]
    
    def _process_event_for_analytics(self, student_id: str, event: Dict):
        """Process an event to generate analytics snapshots"""
        timestamp = event["timestamp"]
        event_type = event["event_type"]
        data = event["data"]
        
        # Generate different analytics metrics based on event type
        if event_type == "problem_completed":
            # Engagement metric
            engagement_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.ENGAGEMENT,
                value=1.0,  # Simple engagement count
                metadata={"event_type": event_type, "difficulty": data.get("difficulty")}
            )
            self.analytics_data.append(engagement_snapshot)
            
            # Performance metric
            success = data.get("success", False)
            performance_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.PERFORMANCE,
                value=1.0 if success else 0.0,
                metadata={"concept": data.get("concept"), "difficulty": data.get("difficulty")}
            )
            self.analytics_data.append(performance_snapshot)
            
            # Learning velocity (problems per hour)
            recent_events = self._get_recent_events(student_id, hours=1)
            problem_events = [e for e in recent_events if e["event_type"] == "problem_completed"]
            velocity = len(problem_events)  # problems per hour
            
            velocity_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.LEARNING_VELOCITY,
                value=velocity,
                metadata={"window_hours": 1}
            )
            self.analytics_data.append(velocity_snapshot)
        
        elif event_type == "session_start":
            # Time distribution tracking
            hour = timestamp.hour
            time_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.TIME_DISTRIBUTION,
                value=hour,
                metadata={"session_type": data.get("session_type")}
            )
            self.analytics_data.append(time_snapshot)
        
        elif event_type == "social_interaction":
            # Social interaction tracking
            interaction_type = data.get("interaction_type", "unknown")
            social_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.SOCIAL_INTERACTION,
                value=1.0,
                metadata={"interaction_type": interaction_type, "target": data.get("target_student")}
            )
            self.analytics_data.append(social_snapshot)
        
        elif event_type == "gamification_reward":
            # Gamification effectiveness tracking
            reward_type = data.get("reward_type", "unknown")
            points = data.get("points", 0)
            gamification_snapshot = AnalyticsSnapshot(
                timestamp=timestamp,
                student_id=student_id,
                metric_type=AnalyticsMetric.GAMIFICATION_EFFECTIVENESS,
                value=points,
                metadata={"reward_type": reward_type, "trigger": data.get("trigger")}
            )
            self.analytics_data.append(gamification_snapshot)
    
    def _get_recent_events(self, student_id: str, hours: int = 24) -> List[Dict]:
        """Get recent events for a student"""
        if student_id not in self.student_sessions:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [event for event in self.student_sessions[student_id]
                if event["timestamp"] >= cutoff_time]
    
    def calculate_engagement_score(self, student_id: str, days: int = 7) -> float:
        """Calculate overall engagement score for a student"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Get engagement snapshots for the time period
        engagement_snapshots = [
            snapshot for snapshot in self.analytics_data
            if (snapshot.student_id == student_id and
                snapshot.metric_type == AnalyticsMetric.ENGAGEMENT and
                snapshot.timestamp >= cutoff_time)
        ]
        
        if not engagement_snapshots:
            return 0.0
        
        # Calculate engagement metrics
        total_activities = len(engagement_snapshots)
        unique_days = len(set(s.timestamp.date() for s in engagement_snapshots))
        
        # Engagement score based on consistency and volume
        consistency_score = unique_days / days  # How many days were active
        volume_score = min(1.0, total_activities / (days * 5))  # Normalized activity volume
        
        return (consistency_score * 0.6 + volume_score * 0.4)
    
    def calculate_performance_trend(self, student_id: str, concept: str = None, 
                                  days: int = 30) -> LearningTrend:
        """Calculate performance trend for a student"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Get performance snapshots
        performance_snapshots = [
            snapshot for snapshot in self.analytics_data
            if (snapshot.student_id == student_id and
                snapshot.metric_type == AnalyticsMetric.PERFORMANCE and
                snapshot.timestamp >= cutoff_time and
                (concept is None or snapshot.metadata.get("concept") == concept))
        ]
        
        if len(performance_snapshots) < 5:
            return LearningTrend(
                metric=AnalyticsMetric.PERFORMANCE,
                trend_direction="insufficient_data",
                trend_strength=0.0,
                confidence=0.0,
                data_points=[],
                insights=["Not enough data to determine performance trend"]
            )
        
        # Group by day and calculate daily performance
        daily_performance = defaultdict(list)
        for snapshot in performance_snapshots:
            day = snapshot.timestamp.date()
            daily_performance[day].append(snapshot.value)
        
        # Calculate daily averages
        daily_averages = []
        for day in sorted(daily_performance.keys()):
            avg_performance = statistics.mean(daily_performance[day])
            daily_averages.append((datetime.combine(day, datetime.min.time()), avg_performance))
        
        # Calculate trend
        if len(daily_averages) < 3:
            return LearningTrend(
                metric=AnalyticsMetric.PERFORMANCE,
                trend_direction="insufficient_data",
                trend_strength=0.0,
                confidence=0.0,
                data_points=daily_averages,
                insights=["Not enough data points for trend analysis"]
            )
        
        # Simple linear trend calculation
        x_values = list(range(len(daily_averages)))
        y_values = [point[1] for point in daily_averages]
        
        # Calculate correlation coefficient as trend strength
        if len(set(y_values)) == 1:
            trend_direction = "stable"
            trend_strength = 0.0
        else:
            correlation = self._calculate_correlation(x_values, y_values)
            trend_strength = abs(correlation)
            
            if correlation > 0.1:
                trend_direction = "increasing"
            elif correlation < -0.1:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"
        
        # Generate insights
        insights = self._generate_performance_insights(trend_direction, trend_strength, y_values)
        
        return LearningTrend(
            metric=AnalyticsMetric.PERFORMANCE,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            confidence=min(1.0, len(daily_averages) / 10),  # More data = higher confidence
            data_points=daily_averages,
            insights=insights
        )
    
    def _calculate_correlation(self, x_values: List[float], y_values: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        sum_y2 = sum(y * y for y in y_values)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _generate_performance_insights(self, trend_direction: str, trend_strength: float, 
                                     performance_values: List[float]) -> List[str]:
        """Generate insights about performance trends"""
        insights = []
        
        if trend_direction == "increasing":
            if trend_strength > 0.7:
                insights.append("Strong improvement trend - student is mastering concepts well")
            elif trend_strength > 0.4:
                insights.append("Moderate improvement - learning is progressing steadily")
            else:
                insights.append("Slight improvement trend detected")
        
        elif trend_direction == "decreasing":
            if trend_strength > 0.7:
                insights.append("⚠️ Strong decline in performance - immediate intervention needed")
            elif trend_strength > 0.4:
                insights.append("⚠️ Moderate performance decline - check for understanding gaps")
            else:
                insights.append("Slight performance decline - monitor closely")
        
        else:  # stable
            avg_performance = statistics.mean(performance_values)
            if avg_performance > 0.8:
                insights.append("Consistently high performance - ready for advanced challenges")
            elif avg_performance > 0.6:
                insights.append("Stable moderate performance - good foundation")
            else:
                insights.append("Stable but low performance - needs additional support")
        
        # Add specific recommendations
        recent_performance = statistics.mean(performance_values[-3:]) if len(performance_values) >= 3 else performance_values[-1]
        
        if recent_performance < 0.5:
            insights.append("Recommend: Review fundamental concepts and provide easier practice problems")
        elif recent_performance > 0.9:
            insights.append("Recommend: Introduce more challenging problems to maintain engagement")
        
        return insights
    
    def generate_course_analytics(self, course_id: str) -> CourseAnalytics:
        """Generate comprehensive course analytics"""
        # Get all students in the course (simplified - would come from enrollment data)
        all_students = set(snapshot.student_id for snapshot in self.analytics_data)
        
        # Calculate active students (engaged in last 7 days)
        cutoff_time = datetime.now() - timedelta(days=7)
        active_students = set(
            snapshot.student_id for snapshot in self.analytics_data
            if snapshot.timestamp >= cutoff_time
        )
        
        # Calculate engagement statistics
        engagement_scores = []
        for student_id in all_students:
            score = self.calculate_engagement_score(student_id)
            engagement_scores.append(score)
        
        avg_engagement = statistics.mean(engagement_scores) if engagement_scores else 0.0
        
        # Calculate concept mastery rates
        concept_mastery = defaultdict(list)
        for snapshot in self.analytics_data:
            if snapshot.metric_type == AnalyticsMetric.PERFORMANCE:
                concept = snapshot.metadata.get("concept", "unknown")
                concept_mastery[concept].append(snapshot.value)
        
        mastery_rates = {}
        for concept, scores in concept_mastery.items():
            mastery_rates[concept] = statistics.mean(scores)
        
        # Calculate difficulty distribution
        difficulty_dist = Counter()
        for snapshot in self.analytics_data:
            difficulty = snapshot.metadata.get("difficulty")
            if difficulty:
                difficulty_dist[difficulty] += 1
        
        # Calculate peak activity hours
        time_snapshots = [s for s in self.analytics_data if s.metric_type == AnalyticsMetric.TIME_DISTRIBUTION]
        hour_counts = Counter(int(s.value) for s in time_snapshots)
        peak_hours = [hour for hour, count in hour_counts.most_common(3)]
        
        return CourseAnalytics(
            course_id=course_id,
            total_students=len(all_students),
            active_students=len(active_students),
            completion_rate=len(active_students) / len(all_students) if all_students else 0.0,
            average_engagement=avg_engagement,
            concept_mastery_rates=mastery_rates,
            difficulty_distribution=dict(difficulty_dist),
            peak_activity_hours=peak_hours
        )
    
    def identify_at_risk_students(self, threshold: float = 0.3) -> List[Dict]:
        """Identify students at risk of falling behind"""
        at_risk_students = []
        
        all_students = set(snapshot.student_id for snapshot in self.analytics_data)
        
        for student_id in all_students:
            # Calculate risk factors
            engagement_score = self.calculate_engagement_score(student_id)
            performance_trend = self.calculate_performance_trend(student_id)
            
            # Recent performance
            recent_events = self._get_recent_events(student_id, hours=72)
            recent_performance_events = [e for e in recent_events 
                                       if e["event_type"] == "problem_completed"]
            
            if recent_performance_events:
                recent_success_rate = sum(1 for e in recent_performance_events 
                                        if e["data"].get("success", False)) / len(recent_performance_events)
            else:
                recent_success_rate = 0.0
            
            # Calculate overall risk score
            risk_factors = {
                "low_engagement": 1.0 - engagement_score,
                "declining_performance": 1.0 if performance_trend.trend_direction == "decreasing" else 0.0,
                "low_recent_performance": 1.0 - recent_success_rate,
                "no_recent_activity": 1.0 if not recent_events else 0.0
            }
            
            risk_score = sum(risk_factors.values()) / len(risk_factors)
            
            if risk_score >= threshold:
                at_risk_students.append({
                    "student_id": student_id,
                    "risk_score": risk_score,
                    "risk_factors": risk_factors,
                    "recommendations": self._generate_intervention_recommendations(risk_factors)
                })
        
        # Sort by risk score (highest first)
        at_risk_students.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return at_risk_students
    
    def _generate_intervention_recommendations(self, risk_factors: Dict[str, float]) -> List[str]:
        """Generate intervention recommendations based on risk factors"""
        recommendations = []
        
        if risk_factors["no_recent_activity"] > 0.5:
            recommendations.append("Send engagement reminder and check if student needs technical support")
        
        if risk_factors["low_engagement"] > 0.5:
            recommendations.append("Implement gamification boosters and peer connection opportunities")
        
        if risk_factors["declining_performance"] > 0.5:
            recommendations.append("Review recent concepts and provide additional scaffolding")
        
        if risk_factors["low_recent_performance"] > 0.5:
            recommendations.append("Reduce difficulty level temporarily and provide concept review")
        
        if not recommendations:
            recommendations.append("Monitor progress and provide encouragement")
        
        return recommendations
    
    def export_analytics_data(self, student_id: str = None, days: int = 30) -> Dict:
        """Export analytics data for external analysis"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Filter data
        filtered_data = [
            snapshot for snapshot in self.analytics_data
            if (snapshot.timestamp >= cutoff_time and
                (student_id is None or snapshot.student_id == student_id))
        ]
        
        # Convert to exportable format
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "student_id": student_id,
            "time_range_days": days,
            "total_snapshots": len(filtered_data),
            "snapshots": [
                {
                    "timestamp": snapshot.timestamp.isoformat(),
                    "student_id": snapshot.student_id,
                    "metric_type": snapshot.metric_type.value,
                    "value": snapshot.value,
                    "metadata": snapshot.metadata
                }
                for snapshot in filtered_data
            ]
        }
        
        return export_data


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Learning Analytics Engine...")
    
    # Initialize engine
    analytics = LearningAnalyticsEngine()
    
    # Simulate student activities
    students = ["alice_123", "bob_456", "charlie_789"]
    
    # Generate sample data
    import random
    from datetime import datetime, timedelta
    
    base_time = datetime.now() - timedelta(days=14)
    
    for day in range(14):
        for student in students:
            # Simulate daily activities
            current_time = base_time + timedelta(days=day)
            
            # Session start
            analytics.record_analytics_event(
                student, "session_start", 
                {"session_type": "problem_solving"}, 
                current_time
            )
            
            # Problem solving activities
            for i in range(random.randint(3, 8)):
                success_rate = 0.8 if student == "alice_123" else 0.6 if student == "bob_456" else 0.4
                success = random.random() < success_rate
                
                analytics.record_analytics_event(
                    student, "problem_completed",
                    {
                        "success": success,
                        "concept": random.choice(["vectors", "matrices", "transformations"]),
                        "difficulty": random.choice(["easy", "medium", "hard"]),
                        "time_spent": random.randint(60, 300)
                    },
                    current_time + timedelta(minutes=i*10)
                )
            
            # Gamification rewards
            if random.random() < 0.7:
                analytics.record_analytics_event(
                    student, "gamification_reward",
                    {
                        "reward_type": "coins",
                        "points": random.randint(10, 50),
                        "trigger": "problem_solved"
                    },
                    current_time + timedelta(minutes=30)
                )
    
    # Test analytics functions
    print("\n📊 Analytics Results:")
    
    # Engagement scores
    for student in students:
        engagement = analytics.calculate_engagement_score(student)
        print(f"{student} engagement: {engagement:.2f}")
    
    # Performance trends
    for student in students:
        trend = analytics.calculate_performance_trend(student)
        print(f"\n{student} performance trend:")
        print(f"  Direction: {trend.trend_direction}")
        print(f"  Strength: {trend.trend_strength:.2f}")
        print(f"  Insights: {trend.insights}")
    
    # Course analytics
    course_analytics = analytics.generate_course_analytics("MATH_231")
    print(f"\n📚 Course Analytics:")
    print(f"Total students: {course_analytics.total_students}")
    print(f"Active students: {course_analytics.active_students}")
    print(f"Average engagement: {course_analytics.average_engagement:.2f}")
    print(f"Peak activity hours: {course_analytics.peak_activity_hours}")
    
    # At-risk students
    at_risk = analytics.identify_at_risk_students()
    print(f"\n⚠️ At-risk students: {len(at_risk)}")
    for student_data in at_risk:
        print(f"  {student_data['student_id']}: risk score {student_data['risk_score']:.2f}")
        print(f"    Recommendations: {student_data['recommendations']}")
    
    print("\n✅ Learning Analytics Engine Tests Complete!")
