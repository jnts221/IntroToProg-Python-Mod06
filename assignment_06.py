# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   Sohail Nassiri,09/02/2024,Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "enrollments.json"  # Set the json file name

# Define the Data Variables
students: list = []  # Table of student data
menu_choice: str  # Hold the choice made by the user


# Processing --------------------------------------- #
class FileProcessor:
    """
        A collection of processing layer functions that work with json files

    ChangeLog: (Who, When, What)
    Sohail Nassiri,09.02.2024,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file into a list of dictionary rows

        Note:
        - Data sent to the student_data parameter will be overwritten.

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.02.2024,Created function

        :param file_name: string with the name of the file we are reading
        :param student_data: list of dictionary rows we are adding data to
        :return: list of dictionary rows filled with data
        """

        try:
            file = open(file_name, "r")  # Reads file
            student_data = json.load(file)  # Parses into a list of dictionaries
            file.close()
        except FileNotFoundError as e:  # Raises exception if file is not found
            # Sending error messages to a function in IO
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:  # Raises any other general exception that is not specifically called out
            IO.output_error_messages("There was a non-specific error when reading the file!", e)
        finally:
            if file:
                file.close()  # Closes file regardless of whether code successfully executes or not
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file from a list of dictionary rows

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.02.2024,Created function

        :param file_name: string with the name of the file we are writing to
        :param student_data: list of dictionary rows we have in our data
        :return: None
        """
        try:
            file = open(file_name, "w")  # Reads file
            json.dump(student_data, file)  # Writes the table list to the JSON file
            file.close()
            IO.output_student_courses(student_data=student_data)  # Sending output to a function in IO
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file:
                file.close()


class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    Sohail Nassiri,09.02.2024,Created Class, Added menu input/output functions, displaying of data, and custom error
    messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error messages to the user

          Note: Allows to customize error messages in one place and affect all error handling

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.02.2024,Created function and toggling technical message off if no exception object is passed

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of option to the user

        :return: None
        """
        print(menu, end='\n\n')  # Adding extra space to make it look cleaner

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("You must choose 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing the exception object to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current data to the user

        :return: None
        """
        print("-" * 50)
        for student in student_data:  # Iterates through each row of table
            print(
                f"Student {student["FirstName"]} {student["LastName"]} is enrolled in {student["CourseName"]}")
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets data from the user and adds it to a list of dictionary rows

        :param student_data: list of dictionary rows containing our current data
        :return: list of dictionary rows filled with a new row of data
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():  # Requires user to input alphabetical name
                raise ValueError("The first name should not contain numbers.")  # Raises error is non-alphabetical
            #  character is entered
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student_data.append({"FirstName": student_first_name, "LastName": student_last_name,
                                 "CourseName": course_name})  # Table is appended with data from list of dictionary row
            print(
                f"You have registered {student_first_name} {student_last_name} for {course_name}.")  # Displays
            #  input registration
        except ValueError as e:
            IO.output_error_messages("Only use names without numbers", e)  # Prints the custom message
        except Exception as e:
            IO.output_error_messages("There was a non-specific error when adding data!", e)
        return student_data


#  End of class definitions

# Beginning of the main body of this script

# When the program starts, reads the file data into a table and extracts the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

#  Repeat the follow tasks
while True:
    IO.output_menu(menu=MENU)  # Present menu choices
    menu_choice: str = IO.input_menu_choice()

    if menu_choice == "1":  # Input data and display data entered
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":  # Get new data and display the change
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":  # Write and save data to file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":  # End program
        break  # Out of the while loop

print("Program Ended")
