import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt


# Function to authenticate with Google Sheets API
def authenticate_google_sheets():
    SCOPE = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", SCOPE)
    CLIENT = gspread.authorize(CREDENTIALS)
    return CLIENT


# Function to retrieve filtered data from Google Sheet
def get_data_from_google_sheet(CLIENT):
    spreadsheet = CLIENT.open("student_data")
    worksheet = spreadsheet.get_worksheet(0)

    while True:
        # Ask user for column name and value to filter the data
        column_name = input(
            "\nEnter column name (Gender, Year, Favourite Subject, or Club): ").strip().title()
        if column_name not in ['Gender', 'Year', 'Favourite Subject', 'Club']:
            print(
                "Invalid column name. Please choose from Gender, Year, Favourite Subject, or Club.")
            continue

        value = input(
            f"Enter {column_name} to filter the data: ").strip().capitalize()

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
            return filtered_df
        else:
            print(
                f"No records found for {column_name}: {value}. Please try again.")


# Function to analyze the data (total students, favorite subjects, club counts)
def analyze_data(df):
    total_students = len(df)
    favorite_subjects = df['Favourite Subject'].value_counts().reset_index()
    club_counts = df['Club'].value_counts().reset_index()
    favorite_subjects.columns = ['Favourite Subject', 'Count']
    club_counts.columns = ['Club', 'Count']
    return total_students, favorite_subjects, club_counts


# Function to display data and analysis results in the console
def display_results(df, total_students, favorite_subjects, club_counts):
    print()
    print("Survey Data:")
    print()
    print(df)
    print("\nTotal Students:", total_students)


# Function to plot the data (gender distribution, favorite subjects distribution)
def plot_data(df):
    plt.figure(figsize=(8, 6))
    df['Gender'].value_counts().plot(kind='bar')
    plt.title('Distribution of Gender')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.show()


# Function to add a new student to the Google Sheet
def add_new_student(CLIENT):
    spreadsheet = CLIENT.open("student_data")
    worksheet = spreadsheet.get_worksheet(0)

    while True:
        # Get student details from the user and capitalize the names
        name = input("Enter student name: ").strip().capitalize()
        gender = input("\nEnter gender (Male/Female): ").strip().capitalize()

        while gender not in ['Male', 'Female']:
            print("Invalid gender. Please enter 'Male' or 'Female'.")
            gender = input("Enter gender (Male/Female): ").strip().capitalize()

        year = input("\nEnter student's year (7-13): ")
        while not year.isdigit() or int(year) not in range(7, 14):
            print("Invalid year. Please enter a number between 7 and 13.")
            year = input("Enter student's year (7-13): ")

        favorite_subject = input(
            "\nEnter favorite subject: ").strip().capitalize()

        # Check if the subject already exists in the database
        existing_subjects = set(worksheet.col_values(4)[1:])
        if favorite_subject not in existing_subjects:
            confirm_subject = input(
                f"'{favorite_subject}' is not in the database. Are you sure you want to add it as a new subject? (y/n): ").strip().lower()
            if confirm_subject not in ['y', 'yes']:
                continue

        club = input("\nEnter club: ").strip().capitalize()

        # Check if the club already exists in the database
        existing_clubs = set(worksheet.col_values(5)[1:])
        if club not in existing_clubs:
            confirm_club = input(
                f"'{club}' is not in the database. Are you sure you want to add it as a new club? (y/n): ").strip().lower()
            if confirm_club not in ['y', 'yes']:
                continue

        # Append student details to the Google Sheet
        worksheet.append_row([name, gender, year, favorite_subject, club])
        print("\nStudent added successfully!")

        # Ask if the user wants to add another student
        add_another = input(
            "\nDo you want to add another student? (y/n): ").strip().lower()
        if add_another not in ['y', 'yes']:
            break  # Exit the loop if the user doesn't want to add another student


# Main function that orchestrates the workflow
def main():
    CLIENT = authenticate_google_sheets()

    # Ask the user if they want to filter data
    filter_data = input("Do you want to filter data? (y/n): ").strip().lower()
    if filter_data in ['y', 'yes']:
        # User wants to filter data, proceed with filtering process
        df = get_data_from_google_sheet(CLIENT)
        total_students, favorite_subjects, club_counts = analyze_data(df)

        # Plotting data
        plot_data(df)

        # Display the results in the console
        display_results(df, total_students, favorite_subjects, club_counts)

    # Ask the user if they want to add a new student
    add_student = input(
        "\nDo you want to add a new student? (y/n): ").strip().lower()
    if add_student in ['y', 'yes']:
        add_new_student(CLIENT)


if __name__ == "__main__":
    main()
