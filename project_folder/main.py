import os
from auth import login
from student_view import show_student_menu
from professor_view import show_professor_menu

def main():
    """Main application entry point"""
    if not os.path.exists('data'):
        os.makedirs('data')

    while True:
        print("\n--- Thesis Management System ---")
        print("1. Login as Student")
        print("2. Login as Professor")
        print("0. Exit")
        choice = input("Select your role: ")

        if choice == '1':
            user = login('student')
            if user:
                show_student_menu(user)
        elif choice == '2':
            user = login('professor')
            if user:
                show_professor_menu(user)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()