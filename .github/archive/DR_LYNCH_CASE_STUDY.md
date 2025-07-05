# Dr. Frank Lynch MATH 231 Customization Case Study

## 🎓 Client Profile: Dr. Frank Lynch, Eastern Washington University

**Course**: MATH 231 - Linear Algebra  
**Institution**: Eastern Washington University  
**Format**: Asynchronous Online Summer Course  
**Teaching Method**: Flipped Classroom with YouTube Video Content  
**YouTube Channel**: https://www.youtube.com/@ewulynch/playlists  
**Faculty Profile**: https://www.ewu.edu/experts/frank-lynch/

### Student Demographics
- **Computer Science Students** - Focus on algorithmic applications
- **Electrical Engineering Students** - Emphasis on signal processing and systems
- **Cyber Operations Students** - Applications in cryptography and security
- **Applied Mathematics Students** - Pure mathematical foundations
- **External Students** - Taking course for credit at other institutions

## 📋 Course Catalog Information

### MATH 231: Linear Algebra (4 credits)
**Prerequisites**: MATH 161 (Calculus I) or equivalent  
**Corequisites**: None  

**Course Description**: Introduction to linear algebra including systems of linear equations, matrices, determinants, vector spaces, linear transformations, eigenvalues and eigenvectors, and applications.

**Learning Outcomes**:
- Solve systems of linear equations using various methods
- Perform matrix operations and understand matrix properties
- Work with vector spaces and linear transformations
- Calculate and interpret eigenvalues and eigenvectors
- Apply linear algebra concepts to real-world problems

## 🎯 Client Requests and Requirements

### Phase 1: Initial Consultation Simulation

**Dr. Lynch's Initial Request** (Simulated):
> "I've been teaching MATH 231 for several years using a flipped classroom approach with my YouTube videos. This summer I have a very diverse group of students from different majors, and I'd like to make the course more engaging and accessible. I've heard about gamification in education and would like to explore how to customize this Canvas framework for my specific needs."

### Phase 2: Requirements Gathering

**Follow-up Questions and Responses**:

**Q**: What specific challenges are you facing with the current course structure?  
**A**: "Students from different majors struggle to see the relevance of linear algebra to their fields. CS students want to see algorithms, EE students need signal processing applications, and cyber students are interested in cryptographic applications."

**Q**: How do you currently use your YouTube content?  
**A**: "I have organized playlists for different topics. Students watch videos before class, but I notice accessibility issues - some students need transcripts, and international students benefit from slower playback and summaries."

**Q**: What would success look like for this customization?  
**A**: "Students would have personalized learning paths based on their major, better accessibility support, and increased engagement through game-like elements while maintaining rigorous mathematical standards."

## 🚀 Project Implementation Roadmap

### Sprint 1: Foundation and Framework (P0 Priority)

#### Issue 1: Core Customization Framework
```bash
python scripts/project-management/local_issue_manager.py \
  --title "FEATURE: Dr. Lynch MATH 231 EWU Customization Framework" \
  --type feature \
  --priority P0 \
  --component course-builder \
  --description "Create customizable framework for Dr. Lynch's MATH 231 Linear Algebra course at Eastern Washington University with multi-major learning paths" \
  --requirements "EWU branding integration, Multi-major pathways (CS/EE/Cyber/Math), YouTube video integration, Flipped classroom support, Accessibility compliance" \
  --acceptance-criteria "Configurable per instructor preferences, Multi-pathway learning support, YouTube playlist integration, WCAG 2.1 AA compliance, Mobile responsive design" \
  --educational-impact "Enables personalized learning paths for diverse student backgrounds while supporting Dr. Lynch's flipped classroom methodology and improving accessibility for all learners" \
  --estimated-effort "20-30 hours" \
  --auto-sync
```

**Rationale**: This establishes the foundational framework that all other customizations will build upon. P0 priority because nothing else can proceed without this foundation.

### Sprint 2: Major-Specific Pathways (P1 Priority)

#### Issue 2: Multi-Major Learning Paths
```bash
python scripts/project-management/local_issue_manager.py \
  --title "FEATURE: Multi-Major Learning Paths for Linear Algebra" \
  --type feature \
  --priority P1 \
  --component gamification \
  --description "Create specialized learning paths for CS, EE, Cyber Operations, and Applied Math students taking MATH 231, with field-specific applications and examples" \
  --requirements "Major-specific skill trees, Field-relevant applications, Customizable prerequisites, Progress tracking per pathway" \
  --acceptance-criteria "Separate skill trees for each major, Real-world applications integrated, Adaptive content delivery, Cross-major collaboration opportunities" \
  --educational-impact "Increases relevance and engagement by connecting linear algebra concepts to students' chosen fields of study" \
  --estimated-effort "15-20 hours" \
  --auto-sync
```

**Rationale**: Addresses the core problem of relevance for different majors. High priority because it directly impacts student engagement and learning outcomes.

### Sprint 3: Accessibility and Content Integration (P1 Priority)

#### Issue 3: YouTube Content Integration
```bash
python scripts/project-management/local_issue_manager.py \
  --title "TASK: YouTube Transcript Scraper for Dr. Lynch's Playlists" \
  --type task \
  --priority P1 \
  --component canvas-api \
  --description "Scrape transcripts from Dr. Lynch's YouTube playlists to create accessible summaries and interactive content for his flipped classroom approach" \
  --requirements "YouTube API integration, Transcript extraction, Accessibility formatting, UDL content generation" \
  --acceptance-criteria "Extracts video metadata and transcripts, Generates accessible summaries, Creates interactive study guides, Supports multiple learning modalities" \
  --educational-impact "Improves accessibility for hearing-impaired students and supports diverse learning preferences through multiple content formats" \
  --estimated-effort "8-12 hours" \
  --auto-sync
```

