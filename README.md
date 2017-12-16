# ECE 567 Software Engineering I

## About
The goal is to create a mobile application that is able to collect general
health information from the user and send to a remote server for analysis and
feedback.

## Server Installation
- Create a Python virtual environment
    * [Virutal Environment Guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- Install required modules
    * `pip install -r requirements.txt`
    * `sudo apt-get install python-dev libmysqlclient-dev`
- Set environment variables in "admin_app_config.py"
- Run development server
    * `python main.py 8080`
- See server options
    * `python main.py --help`

## Brief Description
- Our project is based on Android studio and the final project runnable code is under e-archive/Code/android studio.
- In this folder we have 2 files, one is apk and another is our zip source code

- The apk file can be tested and run on and android smart phone with api version 24 or higher, with google play installed

- The source_code.zip is our android studio source code, you can unzip it and open with android studio,it can be run by any emulator with api level hight than 24, but we highly recommend Nexus 5 , Nougatt api level 24with google display

- Our data is store in our remote server, we will send server detail in the email and the dataset in the folder is our previous test data

- The app can automatically fetch and execute the code while the server is on, so if you want to test the code, please email our server host,Kevin Pielacki,at kpielack@scarletmail.rutgers.edu to make sure the server is not down. or your will get some defautl value 

- Basically we do the test by passing the data from the server. Thus ,in the test part is our test documents on our server side

## Deadlines
| Item                                                | Due Date     |
|-----------------------------------------------------|--------------|
| Proposal                                            | September 17 |
| First Report (Statement of Work & Requirements)     | September 24 |
| First Report (Functional Requirements Specs & UI)   | October 1    |
| First Report (Full)                                 | October 8    |
| Second Report (Interaction Diagrams)                | October 15   |
| Second Report (Class Diagram & System Architecture) | October 22   |
| Second Report (Full)                                | October 29   |
| First Demo                                          | November 1   |
| Third Report (All Reports Collated)                 | December 10  |
| Second Demo                                         | December 13  |
| Electronic Project Archive                          | December 16  |
