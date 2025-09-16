# Thesis Management System - Final Project Documentation

## 1. Project Title and General Information
- **Project Name:** Thesis Management System  
- **Full Name:** Nadia Esmaeili  
- **Student ID:** 402103231  
- **National ID:** 0110530659  
- **Repository Address:** https://github.com/nadiasemaeili18/thesis-management-system  

## 2. Project Overview 
### Project Goal
The goal of this project is to design and implement a comprehensive system for managing the entire thesis process from initial course enrollment to final defense evaluation. The system facilitates academic workflow management between students and professors while maintaining capacity constraints and tracking all necessary documentation.

### General Program Functionality Description
The system provides a complete thesis management solution with two main user roles (student and professor) and handles all stages of thesis processing including course enrollment requests, approval workflows, defense scheduling, and final grading. The application uses JSON-based data storage and follows object-oriented programming principles.

### Base Sections and Additional Features Implementation:

**Student Module:** Implements student authentication, thesis course request functionality, status tracking, defense request submission after 3-month waiting period, and advanced search capabilities in the thesis archive. Students can view available courses, submit requests, and track their thesis status through various stages.

**Professor Module:** Provides professors with tools to manage thesis requests, approve/reject submissions based on capacity constraints, manage defense scheduling, assign internal/external reviewers, and submit final grades. The system enforces capacity limits (5 supervisions, 10 reviews per professor).

**Authentication System:** Handles role-based login for both students and professors with password change functionality. Users authenticate with their institutional IDs and passwords stored in JSON format.

**Search Functionality:** Implements advanced search across defended theses with multiple criteria including title, author, supervisor, keywords, year, and grade. Results display comprehensive thesis information with abstract previews.

**Data Management:** Uses JSON files for persistent storage of all system data including user information, course details, and thesis records. The system automatically tracks dates and status changes throughout the thesis lifecycle.

## 3. Requirements 

### Python Version
- Python 3.8 or higher

### Libraries/Packages Used
- json (for data serialization and storage)
- os (for file system operations)
- uuid (for generating unique identifiers)
- datetime (for date tracking and validation)
- No external dependencies required (uses only Python standard library)

## 4. Project Structure 

### File List with Brief Structure Description:
- **main.py**: Main application entry point that handles role selection and menu navigation
- **auth.py**: Authentication module handling user login and password management
- **database.py**: Data persistence functions for loading/saving JSON data
- **student_view.py**: Student-specific functionality and menu interface
- **professor_view.py**: Professor-specific functionality and menu interface
- **data/students.json**: Stores student information and credentials
- **data/professors.json**: Stores professor information with capacity limits
- **data/courses.json**: Contains thesis course offerings and details
- **data/theses.json**: Maintains thesis records, status, and evaluation data

## 5. Classes and Functions 

### Functions with Performance Description:

**main.py Functions:**
- `main()`: Primary application entry point that displays the main menu and handles user authentication flow

**auth.py Functions:**
- `login(user_type)`: Authenticates users based on role and credentials
- `change_password(user_type, user_id)`: Allows users to update their passwords

**database.py Functions:**
- `load_data(filename)`: Loads and parses JSON data from files
- `save_data(filename, data)`: Serializes and saves data to JSON files

**student_view.py Functions:**
- `show_student_menu(student)`: Displays and manages the student menu interface
- `request_thesis(student_id)`: Handles thesis course enrollment requests
- `view_thesis_status(student_id)`: Shows current status of thesis applications
- `request_defense(student_id)`: Manages defense request submission after 3-month period
- `search_theses()`: Implements advanced search functionality

**professor_view.py Functions:**
- `show_professor_menu(professor)`: Displays and manages the professor menu interface
- `manage_thesis_requests(professor_id)`: Handles thesis request approval/rejection
- `manage_defense_requests(professor_id)`: Manages defense scheduling and reviewer assignment
- `grade_thesis(professor_id)`: Handles grade submission after defense

### Attributes and Methods:
The system uses functional programming approach with clearly defined functions for each operation. Data attributes are stored in JSON structures including user credentials, course information, and thesis details with status tracking.

## 6. Implementation Details (جزییات پیاده‌سازی)

### Algorithms and Specific Logic Used:
- **Capacity Management Algorithm**: Enforces professor supervision and review limits using counter checks
- **Date Validation Logic**: Ensures 3-month waiting period between thesis approval and defense requests
- **Search Algorithm**: Implements multi-criteria search across thesis records with field-specific matching
- **Status Workflow Logic**: Manages state transitions between pending, approved, rejected, and completed statuses
- **Data Persistence**: Implements atomic read-write operations for JSON data storage

## 7. How to Run 

### Steps to Run the Project on User's System:
1. Clone the repository: `git clone https://github.com/nadiasemaeili18/thesis-management-system.git`
2. Navigate to project directory: `cd thesis-management-system`
3. Create data directory with required JSON files (students.json, professors.json, courses.json, theses.json)
4. Run the application: `python main.py`
5. Select role (Student/Professor) and login with appropriate credentials
6. Use menu options to access various system functionalities

## 8. Sample Output 



**Login Function Output:**

## 9. Known Issues and Improvements 

### Incomplete Implemented Ideas and Improvement Solutions:

**Current Limitations:**
- Passwords stored in plain text (needs hashing implementation)
- No concurrent access handling for JSON files
- Basic file upload handling for thesis documents
- No email notification system for status updates
- Console-based interface without GUI

**Improvement Suggestions:**
1. Implement password hashing using bcrypt or similar encryption
2. Add database locking mechanism for concurrent access
3. Develop proper file upload system with PDF validation
4. Integrate email notifications for status changes
5. Create web-based interface using Flask or Django
6. Add reporting and analytics module
7. Implement REST API for system integration
8. Develop mobile application companion
