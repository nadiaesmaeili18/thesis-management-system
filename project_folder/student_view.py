import uuid
from datetime import datetime, timedelta
from database import load_data, save_data

def show_student_menu(student):
    """Display and handle student menu options"""
    while True:
        print("\n--- Student Panel ---")
        print("1. Request Thesis Course")
        print("2. View Thesis Status")
        print("3. Submit Defense Request")
        print("4. Search Thesis Archive")
        print("5. Change Password")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            request_thesis(student['student_id'])
        elif choice == '2':
            view_thesis_status(student['student_id'])
        elif choice == '3':
            request_defense(student['student_id'])
        elif choice == '4':
            search_theses()
        elif choice == '5':
            from auth import change_password
            change_password('student', student['student_id'])
        elif choice == '0':
            break
        else:
            print("Invalid option.")

def request_thesis(student_id):
    """Allow student to request a thesis course from available options"""
    courses = load_data('courses.json')
    theses = load_data('theses.json')

    for thesis in theses:
        if thesis['student_id'] == student_id and thesis['status'] != 'rejected':
            print("You already have an active or approved request.")
            return

    print("Available thesis courses with capacity:")
    available_courses = []
    for course in courses:
        enrollments = sum(1 for t in theses if t['course_id'] == course['course_id'] and t['status'] != 'rejected')
        if course['capacity'] > enrollments:
            available_courses.append(course)
            professors = load_data('professors.json')
            prof_name = next((p['name'] for p in professors if p['professor_id'] == course['professor_id']), "N/A")
            print(f"ID: {course['course_id']}, Title: {course['title']}, Professor: {prof_name}, Year: {course['year']}")
    
    if not available_courses:
        print("No courses with available capacity at the moment.")
        return

    course_id = input("Enter the course ID to request: ")
    chosen_course = next((c for c in available_courses if c['course_id'] == course_id), None)

    if chosen_course:
        new_thesis = {
            "thesis_id": str(uuid.uuid4()),
            "student_id": student_id,
            "course_id": course_id,
            "professor_id": chosen_course['professor_id'],
            "request_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "pending_approval",
            "approval_date": None,
            "title": None,
            "abstract": None,
            "keywords": [],
            "pdf_path": None,
            "defense_request_date": None,
            "defense_date": None,
            "reviewers": {},
            "grade": None
        }
        theses.append(new_thesis)
        save_data('theses.json', theses)
        print("Your request has been submitted successfully and sent to the professor.")
    else:
        print("Invalid course ID.")

def view_thesis_status(student_id):
    """Display the status of student's thesis request"""
    theses = load_data('theses.json')
    student_thesis = next((t for t in reversed(theses) if t['student_id'] == student_id), None)

    if student_thesis:
        status_mapping = {
            "pending_approval": "Pending Approval",
            "approved": "Approved",
            "rejected": "Rejected",
            "defense_requested": "Defense Requested",
            "ready_for_defense": "Ready for Defense",
            "defended": "Defended"
        }
        status = status_mapping.get(student_thesis['status'], student_thesis['status'])
        print(f"Your latest request status: {status}")
        if student_thesis['status'] == 'approved':
            print(f"Approval date: {student_thesis['approval_date']}")
    else:
        print("You have no submitted requests.")

def request_defense(student_id):
    """Submit defense request after thesis approval and 3 months waiting period"""
    theses = load_data('theses.json')
    student_thesis = next((t for t in theses if t['student_id'] == student_id), None)

    if not student_thesis or student_thesis['status'] != 'approved':
        print("You don't have an approved thesis to request defense.")
        return

    approval_date = datetime.strptime(student_thesis['approval_date'], "%Y-%m-%d")
    if datetime.now() < approval_date + timedelta(days=90):
        print("At least 3 months must pass since thesis approval.")
        return
    
    print("Please complete your thesis information:")
    student_thesis['title'] = input("Thesis title: ")
    student_thesis['abstract'] = input("Abstract: ")
    student_thesis['keywords'] = [k.strip() for k in input("Keywords (comma separated): ").split(',')]
    student_thesis['pdf_path'] = input("PDF file path: ")
    input("Place first and last page images in project folder and press Enter.")

    student_thesis['status'] = 'defense_requested'
    student_thesis['defense_request_date'] = datetime.now().strftime("%Y-%m-%d")
    save_data('theses.json', theses)
    print("Defense request submitted successfully and sent to your supervisor.")

def search_theses():
    """Advanced search function for defended theses with multiple search options"""
    theses = load_data('theses.json')
    students = load_data('students.json')
    professors = load_data('professors.json')
    
    defended_theses = [t for t in theses if t['status'] == 'defended']
    
    if not defended_theses:
        print("Thesis archive is empty.")
        return

    print("\n" + "="*50)
    print("Advanced Thesis Search System")
    print("="*50)
    print("1. Search all fields")
    print("2. Search by title")
    print("3. Search by author")
    print("4. Search by supervisor")
    print("5. Search by keywords")
    print("6. Search by year")
    print("7. Search by grade")
    print("0. Back")
    
    search_type = input("\nSelect search type (0-7): ")
    
    if search_type == "0":
        return
    
    term = input("Enter search term: ").strip()
    
    if not term:
        print("Search term cannot be empty.")
        return
    
    results = []
    
    for thesis in defended_theses:
        student_name = next((s['name'] for s in students if s['student_id'] == thesis['student_id']), "Unknown")
        prof_name = next((p['name'] for p in professors if p['professor_id'] == thesis['professor_id']), "Unknown")
        
        if search_type == "1":
            search_content = [
                thesis.get('title', ''),
                student_name,
                prof_name,
                ' '.join(thesis.get('keywords', [])),
                str(thesis.get('year', '')),
                thesis.get('grade', '')
            ]
        elif search_type == "2":
            search_content = [thesis.get('title', '')]
        elif search_type == "3":
            search_content = [student_name]
        elif search_type == "4":
            search_content = [prof_name]
        elif search_type == "5":
            search_content = [' '.join(thesis.get('keywords', []))]
        elif search_type == "6":
            search_content = [str(thesis.get('year', ''))]
        elif search_type == "7":
            search_content = [thesis.get('grade', '')]
        else:
            print("Invalid option")
            return
        
        if any(term.lower() in str(content).lower() for content in search_content if content):
            results.append((thesis, student_name, prof_name))
    
    if not results:
        print("No results found.")
        return
    
    print(f"\nSearch results ({len(results)} items):")
    print("="*60)
    
    for i, (thesis, student_name, prof_name) in enumerate(results, 1):
        print(f"\n{i}. Title: {thesis.get('title', 'No title')}")
        print(f"   Author: {student_name}")
        print(f"   Supervisor: {prof_name}")
        print(f"   Keywords: {', '.join(thesis.get('keywords', ['No keywords']))}")
        print(f"   Grade: {thesis.get('grade', 'Not specified')}")
        print(f"   Year: {thesis.get('year', 'Unknown')}")
        
        if thesis.get('abstract'):
            abstract = thesis['abstract']
            if len(abstract) > 100:
                abstract = abstract[:100] + "..."
            print(f"   Abstract: {abstract}")
        
        print(f"   File: {thesis.get('pdf_path', 'Not available')}")
        print("-" * 50)