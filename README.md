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

    ![Main Menu Error](images/main%20menu%20error.png)

- __Filter Data__
    - When users decide to use the Filter Data function, the terminal will first ask them to choose how they filter the data, with a list of choices. 
    - If the user does not input any of the available choices, it will come up with an error and ask them to choose again.

    ![Filter Data Error](images/filter%20data%20error.png)

    - If the user decides to filter by gender, the user will only be able to input male or female. If they enter anything else, the terminal will tell the user that no records were found. It will then ask if the user still wants to filter the data.

    ![Filter Gender Error](images/filter%20gender%20error.png)

    - If the user decides to filter by year, they will only be able to input the numbers 7-13 as this covers the Secondary School years for the UK. Once again, if they input something not in this range, the same error message will come up as previously and the user will be asked again if they still wish to filter the data.
    - If the user decides to filter by Favourite Subject or Club, the terminal will tell the user the available clubs to pick from. This is updated based on what subjects or clubs are in the Google Sheet.

    ![Filter Subject](images/filter%20subject.png)

    ![Filter Club](images/filter%20club.png)

    - Like previously, if the user does not input one of the available choices, the same error as previously will appear and they will be asked if they wish to continue filtering.
    - If when asked, the user says no, they will be taken back to the Main Menu. If they say yes, they will be asked to choose how they wish to filter the data again.
    - When the data is filtered, the terminal will return a list of students from the Google Sheet that are within the specified filter. It will also say the total number of students within the chosen category underneath the table.

    ![Filter Table with Total](images/filter%20with%20total.png)

    - The function will then terminate and the user will be taken directly back to the Main Menu.

- __Add New Student__
    - When a user decides to add a new student to the Google Sheet, they will be asked for the students name first
    - They will then be asked the student's sex and, if they do not put male or female as an input, they will be asked to enter the sex again.

