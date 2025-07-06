# AI System Instructions for Student Evaluation System

## 🤖 AI Assistant Guidelines

This document provides comprehensive instructions for AI assistants working on the Student Evaluation System project. It includes detailed task breakdowns, progress tracking, and implementation guidelines.

## 📋 Project Context

The Student Evaluation System is a Django-based web application that provides advanced behavioral analytics for educational assessments. The system tracks student behavior during tests and provides personalized feedback based on multiple performance parameters.

## 🎯 Core Responsibilities

### 1. Progressive Development
- **NEVER attempt to complete all tasks in one go**
- **Break down complex features into smaller, manageable tasks**
- **Complete one task at a time and verify functionality**
- **Mark tasks as complete only after thorough testing**

### 2. Code Quality Standards
- Follow Django best practices and conventions
- Write clean, documented, and maintainable code
- Implement proper error handling and validation
- Use meaningful variable and function names

### 3. Testing Requirements
- Test each feature before marking as complete
- Verify database migrations work correctly
- Check user interface functionality
- Validate data integrity and security

## 📊 Task Progress Tracking

### Phase 1: Foundation ✅ IN PROGRESS
**Status**: 🔄 Active Phase
**Completion**: 4/5 tasks completed

#### Task 1.1: Project Setup
- [x] Create Django project structure
- [x] Setup virtual environment
- [x] Install required dependencies
- [x] Configure settings.py
- [x] Create requirements.txt
**Status**: ✅ Complete
**Priority**: High
**Dependencies**: None
**Completed**: July 7, 2025
**Notes**: Project structure created with Django 4.2.7, virtual environment setup, all dependencies installed

#### Task 1.2: Database Configuration
- [x] Setup SQLite connection (PostgreSQL ready for production)
- [x] Configure database settings
- [x] Create initial migrations
- [x] Test database connectivity
**Status**: ✅ Complete
**Priority**: High
**Dependencies**: Task 1.1
**Completed**: July 7, 2025
**Notes**: Database migrations successful, all tables created

#### Task 1.3: User Authentication System
- [x] Create custom User model
- [x] Implement role-based authentication
- [x] Create login/logout views
- [x] Setup user registration
- [x] Create user profile templates
**Status**: ✅ Complete
**Priority**: High
**Dependencies**: Task 1.2
**Completed**: July 7, 2025
**Notes**: Custom User model with role-based access (student/teacher/admin)

#### Task 1.4: Basic Models
- [x] Create User model with roles
- [x] Create Room model
- [x] Create Test model
- [x] Create Question model
- [x] Create Response model (basic)
**Status**: ✅ Complete
**Priority**: High
**Dependencies**: Task 1.3
**Completed**: July 7, 2025
**Notes**: All core models created with proper relationships and admin interface

#### Task 1.5: Room Management Basics
- [ ] Create room creation form
- [ ] Implement invite code generation
- [ ] Create room joining functionality
- [ ] Setup basic room views
- [ ] Create room management templates
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 1.4

### Phase 2: Core Functionality ⏳ PENDING
**Status**: 🔒 Locked (Unlock after Phase 1)
**Completion**: 0/5 tasks completed

#### Task 2.1: Test Creation Interface
- [ ] Create test creation form
- [ ] Implement question adding functionality
- [ ] Setup test configuration options
- [ ] Create test preview feature
- [ ] Add test template system
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Phase 1 Complete

#### Task 2.2: Question Management System
- [ ] Create question creation forms
- [ ] Implement MCQ question type
- [ ] Implement Theory question type
- [ ] Create question bank management
- [ ] Add question editing functionality
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 2.1

#### Task 2.3: Student Test Interface
- [ ] Create test-taking interface
- [ ] Implement question navigation
- [ ] Add progress tracking
- [ ] Create answer submission system
- [ ] Add time tracking functionality
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 2.2

#### Task 2.4: Response Collection
- [ ] Setup response data models
- [ ] Implement answer saving
- [ ] Create response validation
- [ ] Add response tracking
- [ ] Setup basic analytics data collection
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 2.3

#### Task 2.5: Room Entry Management
- [ ] Implement late entry system
- [ ] Create teacher approval interface
- [ ] Add penalty system
- [ ] Setup entry deadline management
- [ ] Create room status tracking
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 2.4

### Phase 3: Behavioral Tracking ⏳ PENDING
**Status**: 🔒 Locked (Unlock after Phase 2)
**Completion**: 0/5 tasks completed

