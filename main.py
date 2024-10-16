import os
import csv

def make_directory():
    # Function to make the lists/ directory if it doesn't already exist
    try:
        os.mkdir("lists")
    except FileExistsError:
        pass


def make_file(filepath):
    # Function to initially make the file
    try:
        with open(f"lists/{filepath}.csv", 'x',newline="") as csvfile:
            fieldnames = ['name','priority','completed']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
    except FileExistsError:
        print("List with same name already created, try again.")


def save_to_file(filepath, name, priority, completed):
    # Function used to add a task to the csv file
    try:
        with open(f"lists/{filepath}.csv", mode='a', newline='') as csvfile:
            fieldnames = ['name', 'priority', 'completed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'name': name, 'priority': priority, 'completed': str(completed)})
    except Exception as e:
        print(f"Error: {e}")


def complete(filepath, target):
    # Function used to make completion true in the csv file
    filepath = f"{filepath}.csv"
    temppath = f"temp_{filepath}"
    with open(f"lists/{filepath}", mode='r', newline="") as csv_read, open(f"lists/{temppath}", mode='w', newline="") as csv_write:
        fieldnames = ['name', 'priority', 'completed']
        writer = csv.DictWriter(csv_write, fieldnames=fieldnames)
        reader = csv.DictReader(csv_read)
        writer.writeheader()
        for row in reader:
            if row['name'] != target:
                writer.writerow(row)
            else:
                row["completed"] = "True"
                writer.writerow(row)
    os.replace(f"lists/{temppath}", f"lists/{filepath}")


def delete(filepath,target):
    # Function used to delete a task
    filepath = f"{filepath}.csv"
    temppath = f"temp_{filepath}"
    with open("lists/"+filepath, mode='r', newline="") as csvfile, open("lists/"+temppath, mode='w', newline="") as temp_csv:
        fieldnames = ['name', 'priority', 'completed']
        writer = csv.DictWriter(temp_csv, fieldnames=fieldnames)
        reader = csv.DictReader(csvfile)
        writer.writeheader()
        for row in reader:
            if row['name'] != target:
                writer.writerow(row)
    os.replace(f"lists/{temppath}", f"lists/{filepath}")


def print_list(filepath):
    # Function to print the to-do list
    print(f"\n----------{filepath}----------\n")
    print(f"{"Name of entry":<35}{"Priority":<35}Completed")
    with open(f"lists/{filepath}.csv", mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['completed'] == 'True':
                row['completed'] = '✅'
            else:
                row['completed'] = '❌'
            print(f"{row['name']:<35} {row['priority']:<35} {row['completed']}")


def delete_if_empty(filepath):
    # Function to delete the list if it is empty
    with open(f"lists/{filepath}.csv", mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    if len(rows) == 0:
        print("\nThere are no entries in this list remaining, the list will now be deleted.")
        os.remove(f"lists/{filepath}.csv")

# Main program logic

print("\n---TO-DO LIST---\n")
print("Would you like to:\nMake a new To-Do List (A)\nView a To-Do List (B)\nDelete an existing list (C)")
option = input("").upper()

while option not in ["A", "B", "C"]:
    option = input("").upper()

make_directory()
if option == "A":
    print("\nEnter the name of the to-do list: ")
    listname = input()
    make_file(listname)
    while True:
        stateCheck = input("\nAdd a new to-do entry (Y/N): ").upper()
        while stateCheck not in ["Y", "N"]:
            stateCheck = input("Please enter either Y or N: ")

        if stateCheck == "Y":
            nameInput = input("\nEnter the name of the to-do list task: ")
            priorityInput = input("Enter the priority of the to-do list task: ")
            completedInput = "False"
            save_to_file(listname, nameInput, priorityInput, completedInput)
        else:
            break
    print_list(listname)
    while True:
        print("\nActions:\nExit / Check as done / Delete entry")
        multiChoice = input()
        while multiChoice not in ["Exit", "Check as done", "Delete entry"]:
            multiChoice = input("Please only choose from the three actions: ")
        if multiChoice == "Check as done":
            print("Input the name of the task that is completed:")
            completeInput = input()
            complete(listname, completeInput)
            print_list(listname)
        if multiChoice == "Delete entry":
            print("Input the name of the task that you want to delete:")
            deleteInput = input()
            delete(listname, deleteInput)
            delete_if_empty(listname)
            if os.path.exists(f"lists/{listname}.csv"):
                print_list(listname)
        if multiChoice == "Exit":
            break
elif option == "B":
    print("\nEnter the name of the to-do list you want to read and change: ")
    viewChoice = input()
    try:
        print_list(viewChoice)
    except FileNotFoundError:
        print("File not found.")
    while True:
        print("\nActions:\nExit / Check as done / Delete entry")
        multiChoice = input()
        while multiChoice not in ["Exit", "Check as done", "Delete entry"]:
            multiChoice = input("Please only choose from the three actions: ")
        if multiChoice == "Check as done":
            print("Input the name of the task that is completed:")
            completeInput = input()
            complete(viewChoice, completeInput)
            print_list(viewChoice)
        if multiChoice == "Delete entry":
            print("Input the name of the task that you want to delete:")
            deleteInput = input()
            delete(viewChoice, deleteInput)
            delete_if_empty(viewChoice)
            if os.path.exists(f"lists/{viewChoice}.csv"):
                print_list(viewChoice)
        if multiChoice == "Exit":
            break
elif option == "C":
    print("\nEnter the name of the to-do list you want to delete: ")
    delInput = input()
    try:
        os.remove(f"lists/{delInput}.csv")
    except FileNotFoundError:
        print("File not found.")