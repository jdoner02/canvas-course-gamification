# 🧮 Linear Algebra Course Builder

A production-ready system for creating, customizing, and managing linear algebra courses with Canvas integration, public student enrollment, and automated workflows.

![Linear Algebra Course Builder](https://img.shields.io/badge/Course%20Builder-Linear%20Algebra-blue)
![Canvas Integration](https://img.shields.io/badge/Canvas-Integrated-green)
![Public Enrollment](https://img.shields.io/badge/Enrollment-Public-orange)
![Auto Cleanup](https://img.shields.io/badge/Cleanup-Automated-red)

## 🌟 Features

### 🎯 For Faculty
- **Custom Course Creation**: Detailed form-based course customization
- **Canvas Integration**: Automatic course deployment to Canvas Free for Teachers
- **Export Functionality**: Download Canvas cartridges (.imscc) for import anywhere
- **Course Management**: Full dashboard for monitoring and administration
- **Automated Workflows**: GitHub Actions for hands-off course creation

### 👥 For Students
- **Public Enrollment**: Join courses with simple codes or direct links
- **Instant Access**: Immediate enrollment with email confirmation
- **Canvas Integration**: Seamless redirect to Canvas course materials
- **No Account Required**: Simple name and email enrollment process

### 🔧 For Administrators
- **System Dashboard**: Monitor all courses, enrollments, and system health
- **Automated Cleanup**: 7-day auto-deletion of test courses
- **Bulk Operations**: Export, manage, and cleanup multiple courses
- **Analytics**: Track usage, performance, and engagement metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Canvas Free for Teachers account
- Canvas API token

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd canvas-course-gamification

# Run the setup script (installs dependencies, sets up environment)
./run.sh setup
```

### 2. Configuration

Update your `.env` file with Canvas API credentials:

```env
CANVAS_API_URL=https://canvas.instructure.com
CANVAS_API_TOKEN='your-canvas-api-token-here'
FLASK_SECRET_KEY='auto-generated-secret-key'
```

### 3. Start the Server

```bash
# Production mode
./run.sh start

# Development mode (with debug logging)
./run.sh dev
```

### 4. Access the Application

Open your browser to `http://localhost:5000`

## 📋 Complete User Guide

### For Faculty: Creating a Course

1. **Access the System**
   - Go to the course builder homepage
   - Click "Create Course"

2. **Fill Out Course Details**
   - **Faculty Information**: Name, email, institution
   - **Course Configuration**: Name, code, semester
   - **Customization**: Focus area, difficulty level, features
   - **Structure**: Duration, weekly hours, special topics
   - **Deployment**: Visibility and enrollment options

3. **Submit and Deploy**
   - Course is created instantly in Canvas
   - Receive join code and management links
   - Get email with complete access information

4. **Manage Your Course**
   - Access the course dashboard
   - Share join code with students
   - Export course for backup/migration
   - Monitor enrollment and analytics

### For Students: Joining a Course

1. **Get Join Information**
   - Receive join code from instructor
   - Or use direct enrollment link

2. **Join the Course**
   - Go to the student portal
   - Enter join code or follow direct link
   - Provide name and email

3. **Access Course Materials**
   - Instant enrollment confirmation
   - Automatic redirect to Canvas
   - Email with login instructions

### For Administrators: System Management

1. **Monitor System Health**
   - Access admin dashboard
   - View course statistics
   - Check system status

2. **Manage Courses**
   - View all active courses
   - Export multiple courses
   - Run cleanup operations

3. **Maintenance Operations**
   - Schedule automated cleanup
   - Monitor performance metrics
   - View system logs

## 🔄 Automated Workflows

### GitHub Actions Integration

Faculty can create courses through GitHub workflows:

1. **Access Repository**
   - Go to Actions tab
   - Select "Linear Algebra Course Automation"

2. **Fill Workflow Form**
   - Same customization options as web interface
   - Automated deployment and notification

3. **Receive Results**
   - Email notification with course details
   - Automatic course export generation
   - Complete access information

### Course Lifecycle Management

1. **Creation**: Instant deployment to Canvas
2. **Active Phase**: Student enrollment and content access
3. **Export**: Automated backup generation
4. **Cleanup**: 7-day auto-deletion with warnings

## 🎨 Course Customization Options

### Focus Areas
- **Mathematical Foundations**: Theory and proofs emphasis
- **Real-World Applications**: Practical problem solving
- **Computational Methods**: Programming and algorithms
- **Theoretical Emphasis**: Advanced mathematical concepts
- **Engineering Applications**: Applied mathematics for engineers
- **Data Science Applications**: Machine learning and analytics focus

### Difficulty Levels
- **Introductory**: Basic concepts, minimal prerequisites
- **Intermediate**: Standard undergraduate level
- **Advanced**: Upper-level undergraduate
- **Graduate**: Research-oriented approach

### Learning Features
- **Gamified Learning**: Skill trees and achievement systems
- **Interactive Visualizations**: Dynamic mathematical content
- **Real-World Applications**: Practical problem examples
- **Mathematical Proofs**: Formal mathematical reasoning
- **Collaborative Learning**: Group problem-solving activities

## 🏗️ System Architecture

### Web Application (Flask)
- **Frontend**: Bootstrap-based responsive UI
- **Backend**: Flask with WTForms for form handling
- **Database**: SQLite for course and enrollment data
- **Security**: CSRF protection, encrypted sensitive data

### Canvas Integration
- **API**: Canvas REST API for course management
- **Authentication**: Token-based API access
- **Course Creation**: Automated Canvas course deployment
- **Enrollment**: Direct Canvas enrollment management

### Course Template System
- **Template Engine**: Customizable course structure
- **Content Generation**: Automated module and assignment creation
- **Skill Trees**: Gamified learning progression
- **Export System**: Canvas cartridge (.imscc) generation

### Automation & Workflows
- **GitHub Actions**: Automated course creation workflows
- **Email Notifications**: Automated faculty and student communication
- **Cleanup System**: Scheduled course lifecycle management
- **Export Generation**: Automated backup and migration support

## 🔧 Technical Details

### Technologies Used
- **Backend**: Python 3.11+, Flask, asyncio
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Database**: SQLite with encrypted sensitive data
- **Canvas API**: canvasapi library for Canvas integration
- **Security**: Fernet encryption, CSRF protection
- **Automation**: GitHub Actions, email notifications

### Key Components

```
canvas-course-gamification/
├── app.py                     # Main Flask application
├── server.py                  # Production server with logging
├── run.sh                     # Setup and deployment script
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
├── src/
│   └── course_templates/
│       └── linear_algebra_template.py  # Course creation engine
├── templates/                 # HTML templates
├── .github/
│   └── workflows/
│       └── course-automation.yml  # GitHub Actions workflow
├── config/
│   └── .privacy_encryption_key    # Encryption key
├── data/                      # SQLite databases
├── exports/                   # Generated course exports
└── logs/                      # Application logs
```

### Database Schema

```sql
-- Courses table
CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    instructor_name TEXT NOT NULL,
    instructor_email TEXT NOT NULL,
    canvas_course_id INTEGER,
    join_code TEXT UNIQUE,
    join_url TEXT,
    canvas_url TEXT,
    status TEXT DEFAULT 'active',
    created_date TEXT,
    cleanup_date TEXT,
    course_data TEXT  -- JSON configuration
);

-- Enrollments table
CREATE TABLE enrollments (
    enrollment_id TEXT PRIMARY KEY,
    course_id TEXT,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    enrollment_date TEXT,
    canvas_enrollment_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

-- Exports table
CREATE TABLE exports (
    export_id TEXT PRIMARY KEY,
    course_id TEXT,
    export_path TEXT,
    created_date TEXT,
    file_size INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);
```

## 🔒 Security Features

### Data Protection
- **Encryption**: Sensitive data encrypted with Fernet
- **CSRF Protection**: Form submission protection
- **Input Validation**: Server-side validation for all inputs
- **Secure Sessions**: HTTP-only, secure cookies

### API Security
- **Token Authentication**: Canvas API token management
- **Rate Limiting**: Prevents API abuse
- **Error Handling**: Secure error messages
- **Logging**: Comprehensive audit trail

### Privacy Compliance
- **Data Minimization**: Only collect necessary information
- **Automatic Cleanup**: 7-day data retention for test courses
- **Encrypted Storage**: Sensitive data never stored in plain text
- **Access Control**: Role-based access to system functions

## 📊 Monitoring & Analytics

### System Metrics
- Course creation rates
- Student enrollment statistics
- System performance indicators
- Error rates and success metrics

### Course Analytics
- Enrollment trends
- Usage patterns
- Export activity
- Cleanup operations

### Faculty Dashboard
- Course performance metrics
- Student engagement data
- Export history
- Access statistics

## 🚀 Deployment Options

### Local Development
```bash
./run.sh dev
```

### Production Server
```bash
./run.sh setup
./run.sh start
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t linear-algebra-builder .
docker run -p 5000:5000 linear-algebra-builder
```

### Cloud Deployment
- **Heroku**: Ready for Heroku deployment
- **AWS**: EC2 or Elastic Beanstalk compatible
- **Google Cloud**: App Engine ready
- **Azure**: Web App service compatible

## 🧪 Testing

### Run Tests
```bash
./run.sh test
```

### Manual Testing Checklist
- [ ] Course creation flow
- [ ] Student enrollment process
- [ ] Canvas integration
- [ ] Course export functionality
- [ ] Admin dashboard operations
- [ ] Email notifications
- [ ] Cleanup operations

## 🔧 Troubleshooting

### Common Issues

**Canvas API Connection Failed**
- Verify API token in `.env` file
- Check Canvas API URL
- Ensure token has proper permissions

**Database Errors**
- Run `./run.sh init` to reinitialize database
- Check file permissions in `data/` directory
- Verify SQLite installation

**Email Notifications Not Working**
- Configure SMTP settings in GitHub secrets
- Check email server connectivity
- Verify email template formatting

**Course Creation Failures**
- Check Canvas API rate limits
- Verify course configuration parameters
- Review application logs in `logs/`

### Debug Mode
```bash
./run.sh dev  # Start with debug logging
tail -f logs/app.log  # Monitor logs in real-time
```

## 📚 Additional Resources

### Documentation
- [Canvas API Documentation](https://canvas.instructure.com/doc/api/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

### Support
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions
- **Documentation**: Comprehensive guides and API reference

### Contributing
We welcome contributions! Please see our contributing guidelines and code of conduct.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Canvas Free for Teachers program
- Linear algebra education community
- Open source contributors
- GitHub Actions team

---

**Built with ❤️ for education**

Ready to transform linear algebra education? Get started now with the Linear Algebra Course Builder!