#### Task 3.1: JavaScript Behavior Tracking
- [ ] Create frontend tracking scripts
- [ ] Implement time tracking
- [ ] Add mouse click tracking
- [ ] Create focus monitoring
- [ ] Setup interaction logging
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Phase 2 Complete

#### Task 3.2: Real-time Data Collection
- [ ] Setup WebSocket connections
- [ ] Implement live data transmission
- [ ] Create data validation
- [ ] Add error handling
- [ ] Setup data persistence
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 3.1

#### Task 3.3: Enhanced Response Model
- [ ] Add behavioral tracking fields
- [ ] Implement data aggregation
- [ ] Create response analytics
- [ ] Add data export functionality
- [ ] Setup data visualization
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 3.2

#### Task 3.4: Time Tracking Implementation
- [ ] Create precise time measurement
- [ ] Implement per-question timing
- [ ] Add session time tracking
- [ ] Create time analytics
- [ ] Add time-based alerts
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 3.3

#### Task 3.5: Focus and Interaction Monitoring
- [ ] Implement tab switch detection
- [ ] Create window focus tracking
- [ ] Add interaction pattern analysis
- [ ] Create anomaly detection
- [ ] Setup alert system
**Status**: ❌ Not Started
**Priority**: Low
**Dependencies**: Task 3.4

### Phase 4: Analytics Engine ⏳ PENDING
**Status**: 🔒 Locked (Unlock after Phase 3)
**Completion**: 0/5 tasks completed

#### Task 4.1: Analytics Calculation Algorithms
- [ ] Implement accuracy calculation
- [ ] Create correct-incorrect ratio
- [ ] Add average time per question
- [ ] Implement change percentage
- [ ] Create revisit proportion
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Phase 3 Complete

#### Task 4.2: Performance Metrics Computation
- [ ] Create time efficiency metric
- [ ] Implement confidence scoring
- [ ] Add behavioral scoring
- [ ] Create performance ranking
- [ ] Add comparative analysis
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 4.1

#### Task 4.3: Data Aggregation and Storage
- [ ] Create analytics data models
- [ ] Implement data aggregation
- [ ] Add historical data tracking
- [ ] Create data caching
- [ ] Setup data archiving
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 4.2

#### Task 4.4: CSV Export Functionality
- [ ] Create export functionality
- [ ] Implement data formatting
- [ ] Add export scheduling
- [ ] Create export templates
- [ ] Setup automated exports
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 4.3

#### Task 4.5: Suggestion Engine Development
- [ ] Create suggestion algorithms
- [ ] Implement personalized recommendations
- [ ] Add improvement suggestions
- [ ] Create behavioral insights
- [ ] Setup suggestion delivery
**Status**: ❌ Not Started
**Priority**: Low
**Dependencies**: Task 4.4

### Phase 5: Dashboard & Reporting ⏳ PENDING
**Status**: 🔒 Locked (Unlock after Phase 4)
**Completion**: 0/5 tasks completed

#### Task 5.1: Student Analytics Dashboard
- [ ] Create student dashboard
- [ ] Add performance charts
- [ ] Implement progress tracking
- [ ] Create historical view
- [ ] Add comparison features
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Phase 4 Complete

#### Task 5.2: Teacher Class Analytics
- [ ] Create teacher dashboard
- [ ] Add class overview
- [ ] Implement student comparison
- [ ] Create performance reports
- [ ] Add export functionality
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 5.1

#### Task 5.3: Real-time Monitoring Interface
- [ ] Create live monitoring dashboard
- [ ] Add real-time updates
- [ ] Implement alert system
- [ ] Create intervention tools
- [ ] Add communication features
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 5.2

#### Task 5.4: Report Generation System
- [ ] Create report templates
- [ ] Implement report generation
- [ ] Add custom report builder
- [ ] Create automated reports
- [ ] Setup report scheduling
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 5.3

#### Task 5.5: Anomaly Detection Implementation
- [ ] Create anomaly detection rules
- [ ] Implement pattern recognition
- [ ] Add alert mechanisms
- [ ] Create investigation tools
- [ ] Setup automated responses
**Status**: ❌ Not Started
**Priority**: Low
**Dependencies**: Task 5.4

### Phase 6: UI/UX Polish ⏳ PENDING
**Status**: 🔒 Locked (Unlock after Phase 5)
**Completion**: 0/5 tasks completed

