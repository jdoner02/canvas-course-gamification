# Canvas Course Gamification Framework

A comprehensive Python framework for creating and deploying gamified courses to Canvas LMS with automated skill trees, XP systems, and mastery-based learning progressions.

## 🎯 Overview

This framework transforms traditional Canvas courses into engaging, game-like learning experiences through:

- **📈 Skill Tree Progression**: Visual learning paths with prerequisite-based unlocking
- **🏆 Achievement System**: Badges, XP points, and mastery criteria
- **🎮 Gamification Elements**: Level progression, unlockables, and visual feedback
- **🤖 Automated Deployment**: One-click course creation and updates via Canvas API
- **📊 Mastery-Based Learning**: Conditional content release based on student performance

## ✨ Features

### Core Gamification
- **Experience Points (XP)**: Dynamic point system integrated with assignments
- **Digital Badges**: Achievement rewards with visual representations
- **Skill Trees**: Interactive progression visualization
- **Mastery Paths**: Conditional content unlocking
- **Progress Tracking**: Real-time student advancement monitoring

### Technical Features
- **Canvas API Integration**: Full REST API automation
- **Modular Architecture**: Easily customizable course components
- **Idempotent Deployment**: Safe to run multiple times without duplication
- **CI/CD Pipeline**: GitHub Actions for automated deployment
- **Environment Management**: Secure credential handling

### Course Management
- **Structured Content**: JSON-based course definition
- **Validation System**: Pre-deployment checks and testing
- **Documentation**: Comprehensive guides for instructors and students
- **Customization**: Configurable themes, badges, and progression rules

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Canvas LMS account with API access
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/canvas-course-gamification.git
   cd canvas-course-gamification
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Canvas credentials**
   ```bash
   cp .env.example .env
   # Edit .env with your Canvas API credentials
   ```

4. **Deploy your course**
   ```bash
   python deploy.py
   ```

## 📁 Project Structure

```
canvas-course-gamification/
├── src/                    # Core framework code
│   ├── canvas_api/        # Canvas API integration
│   ├── gamification/      # Game mechanics implementation
│   ├── course_builder/    # Course structure management
│   └── validators/        # Content validation tools
├── content/               # Course content definitions
│   ├── assignments.json   # Assignment configurations
│   ├── modules.json       # Module structure and progression
│   ├── badges.json        # Achievement badge definitions
│   └── pages.json         # Course page content
├── config/                # Framework configuration
│   ├── course_settings.yml # Course metadata and settings
│   ├── gamification.yml   # Gamification rules and mechanics
│   └── api_config.yml     # Canvas API configuration
├── examples/              # Example course implementations
│   ├── linear_algebra/    # MATH 231 Linear Algebra course
│   ├── calculus/          # Example calculus course
│   └── templates/         # Course templates
├── docs/                  # Documentation
│   ├── instructor_guide.md # Instructor documentation
│   ├── api_reference.md   # API documentation
│   └── customization.md   # Customization guide
├── tests/                 # Test suite
├── scripts/              # Utility scripts
└── .github/workflows/    # CI/CD automation
```

## 🎮 Gamification Features

### Skill Tree System
- **Visual Progression**: Interactive tree showing learning paths
- **Prerequisites**: Unlock requirements based on mastery
- **Multiple Pathways**: Branching progression options
- **Level Indicators**: Clear advancement markers

### Achievement System
- **Dynamic Badges**: Earned through various accomplishments
- **XP Points**: Quantified learning progress
- **Mastery Criteria**: Clear objectives for advancement
- **Visual Feedback**: Engaging progress displays

### Adaptive Learning
- **Conditional Release**: Content unlocks based on performance
- **Personalized Paths**: Student-specific progression routes
- **Remediation Loops**: Automatic retry mechanisms
- **Advanced Challenges**: Optional enhanced content

## 📚 Example: Linear Algebra Course

The framework includes a complete Linear Algebra (MATH 231) course example featuring:

- **5 Skill Levels**: Foundation → Systems → Transformations → Eigenspace → Applications
- **13 Progressive Modules**: Structured learning sequence
- **39 Gamified Assignments**: XP-rewarded activities
- **78 Learning Outcomes**: Comprehensive skill mapping
- **15+ Achievement Badges**: Diverse accomplishment rewards

### Course Progression
1. **Foundation Level**: Basic operations and concepts
2. **Systems Level**: Linear equations and matrix basics
3. **Transformations Level**: Matrix operations and linear maps
4. **Eigenspace Level**: Advanced decompositions and theory
5. **Applications Level**: Real-world implementations

## 🛠️ Customization

### Creating Your Own Course

1. **Define course structure** in `content/modules.json`
2. **Create assignments** in `content/assignments.json`
3. **Design badge system** in `content/badges.json`
4. **Configure gamification** in `config/gamification.yml`
5. **Deploy to Canvas** with `python deploy.py`

### Badge Customization
- Custom badge images and criteria
- XP value configuration
- Unlock condition definitions
- Visual theme customization

### Progression Rules
- Mastery threshold settings
- Prerequisite relationship definitions
- Conditional release configurations
- Retry and remediation policies

## 🔧 Technical Details

### Canvas API Integration
- **Authentication**: OAuth2 and token-based auth
- **Rate Limiting**: Automatic throttling and retry logic
- **Error Handling**: Comprehensive error management
- **Validation**: Pre-deployment content verification

### Architecture
- **Modular Design**: Separable components for flexibility
- **Event-Driven**: Hook-based customization system
- **Data-Driven**: JSON configuration for easy modification
- **Version Control**: Git-friendly course versioning

### Deployment
- **Idempotent Operations**: Safe multiple deployments
- **Incremental Updates**: Only deploy changed content
- **Rollback Support**: Revert to previous versions
- **Testing Integration**: Automated validation pipeline

## 📖 Documentation

- **[Instructor Guide](docs/instructor_guide.md)**: Complete setup and usage documentation
- **[API Reference](docs/api_reference.md)**: Technical API documentation
- **[Customization Guide](docs/customization.md)**: Framework customization instructions
- **[Examples](examples/)**: Sample course implementations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Canvas LMS**: For providing the robust API foundation
- **Educational Technology Community**: For gamification research and best practices
- **Open Source Contributors**: For tools and libraries that make this possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/canvas-course-gamification/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/canvas-course-gamification/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/canvas-course-gamification/wiki)

---

**Transform your Canvas courses into engaging, game-like learning experiences!** 🎓✨
