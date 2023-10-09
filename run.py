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
            "Enter column name (Gender, Year, Favourite Subject, or Club): ").strip().title()
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
    print("Survey Data:")
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
        # Get student details from the user
        name = input("Enter student name: ")
        gender = input("Enter gender (Male/Female or M/F): ").capitalize()

        while gender not in ['Male', 'M', 'Female', 'F']:
            print("Invalid gender. Please enter 'Male', 'M', 'Female', or 'F'.")
            gender = input("Enter gender (Male/Female or M/F): ").capitalize()

        year = input("Enter student's year (7-13): ")
        while not year.isdigit() or int(year) not in range(7, 14):
            print("Invalid year. Please enter a number between 7 and 13.")
            year = input("Enter student's year (7-13): ")

        favorite_subject = input("Enter favorite subject: ")
        club = input("Enter club: ")

        # Append student details to the Google Sheet
        worksheet.append_row([name, gender, year, favorite_subject, club])
        print("Student added successfully!")

        # Ask if the user wants to add another student
        add_another = input(
            "Do you want to add another student? (y/n): ").strip().lower()
        while add_another not in ['y', 'n', 'yes', 'no']:
            print("Invalid input. Please enter 'y' or 'n' (or 'yes' or 'no').")
            add_another = input(
                "Do you want to add another student? (y/n): ").strip().lower()

        if add_another in ['n', 'no']:
            break  # Exit the loop if the user doesn't want to add another student


# Function to find students by year and club
def find_students_by_year_and_club(df):
    while True:
        year = input("Enter the year (7-13): ")
        if year.isdigit() and int(year) in range(7, 14):
            break
        else:
            print("Invalid year. Please enter a number between 7 and 13.")

    # Get a list of existing clubs from the dataset
    existing_clubs = df['Club'].unique()

    while True:
        club = input("Enter the club name: ").capitalize()
        if club in existing_clubs:
            break
        else:
            print(f"Club '{club}' not found in the database.")
            print("Existing clubs:", ", ".join(existing_clubs))

    # Filter the DataFrame based on the specified year and validated club
    filtered_students = df[(df['Year'] == int(year)) & (
        df['Club'].str.capitalize() == club)]
    count = len(filtered_students)

    print(f"There are {count} students from year {year} in the '{club}' club.")


# Update the main function to include the new functionality
def main():
    CLIENT = authenticate_google_sheets()

    df = get_data_from_google_sheet(CLIENT)
    total_students, favorite_subjects, club_counts = analyze_data(df)

    # Plotting data (optional)
    plot_data(df)

    # Display the results in the console
    display_results(df, total_students, favorite_subjects, club_counts)

    # Ask the user if they want to add a new student
    add_student = input(
        "\nDo you want to add a new student? (y/n): ").strip().lower()
    while add_student not in ['y', 'n', 'yes', 'no']:
        print("Invalid input. Please enter 'y' or 'n' (or 'yes' or 'no').")
        add_student = input(
            "Do you want to add a new student? (y/n): ").strip().lower()

    if add_student in ['y', 'yes']:
        add_new_student(CLIENT)

    # Ask the user if they want to find students by year and club
    find_students = input(
        "\nDo you want to find students by year and club? (y/n): ").strip().lower()
    while find_students not in ['y', 'n', 'yes', 'no']:
        print("Invalid input. Please enter 'y' or 'n' (or 'yes' or 'no').")
        find_students = input(
            "Do you want to find students by year and club? (y/n): ").strip().lower()

    if find_students in ['y', 'yes']:
        find_students_by_year_and_club(df)


if __name__ == "__main__":
    main()