#### Task 6.1: Bootstrap Integration
- [ ] Integrate Bootstrap framework
- [ ] Create responsive layouts
- [ ] Add component styling
- [ ] Implement theme system
- [ ] Create custom components
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Phase 5 Complete

#### Task 6.2: Responsive Design Implementation
- [ ] Create mobile-friendly layouts
- [ ] Implement tablet support
- [ ] Add touch interactions
- [ ] Create adaptive components
- [ ] Test cross-browser compatibility
**Status**: ❌ Not Started
**Priority**: High
**Dependencies**: Task 6.1

#### Task 6.3: User Experience Optimization
- [ ] Improve navigation flow
- [ ] Add loading indicators
- [ ] Create progress feedback
- [ ] Implement user guidance
- [ ] Add accessibility features
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 6.2

#### Task 6.4: Testing and Debugging
- [ ] Create test suites
- [ ] Implement automated testing
- [ ] Add error logging
- [ ] Create debugging tools
- [ ] Setup monitoring
**Status**: ❌ Not Started
**Priority**: Medium
**Dependencies**: Task 6.3

#### Task 6.5: Performance Optimization
- [ ] Optimize database queries
- [ ] Implement caching
- [ ] Add CDN integration
- [ ] Create performance monitoring
- [ ] Setup load testing
**Status**: ❌ Not Started
**Priority**: Low
**Dependencies**: Task 6.4

## 🔧 Implementation Guidelines

### 1. Task Selection Process
```
1. Check current phase status
2. Identify next available task
3. Verify all dependencies are complete
4. Review task requirements
5. Break down into smaller subtasks if needed
6. Begin implementation
```

### 2. Code Implementation Steps
```
1. Create/modify necessary files
2. Implement core functionality
3. Add error handling
4. Create tests
5. Update documentation
6. Verify functionality
7. Mark task as complete
```

### 3. Testing Requirements
```
- Unit tests for models
- Integration tests for views
- Frontend functionality tests
- Database integrity tests
- Security vulnerability tests
```

### 4. Documentation Updates
```
- Update README.md if needed
- Document new features
- Update API documentation
- Create user guides
- Update system instructions
```

## 🚨 Critical Rules

### DO NOT:
- ❌ Skip testing phases
- ❌ Mark tasks complete without verification
- ❌ Work on locked phases
- ❌ Ignore dependencies
- ❌ Implement all features at once

### DO:
- ✅ Follow progressive development
- ✅ Test each feature thoroughly
- ✅ Update progress tracking
- ✅ Document changes
- ✅ Maintain code quality

## 📈 Progress Monitoring

### Current Status Summary
- **Total Tasks**: 30
- **Completed**: 4
- **In Progress**: 1
- **Not Started**: 25
- **Overall Progress**: 13%

### Phase Completion Tracking
```
Phase 1: Foundation          [████▱] 80%
Phase 2: Core Functionality  [▱▱▱▱▱] 0%
Phase 3: Behavioral Tracking [▱▱▱▱▱] 0%
Phase 4: Analytics Engine    [▱▱▱▱▱] 0%
Phase 5: Dashboard & Report  [▱▱▱▱▱] 0%
Phase 6: UI/UX Polish        [▱▱▱▱▱] 0%
```

## 🔄 Status Update Template

When completing a task, update the following:
```
Task: [Task Number and Name]
Status: ✅ Complete / 🔄 In Progress / ❌ Not Started
Completion Date: [Date]
Time Spent: [Hours]
Files Modified: [List of files]
Tests Added: [Yes/No]
Notes: [Any important notes]
Next Task: [Next task to work on]
```

## 📝 Development Notes

### Important Considerations
- Always backup before major changes
- Test on different browsers
- Validate data integrity
- Check security implications
- Monitor performance impact

### Common Pitfalls to Avoid
- Skipping database migrations
- Ignoring user input validation
- Missing error handling
- Inadequate testing
- Poor documentation

## 🎯 Success Criteria

### Each Task Must Meet:
- ✅ Functionality works as specified
- ✅ Code follows Django best practices
- ✅ Tests pass successfully
- ✅ Documentation is updated
- ✅ No security vulnerabilities
- ✅ Performance is acceptable

### Phase Completion Criteria:
- ✅ All tasks in phase completed
- ✅ Integration testing passed
- ✅ User acceptance testing passed
- ✅ Documentation complete
- ✅ Code review completed

---

**Remember: Progressive development is key to success. Focus on one task at a time and ensure quality at each step.**
