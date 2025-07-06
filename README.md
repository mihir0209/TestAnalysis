# Advanced Student Evaluation System

## Project Overview

This is a comprehensive student evaluation system that goes beyond traditional scoring methods to analyze behavioral patterns and provide personalized feedback. Unlike Google Forms that judges students based only on correct answers, this system evaluates students on multiple behavioral and performance parameters to provide deeper insights into learning patterns.

## 🎯 Core Concept

The system creates a **room-based evaluation environment** (similar to gaming lobbies) where teachers can create test rooms, invite students via links, and monitor their performance in real-time. The platform captures detailed behavioral data during tests and provides AI-powered insights for both students and teachers.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  Django Templates + Bootstrap + JavaScript (Behavior Track) │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  Django Views + Forms + Authentication + Role Management    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│  Analytics Engine + Suggestion Engine + Export Services     │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  PostgreSQL + Django ORM + CSV Export + Future ML Pipeline  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: Django Templates + HTML/CSS + JavaScript
- **UI Framework**: Bootstrap (for responsive design)
- **Real-time**: WebSocket for live monitoring
- **Analytics**: Pandas + NumPy for data processing
- **ML Integration**: Scikit-learn (future scope)

## 📊 Behavioral Parameters Tracked

### 1. **Accuracy**
- **Definition**: Percentage of correct answers out of total attempted
- **Calculation**: (Correct Answers / Total Attempted) × 100
- **Use Case**: Basic performance indicator

### 2. **Correct-to-Incorrect Ratio**
- **Definition**: Ratio of correct responses to incorrect ones
- **Calculation**: Correct Answers / Incorrect Answers
- **Use Case**: Provides depth beyond simple scoring

### 3. **Average Time per Question**
- **Definition**: Mean time spent on each question
- **Calculation**: Total Time / Number of Questions
- **Use Case**: Identifies confidence vs confusion patterns

### 4. **Answer Change Percentage**
- **Definition**: Percentage of answers that were modified
- **Calculation**: (Changed Answers / Total Answers) × 100
- **Use Case**: Indicates uncertainty and decision-making patterns

### 5. **Revisit Proportion**
- **Definition**: Percentage of questions revisited
- **Calculation**: (Revisited Questions / Total Questions) × 100
- **Use Case**: Shows review habits and confidence levels

### 6. **Time Efficiency**
- **Definition**: Effectiveness of time usage
- **Calculation**: (Correct Answers × Available Time) / (Total Time Spent)
- **Use Case**: Measures optimal time management

### 7. **Additional Behavioral Metrics**
- **Confidence Level**: Self-reported confidence (1-5 scale)
- **Thinking Time**: Time before first answer attempt
- **Focus Lost Count**: Number of tab switches or window changes
- **Mouse Click Patterns**: Interaction tracking for engagement

## 🏛️ Core Features

### 1. **Room Management System**

#### Room Creation
- Teachers create test rooms with unique invite codes
- Configure room settings (max students, time limits, penalties)
- Set entry deadlines and access controls

#### Invite Link System
- Generate secure invite links for students
- Links expire after specified time
- Support for bulk invite generation

#### Entry Control
- **5-minute grace period** after test start
- **Late entry approval system** with teacher notification
- **Penalty system** for late entries (configurable)
- **Room capacity management**

### 2. **Test Configuration System**

#### Test Creation
- Support for **MCQ** and **Theory** questions
- **Flexible question types** with multimedia support
- **Question bank management** with categorization
- **Difficulty level assignment**

#### Test Templates
- **Pre-configured test templates** for quick setup
- **Template categories** (Quiz, Exam, Assignment, etc.)
- **Customizable settings** without questions
- **Template sharing** between teachers

#### Advanced Settings
- **Pause/Resume capability** (teacher configurable)
- **Retake policies** with attempt limits
- **Time management** (per question/total test)
- **Navigation controls** (forward/backward, jump to question)

### 3. **Evaluation Engine**

#### MCQ Evaluation
- **Instant scoring** with partial credit options
- **Negative marking** support
- **Weighted scoring** for different difficulty levels

#### Theory Question Evaluation
- **Keyword-based scoring** with weighted blocks
- **Flexible keyword blocks** (teacher configurable)
- **Threshold-based evaluation**
- **Manual override capability**

