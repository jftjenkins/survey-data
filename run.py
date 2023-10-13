import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pyfiglet


def authenticate_google_sheets():
    """
    Function to authenticate with Google Sheets API
    """
    SCOPE = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", SCOPE)
    CLIENT = gspread.authorize(CREDENTIALS)
    return CLIENT


def get_user_choice():
    """
    Function to display the main menu and get user choice
    """
    while True:
        print(pyfiglet.figlet_format("Main Menu"))
        print("1. Filter Data")
        print("2. Add New Student")
        print("3. Exit")
        choice = input("\nEnter your choice (1, 2, or 3):\n").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_data_from_google_sheet(CLIENT):
    """
    Function to retrieve filtered data from Google Sheet
    """
    while True:
        spreadsheet = CLIENT.open("student_data")
        worksheet = spreadsheet.get_worksheet(0)

        # Ask user for column name and value to filter the data
        column_name = input(
            "\nEnter column name (Gender, Year, Favourite Subject, or Club):\n").strip().title()
        if column_name not in ['Gender', 'Year', 'Favourite Subject', 'Club']:
            print(
                "Invalid column name. Please choose from Gender, Year, Favourite Subject, or Club.")
            continue

        if column_name in ['Favourite Subject', 'Club']:
            # Provide a list of available choices
            existing_choices = set(worksheet.col_values(4)[1:]) if column_name == 'Favourite Subject' else set(
                worksheet.col_values(5)[1:])
            print(f"Available {column_name}s: {', '.join(existing_choices)}")

        value = input(
            f"Enter {column_name} to filter the data:\n").strip().capitalize()

        # Get all records from the worksheet
        data = worksheet.get_all_records()

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Apply filtering based on user input
        if column_name == 'Year':
            try:
                value = int(value)
                filtered_df = df[df[column_name] == value]
            except ValueError:
                print("Invalid input for Year. Please enter a number.")
                continue
        else:
            filtered_df = df[df[column_name] == value]

        # Check if any records were found
        if not filtered_df.empty:
            print("\nFiltered Data:")
            print(filtered_df)
            # Return the filtered data
            return filtered_df
        else:
            print(
                f"No records found for {column_name}: {value}. Please try again.")

        # Ask if the user wants to filter data again
        repeat_filter = input(
            "\nDo you want to filter data again? (y/n):\n").strip().lower()
        if repeat_filter not in ['y', 'yes']:
            # Return None if the user does not want to filter data again
            return None


def analyze_data(df):
    """
    Function to analyze the data (total students,
    favorite subjects, club counts)
    """
    total_students = len(df)
    favorite_subjects = df['Favourite Subject'].value_counts().reset_index()
    club_counts = df['Club'].value_counts().reset_index()
    favorite_subjects.columns = ['Favourite Subject', 'Count']
    club_counts.columns = ['Club', 'Count']
    return total_students, favorite_subjects, club_counts


def display_results(df, total_students, favorite_subjects, club_counts):
    """
    Function to display data and analysis results in the console
    """
    print()
    print("\nTotal Students:", total_students)


def add_new_student(CLIENT):
    """
    Function to add a new student to the Google Sheet
    """
    spreadsheet = CLIENT.open("student_data")
    worksheet = spreadsheet.get_worksheet(0)

    while True:
        # Get student details from the user and capitalize the names
        name = input("Enter student name:\n").strip().capitalize()
        gender = input("\nEnter gender (Male/Female):\n").strip().capitalize()

        while gender not in ['Male', 'Female']:
            print("Invalid gender. Please enter 'Male' or 'Female'.")
            gender = input(
                "Enter gender (Male/Female):\n").strip().capitalize()

        year = input("\nEnter student's year (7-13): ")
        while not year.isdigit() or int(year) not in range(7, 14):
            print("Invalid year. Please enter a number between 7 and 13.")
            year = input("Enter student's year (7-13):\n")

        # Ask for favorite subject
        while True:
            favorite_subject = input(
                "\nEnter favorite subject:\n").strip().capitalize()

            # Check if the subject already exists in the database
            existing_subjects = set(worksheet.col_values(4)[1:])
            if favorite_subject in existing_subjects:
                break  # Subject exists, proceed to club question

            confirm_subject = input(
                f"'{favorite_subject}' is not in the database. Are you sure you want to add it as a new subject? (y/n):\n").strip().lower()
            if confirm_subject in ['y', 'yes']:
                break  # User confirmed, proceed to club question

        # Ask for club
        while True:
            club = input("\nEnter club:\n").strip().capitalize()

            # Check if the club already exists in the database
            existing_clubs = set(worksheet.col_values(5)[1:])
            if club in existing_clubs:
                break  # Club exists, exit loop

            confirm_club = input(
                f"'{club}' is not in the database. Are you sure you want to add it as a new club? (y/n):\n").strip().lower()
            if confirm_club in ['y', 'yes']:
                break  # User confirmed, exit loop

        # Append student details to the Google Sheet
        worksheet.append_row([name, gender, year, favorite_subject, club])
        print("\nStudent added successfully!")

        # Ask if the user wants to add another student
        add_another = input(
            "\nDo you want to add another student? (y/n):\n").strip().lower()
        if add_another not in ['y', 'yes']:
            break  # Exit the loop if the user doesn't want to add another student


def main():
    """
    Main function that orchestrates the workflow
    """
    CLIENT = authenticate_google_sheets()

    while True:
        choice = get_user_choice()

        if choice == '1':
            df = get_data_from_google_sheet(CLIENT)
            if df is not None:
                total_students, favorite_subjects, club_counts = analyze_data(
                    df)
                display_results(df, total_students,
                                favorite_subjects, club_counts)
        elif choice == '2':
            add_new_student(CLIENT)
        else:
            print("Exiting the program. Goodbye!")
            break


if __name__ == "__main__":
    # Execute main Python function
    main()