**Rationale**: Critical for accessibility compliance and UDL implementation. Leverages existing instructor content while making it more inclusive.

### Sprint 4: Institutional Integration (P2 Priority)

#### Issue 4: EWU Branding
```bash
python scripts/project-management/local_issue_manager.py \
  --title "TASK: EWU Branding and Institutional Integration" \
  --type task \
  --priority P2 \
  --component course-builder \
  --description "Integrate Eastern Washington University branding, colors, logos, and institutional resources into the course framework" \
  --requirements "EWU brand guidelines compliance, Logo integration, Color scheme adaptation, Campus resource links" \
  --acceptance-criteria "Official EWU branding applied, Consistent visual identity, Links to EWU resources, Compliance with university standards" \
  --educational-impact "Creates institutional connection and pride while maintaining professional appearance for university-level courses" \
  --estimated-effort "6-8 hours" \
  --auto-sync
```

**Rationale**: Important for institutional adoption and professional appearance, but lower priority than core functionality.

## 🔧 Technical Implementation Details

### GitHub Copilot Agent Workflow

For AI agents working on this project, follow this workflow:

1. **Initialize Context**:
   ```markdown
   @agent I'm working on Dr. Lynch's MATH 231 customization project.
   
   Context files:
   #file:.github/PROJECT_STATUS.md
   #file:.github/AI_AGENT_GUIDE.md
   #folder:examples/linear_algebra/
   #folder:scripts/project-management/
   
   Please analyze the current issues and suggest next steps for implementation.
   ```

2. **Create Issues Programmatically**:
   ```bash
   # Use the enhanced local issue manager
   python scripts/project-management/local_issue_manager.py --help
   ```

3. **Follow Quality Standards**:
   ```bash
   # Always run quality checks
   python scripts/project-management/workflow_manager.py --check
   
   # Commit with intelligent messaging
   python scripts/project-management/workflow_manager.py --commit --push
   ```

### YouTube API Integration Specifications

**Target Playlists** (from https://www.youtube.com/@ewulynch/playlists):
- Linear Algebra Fundamentals
- Matrix Operations
- Vector Spaces
- Eigenvalues and Eigenvectors
- Applications in Engineering

**Required Extractions**:
- Video titles and descriptions
- Automatic transcripts (when available)
- Timestamps for key concepts
- Playlist organization structure

**Accessibility Enhancements**:
- Generate closed captions
- Create text summaries
- Provide concept glossaries
- Multi-language support preparation

## 📊 Success Metrics and Evaluation

### Quantitative Metrics
- **Student Engagement**: Time spent in course, completion rates
- **Accessibility Compliance**: WCAG 2.1 AA audit results
- **Performance**: Page load times, API response times
- **Adoption**: Faculty usage rates, customization frequency

### Qualitative Metrics
- **Student Satisfaction**: Course evaluations, feedback surveys
- **Faculty Experience**: Ease of customization, support needs
- **Educational Effectiveness**: Learning outcome achievement
- **Accessibility Impact**: Student feedback on inclusive features

## 🎓 Educational Technology Best Practices Demonstrated

### Universal Design for Learning (UDL) Implementation
- **Multiple Means of Representation**: Video, text, interactive visualizations
- **Multiple Means of Engagement**: Gamification, major-specific content
- **Multiple Means of Action/Expression**: Various assessment formats

### WCAG 2.1 AA Compliance
- **Perceivable**: Alt text, captions, high contrast
- **Operable**: Keyboard navigation, no seizure triggers
- **Understandable**: Clear language, consistent navigation
- **Robust**: Compatible with assistive technologies

### Faculty Development Support
- **Documentation**: Comprehensive guides and tutorials
- **Training Materials**: Video walkthroughs, best practices
- **Community Support**: Discussion forums, peer mentoring

## 🔄 Project Management Workflow Demonstration

### Issue Creation and Tracking
```bash
# Check current project status
python scripts/project-management/local_issue_manager.py --status

# Create new issues as needed
python scripts/project-management/local_issue_manager.py --title "..." --type ... --priority ...

# Sync to GitHub for team collaboration
python scripts/project-management/local_issue_manager.py --sync

# Monitor progress
python scripts/project-management/github_integration.py --dashboard
```

### Quality Assurance Process
```bash
# Before starting work
python scripts/project-management/workflow_manager.py --status

# After making changes
python scripts/project-management/workflow_manager.py --check

# Commit and push
python scripts/project-management/workflow_manager.py --commit --push
```

## 📚 Open Source and Professional Publication

### Documentation for Publication
This case study demonstrates:
- **Systematic Approach**: Structured requirements gathering and implementation
- **Professional Standards**: Enterprise-grade project management
- **Educational Focus**: UDL and accessibility compliance
- **Scalability**: Replicable for other institutions and courses

### Replication Guidelines
1. **Fork the Repository**: Clone for your institution
2. **Follow the Workflow**: Use the project management system
3. **Customize Systematically**: Use the issue creation patterns
4. **Maintain Standards**: Follow the quality assurance process

### Community Contribution
- **Share Customizations**: Contribute back to the main repository
- **Document Lessons Learned**: Add to the community knowledge base
- **Mentor Other Faculty**: Support peer adoption

---

**Status**: ✅ **COMPREHENSIVE CASE STUDY COMPLETE**

This case study provides a complete template for faculty customization of the Canvas Course Gamification framework, demonstrating professional project management practices, educational technology best practices, and accessibility compliance while maintaining focus on student learning outcomes.

*Created: July 4, 2025*  
*Client: Dr. Frank Lynch, Eastern Washington University*  
*Course: MATH 231 Linear Algebra*