#### Keyword Block System
```
Block 1 (Weight: 40%)
├── Keyword 1: "photosynthesis"
├── Keyword 2: "chlorophyll"
└── Keyword 3: "light energy"

Block 2 (Weight: 35%)
├── Keyword 1: "glucose"
├── Keyword 2: "oxygen"
└── Keyword 3: "carbon dioxide"

Block 3 (Weight: 25%)
├── Keyword 1: "cellular respiration"
└── Keyword 2: "ATP"
```

### 4. **Real-time Monitoring Dashboard**

#### Teacher Dashboard
- **Live student progress** tracking
- **Real-time analytics** during test
- **Anomaly detection** alerts
- **Room management** controls

#### Student Progress Indicators
- **Completion status** (In Progress, Completed, Paused)
- **Time remaining** displays
- **Question navigation** tracking
- **Behavioral pattern** monitoring

#### Anomaly Detection System
- **Time-based anomalies**: Too fast/slow completion
- **Pattern anomalies**: Suspicious answer patterns
- **Behavioral anomalies**: Excessive tab switching
- **Performance anomalies**: Sudden improvement patterns

### 5. **Analytics Engine**

#### Student Analytics
- **Individual performance** breakdown
- **Behavioral pattern** analysis
- **Improvement suggestions** based on data
- **Historical performance** tracking

#### Teacher Analytics
- **Class-wide performance** summaries
- **Question difficulty** analysis
- **Behavioral summaries** of students
- **Comparative analysis** across tests

#### Suggestion Engine
- **Personalized recommendations** for students
- **Behavioral improvement** suggestions
- **Study pattern** optimization
- **Time management** tips

## 🎨 User Interface Design

### Student View
- **Clean, distraction-free** test interface
- **Progress indicators** and timers
- **Question navigation** panel
- **Confidence level** input for each question
- **Review and submit** interface

### Teacher View
- **Test creation** wizard
- **Room management** dashboard
- **Live monitoring** interface
- **Analytics dashboard** with charts
- **Report generation** tools

## 📊 Data Model Structure

### Core Entities

#### User Management
```python
User
├── id, name, email, password
├── role (student/teacher/admin)
├── profile_data (JSON)
└── created_at, updated_at
```

#### Room System
```python
Room
├── id, name, description
├── teacher_id, test_id
├── invite_code, entry_deadline
├── is_active, max_students
├── late_penalty, settings (JSON)
└── created_at, updated_at
```

#### Test Structure
```python
Test
├── id, title, description
├── created_by, room_id
├── can_pause, analytics_mode
├── total_time, questions_count
├── settings (JSON)
└── created_at, updated_at

Question
├── id, test_id, question_text
├── type (MCQ/Theory)
├── options (JSON), correct_answer
├── evaluation_type, keywords (JSON)
├── keyword_threshold, difficulty_level
└── created_at, updated_at
```

#### Response Tracking
```python
Response
├── id, user_id, test_id, question_id
├── answer, is_correct, confidence_level
├── time_taken, time_before_first_answer
├── changed, revisited, mouse_clicks
├── focus_lost_count, timestamp
└── created_at, updated_at
```

#### Analytics Storage
```python
Analytics
├── id, user_id, test_id
├── accuracy, correct_incorrect_ratio
├── avg_time_per_question, change_percentage
├── revisit_proportion, time_efficiency
├── behavioral_score, suggestions (JSON)
└── created_at, updated_at
```

## 🔐 Security Features

### Authentication & Authorization
- **Role-based access control** (Student/Teacher/Admin)
- **Session management** with secure cookies
- **Password encryption** with Django's built-in system
- **CSRF protection** on all forms

### Test Security
- **Invite code verification** for room entry
- **Time-based access control**
- **Anti-cheating measures** (tab monitoring, time limits)
- **Audit trails** for all user actions

### Data Protection
- **Personal data encryption** for sensitive information
- **GDPR compliance** with data retention policies
- **Secure data export** with anonymization options
- **Backup and recovery** procedures

## 🚀 Development Phases

