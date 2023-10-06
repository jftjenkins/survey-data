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


# Main function that orchestrates the workflow
def main():
    CLIENT = authenticate_google_sheets()
    df = get_data_from_google_sheet(CLIENT)
    total_students, favorite_subjects, club_counts = analyze_data(df)


    # Plotting data
    plot_data(df)


    # Display the results in the console
    display_results(df, total_students, favorite_subjects, club_counts)


if __name__ == "__main__":
    main()
