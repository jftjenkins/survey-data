# Student Data Analysis

Student Data Analysis is a python data analysis service that runs in the Code Institute mock terminal on heroku. 
This has been specifically built for admin at secondary schools so that they may easily find data about students, such as lists of students in certain clubs.
Users are also able to quickly add new students to the Google Sheet through the use of the python terminal.

A live link to the Student Data Analysis can be found [here](https://student-data-analysis-0ebe99e84522.herokuapp.com/)

A live link to the Student Data Google Sheet can be found [here](https://docs.google.com/spreadsheets/d/1OTNuh06X-GHCG1R-ZOdrq5prXCNZEzCgLlbxohJGBJM/edit?usp=sharing)

![Main Menu](images/main%20menu.png)

## Technologies Used

### Libraries

- os
- gspread
- oauth2client.service_account
- pandas
- pyfiglet

## Features

### Existing Features

- __Main Menu__

    - When first booted up, the first thing that appears is the Main Menu. The style of font seen is achieved using the <b>pyfiglet</b> plugin.
    - From the Main Menu, users can navigate either to the Filter section of the code, or to the Add New Student section. There is also the option to quit the code.
    - This is all achieved by simply typing in 1, 2, or 3 in the terminal.
    - Whenever a process is finished (as long as it is not the Exit process), it will return to the Main Menu so users do not have to reset the terminal after every use.
    - If users type in anything but 1, 2, or 3, the terminal will tell them that they have inputted an "invalid choice" and will tell them they can only input 1, 2, or 3.

    ![Main Menu Error](images/main%20menu%20invalid%20choice.png)

- __Filter Data__

    - When users decide to use the Filter Data function, the terminal will first ask them to choose how they filter the data, with a list of choices. 
    - If the user does not input any of the available choices, it will come up with an error and ask them to choose again.

    ![Filter Data Error](images/invalid%20column%20name.png)

    - If the user decides to filter by sex, the user will only be able to input male or female. If they enter anything else, the terminal will tell the user that no records were found. It will then ask if the user still wants to filter the data.

    ![Filter Sex Error](images/invalid%20sex%20error.png)

    - If the user decides to filter by year, they will only be able to input the numbers 7-13 as this covers the Secondary School years for the UK. Once again, if they input something not in this range, the same error message will come up as previously and the user will be asked again if they still wish to filter the data.
    - If the user decides to filter by Favourite Subject or Club, the terminal will tell the user the available clubs to pick from. This is updated based on what subjects or clubs are in the Google Sheet.

    ![Filter Subject](images/favourite%20subjects%20filter.png)

    ![Filter Club](images/club%20filter.png)

    - Like previously, if the user does not input one of the available choices, the same error as previously will appear and they will be asked if they wish to continue filtering.
    - If when asked, the user says no, they will be taken back to the Main Menu. If they say yes, they will be asked to choose how they wish to filter the data again.
    - When the data is filtered, the terminal will return a list of students from the Google Sheet that are within the specified filter. It will also say the total number of students within the chosen category underneath the table.

    ![Filter Table with Total](images/filter%20with%20total.png)

    - The function will then terminate and the user will be taken directly back to the Main Menu.

- __Add New Student__

    - When a user decides to add a new student to the Google Sheet, they will be asked for the students name first
    - They will then be asked the student's sex and, if they do not put male or female as an input, they will be asked to enter the sex again.

    ![Add Student Sex Error](images/new%20student%20invalid%20sex.png)

    - The user will then be asked to enter the student's year from 7-13. Once again, if they do not make a valid input, they will be told that the input has to be a number between 7 and 13, and will be asked to input the student's year again.
    - The user will be asked for the student's favourite subject. If the user enters a subject that does not already exist in the database, they will be asked to confirm that they wish to add a new subject.

    ![Add Student with New Subject](images/add%20student%20new%20subject.png)

    - This has also been implemented for when the user has to add the student's club. If the subject/club already exists, this message will not appear.
    - This has been implemented so that users are sure they are putting the right information in, and have not possibly made a typo.
    - Once this is complete, the terminal will ask the user if they wish to add another student. If they say yes, the process will begin again. If they say no, the function will take them back to the Main Menu.

    ![Add New Student Full Example](images/add%20new%20student%20full.png)

    - This new student will now appear at the bottom of the Google Sheet document

    ![Original Google Sheet](images/google%20sheet%20original.png)

    ![Updated Google Sheet](images/google%20sheet%20updated.png)

- __Future Features__

    - Allow users to filter data by more than one variable eg. Student's that have Maths as a Favourite Subject AND are in Drama Club
    - Implement some way for filtered data to be displayed graphically as well, perhaps using <b>matplotlib</b>
    - Implement some sort of user authentication into the Python code so that only those with valid username and passwords are able to access the data
    - Implement a feature that allows users to edit or delete already existing student data

## Deployment

This code was deployed using Code Institute's mcok terminal for Heroku.

- __Steps for deployment:__
    - Fork or clone this repository
    - Create a new Heroku app
    - Set the buildbacks to <b>Python</b> and <b>NodeJS</b> in that order
    - Link the Heroku app to the repository
    - Click on <b>Deploy</b>
    - Make sure [this Google Sheet](ttps://docs.google.com/spreadsheets/d/1OTNuh06X-GHCG1R-ZOdrq5prXCNZEzCgLlbxohJGBJM/edit?usp=sharing) is open to display the already existing data, and any data you add through the use of the terminal.

## Testing

I have manually tested the code by doing the following:
    
- Passed the code through the [CI Python Linter](https://pep8ci.herokuapp.com/) and confirmed there were no problems/errors

![Code Authenticator](images/code%20authenticator.png)

- Gave the code different invalid inputs at different points in the program to make sure correct responses were created by the code.
- Tested the code both in the local terminal provided within CodeAnywhere, and within the CI Heroku Terminal

### Bugs

- __Solved Bugs__

    - Duplicated Entries: When adding a new student with a favorite subject or club that did not exist in the database, the script allowed the addition but resulted in duplicated entries for the same subject or club. To fix this, a check was added to verify if the subject or club already existed in the database. If it did not exist, the script prompted the user for confirmation before adding it as a new subject or club. This check ensured that duplicate entries were avoided.
    - Data Overwriting: There were instances where existing student data was being overwritten, especially related to favorite subjects and clubs. This occurred when new subjects or clubs were added, potentially impacting existing records. The overwriting issue was resolved by refining the logic for adding new subjects and clubs.
    - Filtering Issue: There was an issue with displaying the total number of students when filtering data. The total count of students wasn't being printed to the console during the filtering process. The issue with displaying the total number of students during filtering was fixed by modifying the analyze_data function. The function was updated to include a print statement that outputs the total number of students in the filtered dataset, ensuring that the total count is displayed to the user.

- __Remaining Bugs__

    - No bugs remaining

- __Validator Test__

    - [PEP8](https://pep8ci.herokuapp.com/)
        - No errors were returned from pep8ci.herokuapp.com/

## Credits

### Code

The following sources were used for this project:
- [Example Spreadsheet](https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit?usp=sharing)
- Python Essentials from [Code Institute](https://codeinstitute.net/)
- [Gspread](https://docs.gspread.org/en/v5.10.0/)
- [black](https://pypi.org/project/black/)
- [Matplotlib](https://matplotlib.org/)
- [W3 Schools](https://www.w3schools.com/python/matplotlib_pyplot.asp)
- [freeCodeCamp](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/)

### Achnowledgements

- The Slack community, particularly Lucimeri Andretta, who helped me with the layout of this README file
- My Mentor Sandeep Aggarwal for continuours feedback during the project and helping envision my ideas


- - -

Developed by Joseph Jenkins for Code Institute's Project 3. Feel free to connect with me on my [LinkedIn](www.linkedin.com/in/joseph-jenkins-baille-637a55205)