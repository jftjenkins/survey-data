import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt


# Function to authenticate with Google Sheets API
def authenticate_google_sheets():
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
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
   
    # Get student details from the user
    name = input("Enter student name: ")
    gender = input("Enter gender: ")
    year = input("Enter student's year: ")
    favorite_subject = input("Enter favorite subject: ")
    club = input("Enter club: ")
   
    # Append student details to the Google Sheet
    worksheet.append_row([name, gender, year, favorite_subject, club])
    print("Student added successfully!")


# Main function that orchestrates the workflow
def main():
    CLIENT = authenticate_google_sheets()


    # Ask the user if they want to add a new student
    add_student = input("Do you want to add a new student? (y/n): ").lower()
    while add_student not in ['y', 'n']:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        add_student = input("Do you want to add a new student? (y/n): ").lower()

    if add_student == "y":
        add_new_student(CLIENT)
    

    df = get_data_from_google_sheet(CLIENT)
    total_students, favorite_subjects, club_counts = analyze_data(df)


    # Plotting data
    plot_data(df)


    # Display the results in the console
    display_results(df, total_students, favorite_subjects, club_counts)


if __name__ == "__main__":
    main()
