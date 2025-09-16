from datetime import datetime
from database import load_data, save_data

def show_professor_menu(professor):
    """Display and handle professor menu options"""
    while True:
        print("\n--- Professor Panel ---")
        print("1. Review Thesis Requests (Supervisor)")
        print("2. Manage Defense Requests (Supervisor)")
        print("3. Submit Grade (Reviewer)")
        print("4. Search Thesis Archive")
        print("5. Change Password")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            manage_thesis_requests(professor['professor_id'])
        elif choice == '2':
            manage_defense_requests(professor['professor_id'])
        elif choice == '3':
            grade_thesis(professor['professor_id'])
        elif choice == '4':
            from student_view import search_theses
            search_theses()
        elif choice == '5':
            from auth import change_password
            change_password('professor', professor['professor_id'])
        elif choice == '0':
            break
        else:
            print("Invalid option.")

def manage_thesis_requests(professor_id):
    """Approve or reject thesis requests as supervisor"""
    theses = load_data('theses.json')
    students = load_data('students.json')
    
    requests = [t for t in theses if t['professor_id'] == professor_id and t['status'] == 'pending_approval']
    
    if not requests:
        print("No new requests for you.")
        return

    print("\nThesis Request List:")
    for req in requests:
        student_name = next((s['name'] for s in students if s['student_id'] == req['student_id']), "N/A")
        print(f"Request ID: {req['thesis_id']}, Student: {student_name}, Date: {req['request_date']}")
    
    thesis_id = input("Enter request ID to review (or 0 to return): ")
    if thesis_id == '0':
        return

    chosen_thesis = next((t for t in theses if t['thesis_id'] == thesis_id), None)
    if not chosen_thesis or chosen_thesis['professor_id'] != professor_id:
        print("Invalid request ID.")
        return

    action = input("Enter 'y' to approve or 'n' to reject: ").lower()
    if action == 'y':
        active_supervisions = sum(1 for t in theses if t['professor_id'] == professor_id and t['status'] == 'approved')
        professor_data = next((p for p in load_data('professors.json') if p['professor_id'] == professor_id), None)
        if active_supervisions >= professor_data['supervision_capacity']:
            print("Your supervision capacity is full.")
            return
        chosen_thesis['status'] = 'approved'
        chosen_thesis['approval_date'] = datetime.now().strftime("%Y-%m-%d")
        print("Request approved successfully.")
    elif action == 'n':
        chosen_thesis['status'] = 'rejected'
        print("Request rejected.")
    else:
        print("Invalid input.")
        return

    save_data('theses.json', theses)

def manage_defense_requests(professor_id):
    """Manage defense requests and assign reviewers"""
    theses = load_data('theses.json')
    professors = load_data('professors.json')
    
    requests = [t for t in theses if t['professor_id'] == professor_id and t['status'] == 'defense_requested']
    
    if not requests:
        print("No defense requests for you.")
        return

    print("\nDefense Request List:")
    for req in requests:
        print(f"Thesis ID: {req['thesis_id']}, Title: {req['title']}")

    thesis_id = input("Enter thesis ID to review (or 0 to return): ")
    if thesis_id == '0': return

    chosen_thesis = next((t for t in theses if t['thesis_id'] == thesis_id), None)
    if not chosen_thesis or chosen_thesis['professor_id'] != professor_id:
        print("Invalid ID.")
        return

    print(f"Details: \nTitle: {chosen_thesis['title']}\nAbstract: {chosen_thesis['abstract']}")
    action = input("Enter 'y' to approve and assign reviewers or 'n' to reject: ").lower()

    if action == 'y':
        defense_date = input("Enter defense date (YYYY-MM-DD): ")
        print("Available professors for review:")
        for prof in professors:
            if prof['professor_id'] != professor_id:
                print(f"ID: {prof['professor_id']}, Name: {prof['name']}")
        
        internal_reviewer_id = input("Select internal reviewer ID: ")
        external_reviewer_id = input("Select external reviewer ID: ")
        
        chosen_thesis['defense_date'] = defense_date
        chosen_thesis['reviewers'] = {
            "internal": internal_reviewer_id,
            "external": external_reviewer_id
        }
        chosen_thesis['status'] = 'ready_for_defense'
        print("Defense process approved successfully.")
    elif action == 'n':
        chosen_thesis['status'] = 'approved'
        print("Defense request rejected.")
    else:
        print("Invalid input.")
        return

    save_data('theses.json', theses)

def grade_thesis(professor_id):
    """Submit final grade as a reviewer"""
    theses = load_data('theses.json')
    
    reviewable_theses = [t for t in theses if professor_id in t.get('reviewers', {}).values() and t['status'] == 'ready_for_defense']
    
    if not reviewable_theses:
        print("No theses available for your review.")
        return
        
    print("\nTheses ready for grading:")
    for thesis in reviewable_theses:
        if datetime.strptime(thesis['defense_date'], "%Y-%m-%d") <= datetime.now():
            print(f"Thesis ID: {thesis['thesis_id']}, Title: {thesis['title']}")
        
    thesis_id = input("Enter thesis ID to grade: ")
    chosen_thesis = next((t for t in reviewable_theses if t['thesis_id'] == thesis_id), None)
    
    if not chosen_thesis:
        print("Invalid ID.")
        return
        
    try:
        score = float(input("Enter final score (0-20): "))
        if not 0 <= score <= 20:
            raise ValueError
    except ValueError:
        print("Please enter a valid number between 0-20.")
        return
    
    grade = ''
    if 17 <= score <= 20: grade = 'A'
    elif 13 <= score < 17: grade = 'B'
    elif 10 <= score < 13: grade = 'C'
    else: grade = 'D'
        
    chosen_thesis['grade'] = grade
    chosen_thesis['status'] = 'defended'
    save_data('theses.json', theses)
    print(f"Grade submitted successfully. Result: {grade}")