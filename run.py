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


# Function to retrieve data from a specific Google Sheet
def get_data_from_google_sheet(CLIENT):
    spreadsheet = CLIENT.open("student_data")
    worksheet = spreadsheet.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df


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
    print("\nFavorite Subjects:")
    print(favorite_subjects)
    print("\nClub Counts:")
    print(club_counts)


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
        gender = input("Enter gender (Male/Female): ").capitalize()
        while gender not in ['Male', 'Female']:
            print("Invalid gender. Please enter 'Male' or 'Female'.")
            gender = input("Enter gender (Male/Female): ").capitalize()

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
            "Do you want to add another student? (y/n): ").lower()
        if add_another != "y":
            break  # Exit the loop if the user doesn't want to add another student


def find_students_by_year_and_club(df):
    year = input("Enter the year (7-13): ")
    while not year.isdigit() or int(year) not in range(7, 14):
        print("Invalid year. Please enter a number between 7 and 13.")
        year = input("Enter the year (7-13): ")

    # Get a list of existing clubs from the dataset
    existing_clubs = df['Club'].unique()

    club = input("Enter the club name: ")
    while club not in existing_clubs:
        print(f"Club '{club}' not found in the database.")
        print("Existing clubs:", ", ".join(existing_clubs))
        club = input("Enter an existing club name: ")

    # Filter the DataFrame based on the specified year and validated club
    filtered_students = df[(df['Year'] == int(year)) & (df['Club'] == club)]
    count = len(filtered_students)

    print(f"There are {count} students from year {year} in the '{club}' club.")

# Update the main function to include the new functionality


def main():
    CLIENT = authenticate_google_sheets()

    # Ask the user if they want to add a new student
    add_student = input("Do you want to add a new student? (y/n): ").lower()
    while add_student not in ['y', 'n']:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        add_student = input(
            "Do you want to add a new student? (y/n): ").lower()

    if add_student == "y":
        add_new_student(CLIENT)

    df = get_data_from_google_sheet(CLIENT)
    total_students, favorite_subjects, club_counts = analyze_data(df)

    # Plotting data (optional)
    plot_data(df)

    # Display the results in the console
    display_results(df, total_students, favorite_subjects, club_counts)

    # Ask the user if they want to find students by year and club
    find_students = input(
        "Do you want to find students by year and club? (y/n): ").lower()
    if find_students == "y":
        find_students_by_year_and_club(df)


if __name__ == "__main__":
    main()