### Phase 1: Foundation (Weeks 1-2)
- [x] Django project setup ✅
- [x] PostgreSQL integration (SQLite configured for dev) ✅
- [x] User authentication system ✅
- [x] Basic models (User, Room, Test, Question) ✅
- [ ] Room creation and invite system 🔄

### Phase 2: Core Functionality (Weeks 3-4)
- [ ] Test creation interface
- [ ] Question management system
- [ ] Student test-taking interface
- [ ] Basic response collection
- [ ] Room entry management

### Phase 3: Behavioral Tracking (Weeks 5-6)
- [ ] JavaScript behavior tracking
- [ ] Real-time data collection
- [ ] Response model enhancements
- [ ] Time tracking implementation
- [ ] Focus and interaction monitoring

### Phase 4: Analytics Engine (Weeks 7-8)
- [ ] Analytics calculation algorithms
- [ ] Performance metrics computation
- [ ] Data aggregation and storage
- [ ] CSV export functionality
- [ ] Suggestion engine development

### Phase 5: Dashboard & Reporting (Weeks 9-10)
- [ ] Student analytics dashboard
- [ ] Teacher class analytics
- [ ] Real-time monitoring interface
- [ ] Report generation system
- [ ] Anomaly detection implementation

### Phase 6: UI/UX Polish (Weeks 11-12)
- [ ] Bootstrap integration
- [ ] Responsive design implementation
- [ ] User experience optimization
- [ ] Testing and debugging
- [ ] Performance optimization

### Phase 7: ML Integration (Future Scope)
- [ ] Historical data analysis
- [ ] ML model training pipeline
- [ ] Predictive analytics
- [ ] Advanced suggestion algorithms
- [ ] Pattern recognition system

## 📈 Machine Learning Integration

### Data Pipeline
- **Data Collection**: Behavioral metrics from all tests
- **Data Preprocessing**: Cleaning and normalization
- **Feature Engineering**: Creating meaningful features
- **Model Training**: Using historical data patterns
- **Prediction**: Real-time suggestions and insights

### ML Models Planned
- **Classification**: Student performance categorization
- **Regression**: Time estimation and efficiency prediction
- **Clustering**: Student behavioral pattern grouping
- **Anomaly Detection**: Cheating and unusual pattern detection
- **Recommendation**: Personalized study suggestions

## 🎯 Future Enhancements

### Short-term (6 months)
- **Mobile app** development
- **Advanced analytics** with charts
- **Bulk operations** for teachers
- **Question import/export** functionality
- **Advanced templates** with AI suggestions

### Long-term (1 year)
- **AI-powered question generation**
- **Predictive performance** analytics
- **Integration with LMS** systems
- **Advanced proctoring** features
- **Multi-language support**

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js (for JavaScript dependencies)
- Git

### Local Development Setup
```bash
# Clone the repository
git clone https://github.com/mihir0209/TestAnalysis.git
cd TestAnalysis

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 📋 API Documentation

### Room Management
- `POST /api/rooms/create/` - Create new room
- `GET /api/rooms/{id}/` - Get room details
- `POST /api/rooms/{id}/join/` - Join room with invite code
- `GET /api/rooms/{id}/students/` - Get room participants

### Test Management
- `POST /api/tests/create/` - Create new test
- `GET /api/tests/{id}/` - Get test details
- `POST /api/tests/{id}/submit/` - Submit test responses
- `GET /api/tests/{id}/analytics/` - Get test analytics

### Analytics
- `GET /api/analytics/student/{id}/` - Get student analytics
- `GET /api/analytics/class/{id}/` - Get class analytics
- `POST /api/analytics/export/` - Export analytics data

## 🤝 Contributing

### Development Guidelines
- Follow PEP 8 coding standards
- Write comprehensive tests
- Update documentation for new features
- Use meaningful commit messages

### Code Review Process
- Create feature branches
- Submit pull requests
- Peer review required
- Automated testing must pass

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Project Lead**: MiHiR 
- **Backend Developer**: Also MiHiR
- **Frontend Developer**: Yupp, MiHiR again
- **Data Scientist**: Okay, kidding!! MiHiR again.

## 📞 Support

For support and questions:
- Email: Nope
- Documentation: Hehe
- Issues: Issues bahut hote hain janab project mai, sudhaar koi nahi laata.

---

**Built with ❤️ for better education and learning analytics**
