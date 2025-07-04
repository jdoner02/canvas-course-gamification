# [HIGH BUG] CanvasAPIClient missing get_course method

**Priority:** P0
**Labels:** bug, high, canvas-api, integration

## 🐛 Bug Description
CourseBuilder expects `get_course` method on CanvasAPIClient but method doesn't exist.

## 🔄 Steps to Reproduce
1. Initialize CourseBuilder with CanvasAPIClient
2. Attempt course deployment
3. Error: `'CanvasAPIClient' object has no attribute 'get_course'`

## ✅ Expected Behavior
CanvasAPIClient should provide get_course method for course information retrieval.

## ❌ Actual Behavior
AttributeError prevents course initialization and deployment.

## 🎯 Impact Assessment
- [x] **High** - Affects user experience significantly

## 🏷️ Component Areas
- [x] Canvas API Integration
- [x] Course Builder

## 🔬 Technical Details
CourseBuilder.deploy_course() calls `self.canvas_client.get_course()` but method is missing.
Available methods: get_course_info, get_course_modules, get_course_assignments.

## 📋 Acceptance Criteria
- [ ] Add get_course method to CanvasAPIClient
- [ ] Method returns proper course object
- [ ] Update CourseBuilder to use correct API methods
- [ ] Add integration tests for course retrieval

## 🎓 Educational Impact
**High** - Prevents Canvas integration, core functionality for course management.

## ⏱️ Estimated Effort
**3-5 hours** - API method implementation and integration testing