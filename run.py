import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pyfiglet

USER_OPTIONS = """
1. Filter Data
2. Add New Student
3. Exit
"""


def authenticate_google_sheets():
    """
    Authenticates with Google Sheets API
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope
    )
    client = gspread.authorize(credentials)
    return client


def get_user_choice():
    """
    Displays the main menu and get user choice
    """
    while True:
        print(pyfiglet.figlet_format("Main Menu"))
        print(USER_OPTIONS)
        choice = input("\nEnter your choice (1, 2, or 3):\n").strip()
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_data_from_google_sheet(CLIENT):
    """
    Retrieves filtered data from Google Sheet
    """
    while True:
        spreadsheet = CLIENT.open("student_data")
        worksheet = spreadsheet.get_worksheet(0)

        # Ask user for column name and value to filter the data
        column_name = (
            input(
                "\nEnter column name "
                "(Gender, Year, Favourite Subject, or Club):\n"
            )
            .strip()
            .title()
        )
        if column_name not in ["Gender", "Year", "Favourite Subject", "Club"]:
            print(
                "Invalid column name. "
                "Please choose from Gender, Year, Favourite Subject, or Club."
            )
            continue

        if column_name in ["Favourite Subject", "Club"]:
            # Provide a list of available choices
            existing_choices = (
                set(worksheet.col_values(4)[1:])
                if column_name == "Favourite Subject"
                else set(worksheet.col_values(5)[1:])
            )
            print(f"Available {column_name}s: {', '.join(existing_choices)}")

        value = (
            input(f"Enter {column_name} to filter the data:\n")
            .strip()
            .capitalize()
        )

        # Get all records from the worksheet
        data = worksheet.get_all_records()

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Apply filtering based on user input
        if column_name == "Year":
            try:
                value = int(value)
            except ValueError:
                print("Invalid input for Year. Please enter a number.")
                continue

        filtered_df = df[df[column_name] == value]

        # Check if any records were found
        if not filtered_df.empty:
            print("\nFiltered Data:")
            print(filtered_df)
            # Return the filtered data
            return filtered_df
        else:
            print(
                f"No records found for {column_name}: {value}. Please try again."
            )

        # Ask if the user wants to filter data again
        repeat_filter = (
            input("\nDo you want to filter data again? (y/n):\n")
            .strip()
            .lower()
        )
        if repeat_filter not in ["y", "yes"]:
            # Return None if the user does not want to filter data again
            return None


def analyze_data(df):
    """
    Analyzes the data (total students,
    favorite subjects, club counts)
    """
    total_students = len(df)
    favorite_subject_counts = df["Favourite Subject"].value_counts(
    ).reset_index()
    club_counts = df["Club"].value_counts().reset_index()
    favorite_subject_counts.columns = ["Favourite Subject", "Count"]
    club_counts.columns = ["Club", "Count"]

    return total_students, favorite_subject_counts, club_counts


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

        while gender not in ["Male", "Female"]:
            print("Invalid gender. Please enter 'Male' or 'Female'.")
            gender = (
                input("Enter gender (Male/Female):\n").strip().capitalize()
            )

        year = input("\nEnter student's year (7-13): ")
        while not year.isdigit() or int(year) not in range(7, 14):
            print("Invalid year. Please enter a number between 7 and 13.")
            year = input("Enter student's year (7-13):\n")

        # Ask for favorite subject
        favorite_subject = (
            input("\nEnter favorite subject:\n").strip().capitalize()
        )

        # Check if the subject already exists in the database
        existing_subjects = set(worksheet.col_values(4)[1:])
        if favorite_subject not in existing_subjects:
            confirm_subject = input(
                f"'{favorite_subject}' is not in the database. Do you want to add it as a new subject? (y/n):\n"
            ).strip().lower()
            if confirm_subject not in ["y", "yes"]:
                continue

        # Ask for club
        club = input("\nEnter club:\n").strip().capitalize()

        # Check if the club already exists in the database
        existing_clubs = set(worksheet.col_values(5)[1:])
        if club not in existing_clubs:
            confirm_club = input(
                f"'{club}' is not in the database. Do you want to add it as a new club? (y/n):\n"
            ).strip().lower()
            if confirm_club not in ["y", "yes"]:
                continue

        # Append student details to the Google Sheet
        worksheet.append_row([name, gender, year, favorite_subject, club])
        print("\nStudent added successfully!")

        # Ask if the user wants to add another student
        add_another = (
            input("\nDo you want to add another student? (y/n):\n")
            .strip()
            .lower()
        )
        if add_another not in ["y", "yes"]:
            break


def main():
    """
    Main function that orchestrates the workflow
    """
    CLIENT = authenticate_google_sheets()

    while True:
        choice = get_user_choice()

        if choice == "1":
            df = get_data_from_google_sheet(CLIENT)
            if df is not None:
                analyze_data(df)
        elif choice == "2":
            add_new_student(CLIENT)
        else:
            print("Exiting the program. Goodbye!")
            break


if __name__ == "__main__":
    # Execute main Python function
    main()
