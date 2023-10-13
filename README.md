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

- __Filter Data__
    - 
