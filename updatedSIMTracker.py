import csv
from os import dup
from verizonUpgrade import verizonUpdate, Employee
from ATTUpgrade import ATTUpdate

def printInstructions():
    print('\n' + '_' * 180)
    print("| INSTRUCTIONS:\n| To use the following program, select any of the corrosponding numbers to the select fucntions. The following prompts will guide you through the function.\n| NOTE: Any names given to the program need to be identical to the list given by pressing '1'.")
    print('_' * 180 + '\n')

def printMenu():
    options = ["1: Print Employee Data", "2: Update Database w/ new file", "3: Change Employee Details", "4: Add Employee", "5: Remove Employee", "6: Find Employee Data"]
    print('\n' + '_' * 180)
    for option in options:
        print(f'| {option:<177} |')
    print('-' * 180)
    print('\n')

def getData(fileName):
    """Reads in database data"""
    with open(fileName, 'r') as INFILE:
        dataReader = csv.DictReader(INFILE)
        dict = {} # Return dict 
        headers = ['Username', 'Mobile Number', 'Status', 'Device ID', 'SIM ID', 'Cost Center', 'Equipment Model', 'Service Carrier']
        firstTime = True
        for item in dataReader:
            employee = Employee(item['Username'], item['Mobile Number'], item['Device ID'], item['SIM ID'], item['Cost Center'], item['Equipment Model'], item['Service Carrier'], item['Status'])
            dict.update({employee.card:employee}) #should be a dict with SIM:employee
        return headers, dict

def saveData(fileName, headers, dict):
    """Save data from program on closing"""
    #fileName[indexOfPer - 1] = '1'
    with open(fileName,'w', newline='') as OUTFILE:
        dataWriter = csv.DictWriter(OUTFILE, fieldnames=headers)
        dataWriter.writeheader()
        for key in dict.keys():
            dummyString = ""
            for i in range(len(dict[key].attributes())):
                if i != len(dict[key].attributes()) - 1:
                    dummyString += dict[key].attributes()[i] + ","
                else:
                    dummyString += dict[key].attributes()[i]

            OUTFILE.write("%s\n" % (dummyString))

def printEmployeesN(topLevel, employeeDict):
    """Prints all employees w/ their data"""
    print(f'\n{" ":>5} {topLevel[0]:<30} {topLevel[1]:<20} {topLevel[2]:<15} {topLevel[3]:<20} {topLevel[4]:<25} {topLevel[5]:<15} {topLevel[6]:<40} {topLevel[7]:<20}\n')
    count = 1
    for worker in employeeDict.values():
        #print(worker.attributes())
        print(f'{count:>4}. {worker.attributes()[0]:<30} {worker.attributes()[1]:<20} {worker.attributes()[2]:<15} {worker.attributes()[3]:<20} {worker.attributes()[4]:<25} {worker.attributes()[5]:<15} {worker.attributes()[6]:<40} {worker.attributes()[7]:<20}')
        count += 1
    print(f'Number of entries: {len(employeeDict)}')

def dup_sorter(duplist):
    """Function to find duplicate SIM ID cards in the database"""
    uh = {}
    for dup in duplist:
        if dup.card not in uh:
            uh.update({dup.card:[dup]})
        else:
            uh[dup.card].append(dup)
    
    for sim_card in uh:
        dummyString = f'{sim_card}: '
        if len(uh[sim_card]) > 1:
            for i in range(len(uh[sim_card])):
                if i == len(uh[sim_card]) - 1:
                    dummyString += uh[sim_card][i].ename + ''
                else:
                    dummyString += uh[sim_card][i].ename + ', '
            print(dummyString)

def attribute_changer(headers, employee_in_question, evers_and_sons_employees_dict):
    if employee_in_question == 'q' or employee_in_question == 'quit':
        return
    correct_employee = person_finder(headers, employee_in_question, evers_and_sons_employees_dict) # 'employee' object
    if correct_employee == None: #Employee was not found
        print("The employee you were looking for could not be found please try again\n")
        return
    attribute_to_change = int(input("What attribute do you want to change?\n1. Username\n2. Mobile Number\n3. Status\n4. Device ID\n5. SIM ID\n6. Cost Center\n7. Equipment Model\n8. Service Carrier\n>"))
    if attribute_to_change == 1:
        correcter_employee_name = input("What is the Employee's new name?: ")
        print(f'{correct_employee.ename} has been changed to {correcter_employee_name}')
        correct_employee.ename = correcter_employee_name

    elif attribute_to_change == 2:
        correcter_employee_number = input("What is the Employee's new Mobile Number?: ")
        print(f'{correct_employee.numb} has been changed to {correcter_employee_number}')
        correct_employee.numb = correcter_employee_number

    elif attribute_to_change == 3:
        status_changed = False
        while (not(status_changed)):
            correcter_employee_status = input("What is the Employee's SIM card status? 'Active' or 'Suspended': ")
            if (correcter_employee_status.find('Active') != -1) or (correcter_employee_status.find('active') != -1): 
                correct_employee.status = 'Active'
                status_changed = True
            elif (correcter_employee_status.find('Suspended') != -1) or (correcter_employee_status.find('suspended') != -1): 
                correct_employee.status = 'Suspended'
                status_changed = True
            else:
                status_changed = False
                if correcter_employee_status == 'q': return
                print("Your input was neither 'Active' or 'Suspended'. Try again or press 'q' to quit")

    elif attribute_to_change == 4:
        correcter_employee_deviceID = input("What is the Employee's new Device ID?: ")
        print(f'{correct_employee.deviceID} has been changed to {correcter_employee_deviceID}')
        correct_employee.deviceID = correcter_employee_deviceID

    elif attribute_to_change == 5:
        correcter_employee_card = input("What is the Employee's new SIM ID Number?: ")
        print(f'{correct_employee.card} has been changed to {correcter_employee_card}')
        correct_employee.card = correcter_employee_card

    elif attribute_to_change == 6:
        correcter_employee_center = input("What is the cost center?: ")
        print(f'{correct_employee.costCenter} has been changed to {correcter_employee_center}')
        correct_employee.costCenter = correcter_employee_center

    elif attribute_to_change == 7:
        correcter_employee_device = input("What is the Employee's new device model?: ")
        print(f'{correct_employee.device} has been changed to {correcter_employee_device}')
        correct_employee.device = correcter_employee_device
        
    elif attribute_to_change == 8:
        correcter_employee_carrier = input("What is the service carrier?: ")
        print(f'{correct_employee.carrier} has been changed to {correcter_employee_carrier}')
        correct_employee.carrier = correcter_employee_carrier

def person_finder(headers, employee_name, evers_and_sons_employees_dict):
    """Given a name of an employee, finds the 'employee' object associated with it. If there are more then 'employee's associated with the same name, returns the correct person."""
    employee_list = [] # This will return a list b/c there could be more then one entry of the same employee. List of employee objects
    
    for employee in evers_and_sons_employees_dict.values(): #for loop to find all relevant employees
        if employee.ename.find(employee_name) != -1: # I would be shocked if this works
            employee_list.append(employee)
    if len(employee_list) == 1:
        return employee_list[0] # if the len is 1 there should only be one thing in the list
    elif len(employee_list) > 1:
        dup_employee_dict = {}
        for employee in employee_list: dup_employee_dict.update({employee.card:employee})
        printEmployeesN(headers, dup_employee_dict)
        correct_employee = int(input("Which is the correct employee?> "))
        return employee_list[correct_employee - 1]
        # temp_string = ""
        # for i in range(len(employee_list)):
        #     if i == len(employee_list) - 1:
        #         temp_string += f'{i + 1}. {employee_list[i].ename}: {employee_list[i].card}'
        #     else:
        #         temp_string += f'{i + 1}. {employee_list[i].ename}: {employee_list[i].card} || '
    else:
        return 
    # dup_employee_dict = {}
    # for employee in evers_and_sons_employees_dict.values():
    #     if employee.ename.find(employee_name) != -1:
    #         dup_employee_dict.update({employee.card:employee})
    # if len(dup_employee_dict) == 1:
    #     return dup_employee_dict[0]
    # elif len(dup_employee_dict) > 1:
    #     printEmployeesN(headers, dup_employee_dict)
    #     correct_employee = int(input("Which is the correct employee?> "))
    #     return dup_employee_dict[correct_employee - 1]
    # else: 
    #     return


def find_SIM_card(sim_in_question, evers_and_sons_employees_dict):
    employee_with_sim_dict = {}
    for SIM in evers_and_sons_employees_dict:
         if SIM == sim_in_question:
            employee_with_sim_dict.update({SIM:evers_and_sons_employees_dict[SIM]})
    return employee_with_sim_dict
    
#--For 'Add User' ----------------------------
def newPhoneNumber(raw_number):
    try:
        if (raw_number[3] == '.') and (raw_number[7] == '.') and (len(raw_number) == 12):
            return raw_number
        elif (len(raw_number) == 10):
            return raw_number[:3] + '.' + raw_number[3:6] + '.' + raw_number[6:]
    except:
        print("The inputed formate of the Phone Number was not correct. It was potentially to long or short, not in formate XXX.YYY.ZZZZ or XXXYYYZZZZ. Please try again.")
        return

def newIMEINumber(raw_IMEI):
    try:
        if (len(raw_IMEI) == 15) and (raw_IMEI.isnumeric()):
            return raw_IMEI
    except:
        print("IMEI is not the right formate. Please use all numbers and ensure that the number is 15 characters long. Please try again.")
        return

def newSIMNumber(raw_SIM):
    try:
        if (len(raw_SIM) == 20) and (raw_SIM.isnumeric()):
            return raw_SIM
    except:
        print("SIM ID is not the right formate. Please use all numbers and ensure that the number is 20 characters long. Please try again.")
        return

def newCostCenter(raw_center):
    try:
        if (len(raw_center) == 4) and (raw_center.isnumeric):
            return raw_center
    except:
        print("Cost Center wrong formate.")
        return
#---------------------------------------------

def list_strip(list_to_strip):
    for value in list_to_strip:
        value = value.strip()
    return list_to_strip

def sim_or_person_checker(sim_or_person_list):
    try:
        if sim_or_person_list[1]:
            return False
    except:
        return True

def menu(userIn, headers, evers_and_sons_employees_dict):
    printInstructions()
    while (userIn != 'q') and (userIn != 'quit'):
        printMenu()
        userIn = input("What do you want to do?: ")

        if userIn == '1': # Print Employees
            if '' in evers_and_sons_employees_dict:
                evers_and_sons_employees_dict.pop('')
            printEmployeesN(headers, evers_and_sons_employees_dict)

        elif userIn == '2': # File update
            good_carrier = False
            while(not(good_carrier)): # Checks to see if the input is correct.
                carrierFile = input("\nWhat carrier did the file come from? What is the name of the file?\nNote: 'AT&T' and 'Verizon' are accepted. Add a ',' between carrier and file_name. File name must one word and exact.\n>").split(',')
                for i in range(len(carrierFile)):
                    carrierFile[i] = carrierFile[i].strip()
                if carrierFile[0] == 'Verizon': #Verizon section
                    dups, carrierData = verizonUpdate(carrierFile[1])
                    good_carrier = True
                elif (carrierFile[0] == 'AT&T'): # AT&T Section
                    dups, carrierData = ATTUpdate(carrierFile[1])
                    good_carrier = True
                elif (carrierFile[0] == 'q' or carrierFile[0] == 'quit'):
                    print("Leaving 'File Update'.")
                    break
                else:
                    print(f'First entry was not "AT&T" or "Verizon". To leave File Update, press q or quit. Please try again.')
                    continue
            #dups, carrierData = verizonUpdate(carrierFile[1]) if carrierFile[0] == 'Verizon' else dups, carrierData = ATTUpdate(carrierFile[1])
            if not(good_carrier):
                continue
            dup_sorter(dups)
            for sim_card in carrierData:
                employee_attributes = carrierData[sim_card].attributes()
                if sim_card in evers_and_sons_employees_dict and (evers_and_sons_employees_dict[sim_card].ename == carrierData[sim_card].ename):
                    print('Match Found')
                    change_made = False
                    for i in range(len(employee_attributes)):
                        if employee_attributes[i] != evers_and_sons_employees_dict[sim_card].attributes()[i]:
                            change_made = True
                            print(f'{carrierData[sim_card].ename} attribute: {employee_attributes[i]} was not in database.\nUpdating now')
                            employee_attributes[i] = evers_and_sons_employees_dict[sim_card].attributes()[i]
                    if change_made:
                        print("Employee has been updated to the correct data.")
                else: 
                    print(f'Owner of {sim_card} was not in the system.\nAdding now.')
                    evers_and_sons_employees_dict.update({sim_card:carrierData[sim_card]})

        elif userIn == '3': # Change Attributes
            employee_in_question = ''
            while (employee_in_question != 'q' and employee_in_question != 'quit'):
                employee_in_question = input("\nWhat is the name of the employee you wish to edit? Press 'q' or 'quit' to leave the selection at any time. \nNote: the name of the employee must be identical to what is in the data base. > ")
                attribute_changer(headers, employee_in_question, evers_and_sons_employees_dict)

        elif userIn == '4': # Manuel Add User
            new_employee_attributes = []
            new_employee_In = ""
            count = 0
            while (new_employee_In != 'q') and (new_employee_In != 'quit') and (count < 8):
                if count == 0: # Entering new Employee Name
                    new_employee_In = input("\nWhat is the new employee's name? To quit this selection, 'q' or 'quit' > ")
                    if (new_employee_In == 'q') or (new_employee_In =='quit'):
                        continue
                    correct = input(f'The new employees name is: {new_employee_In} is this correct?\nNote: y or yes, n or no are acceptable inputs. > ' )
                    if correct == 'y' or correct == 'yes':
                        new_employee_attributes.append(new_employee_In)
                        count += 1
                    elif correct == 'n' or correct == 'no':
                        continue
                    else:
                        print(f'You have entered {correct} which is not of correct formate. Please try again.')
                elif count == 1: # Entering Phone Number
                    new_employee_In = input("\nWhat is the new employee number\nNote: Correct formate is XXX.YYY.ZZZZ or XXXYYYZZZZ > ")
                    if new_employee_In == 'q' or new_employee_In == 'quit':
                        continue
                    newEmployeeNumber = newPhoneNumber(new_employee_In)
                    if newEmployeeNumber != None:
                        new_employee_attributes.append(newEmployeeNumber)
                        count += 1
                    else:
                        #print(f'{newEmployeeNumber} was of the wrong formate, please try again.')
                        continue
                elif count == 2: # IMEI Number
                    new_employee_In = input("\nWhat is the IMEI of the device?\nNote: IMEI numbers are 15 numbers long > ")
                    if new_employee_In == 'q' or new_employee_In == 'quit':
                        continue
                    newEmployeeIMEI = newIMEINumber(new_employee_In)
                    if newEmployeeIMEI != None:
                        new_employee_attributes.append(newEmployeeIMEI)
                        count += 1
                    else:
                        continue
                elif count == 3: # Enter SIM ID card
                    new_employee_In = input("\nWhat is the SIM card ID?\nNote: SIM ID Cards are 20 numbers long. > ")
                    if new_employee_In == 'q' or new_employee_In == 'quit':
                        continue
                    newEmployeeSIM = newSIMNumber(new_employee_In)
                    if newEmployeeSIM != None:
                        new_employee_attributes.append(newEmployeeSIM)
                        count += 1
                    else:
                        continue
                elif count == 4: # Enter Cost Center 
                    new_employee_In = input("\nWhat is the Cost Center?\nNote: 4 numbers long> ")
                    if new_employee_In == 'q' or new_employee_In == 'quit':
                        continue
                    newEmployeeCenter = newCostCenter(new_employee_In)
                    if newEmployeeCenter != None:
                        new_employee_attributes.append(newEmployeeCenter)
                        count += 1
                    else:
                        continue
                elif count == 5: # Employee's Device
                    new_employee_In = input("\nWhat is the new employee's device? To quit this selection, 'q' or 'quit' > ")
                    if (new_employee_In == 'q') or (new_employee_In =='quit'):
                        continue
                    correct = input(f'The new employees Device is: "{new_employee_In}" is this correct?\nNote: y or yes, n or no are acceptable inputs. > ' )
                    if correct == 'y' or correct == 'yes':
                        new_employee_attributes.append(new_employee_In)
                        count += 1
                    elif correct == 'n' or correct == 'no':
                        continue
                    else:
                        print(f'You have entered {correct} which is not of correct formate. Please try again.')
                elif count == 6: # Line Carrier
                    new_employee_In = input("\nWhat is the new employee's carrier? AT&T or Verizon? To quit this selection, 'q' or 'quit' > ")
                    if (new_employee_In == 'q') or (new_employee_In =='quit'):
                        continue
                    elif new_employee_In != "AT&T" and new_employee_In != "Verizon":
                        print(f'"{new_employee_In}" is not "AT&T" or "Verizon" please try again.')
                        continue
                    else:
                        new_employee_attributes.append(new_employee_In)
                        count += 1
                elif count == 7: # Line status
                    new_employee_In = input("\nWhat is the status of the line? To quit this selection, 'q' or 'quit' > ")
                    if (new_employee_In == 'q') or (new_employee_In =='quit'):
                        continue
                    elif new_employee_In != "Active" and new_employee_In != "Suspended":
                        print(f'"{new_employee_In}" is not "Active" or "Suspended" please try again.')
                        continue
                    else:
                        new_employee_attributes.append(new_employee_In)
                        count += 1
            if len(new_employee_attributes) == 8:
                newEmployee = Employee(
                    new_employee_attributes[0], 
                    new_employee_attributes[1], 
                    new_employee_attributes[2], 
                    new_employee_attributes[3], 
                    new_employee_attributes[4], 
                    new_employee_attributes[5], 
                    new_employee_attributes[6], 
                    new_employee_attributes[7]
                )
                evers_and_sons_employees_dict.update({newEmployee.card:newEmployee})
            else:
                new_employee_attributes = []
                print("Employee was not addded. Please try again.")
 
        elif userIn == '5': # Manuel Remove User
            sim_or_person = input("Do you have the 'SIM' ID or 'Person'? What is the number or name?\nNote: SIM ID's and names must be exact. Add a space between the two inputs\n>").strip().split(',')
            if sim_or_person[0] == 'SIM':
                dict_with_sim = find_SIM_card(sim_or_person[1], evers_and_sons_employees_dict)
                if len(dict_with_sim) == 0:
                    print(f'No person with SIM {sim_or_person[1]} in the database.')
                elif len(dict_with_sim) == 1:
                    try:
                        print(f'{sim_or_person[1]} deleted.')
                        evers_and_sons_employees_dict.pop(sim_or_person[1])
                    except:
                        print("Could not find then SIM.")
                else:
                    printEmployeesN(headers, dict_with_sim)
                    which_employee = input("Who is to be removed?")
                    try:
                        print(f'{dict_with_sim[which_employee]} was deleted')
                        evers_and_sons_employees_dict.pop(dict_with_sim[which_employee])
                    except:
                        print("Could not delete the individual.")
            elif sim_or_person[0] == 'Person':
                emplo = person_finder(headers, sim_or_person[1],evers_and_sons_employees_dict)
                if emplo == None:
                    print("Could not find person. Please try again.")
                else:
                    try:
                        print(f'{emplo.ename} has been removed from the database.')
                        evers_and_sons_employees_dict.pop(emplo.card)
                    except:
                        print("Could not find person. Please try again.")                    

        elif userIn == '6': # Find owners of SIM Card X
            sim_or_person = list_strip(input("Do you have the 'SIM' ID or 'Person'? What is the number or name?\nNote: SIM ID's and names must be exact. Add a ',' between the two inputs\n>").split(','))
           
            bad = sim_or_person_checker(sim_or_person)
            while(bad):
                sim_or_person = list_strip(input("Do you have the 'SIM' ID or 'Person'? What is the number or name?\nNote: SIM ID's and names must be exact. Add a ',' between the two inputs\n>").split(','))
                bad = sim_or_person_checker(sim_or_person)
                
            if sim_or_person[0] == 'SIM':
                dict_with_sim = find_SIM_card(sim_or_person[1], evers_and_sons_employees_dict)
                if len(dict_with_sim) == 0:
                    print(f'No person with SIM {sim_or_person[1]} in the database.')
                elif len(dict_with_sim) == 1:
                    try:
                        printEmployeesN(headers, dict_with_sim)
                        #evers_and_sons_employees_dict.pop(sim_or_person[1])
                    except:
                        print("Could not find then SIM.")
                else:
                    printEmployeesN(headers, dict_with_sim)
                    which_employee = input("Which is the correct employee? > ")
                    try:
                        printEmployeesN(headers, dict_with_sim[which_employee])
                        #evers_and_sons_employees_dict.pop(dict_with_sim[which_employee])
                    except:
                        print("Could not delete the individual.")
            elif sim_or_person[0] == 'Person':
                emplo = person_finder(headers, sim_or_person[1],evers_and_sons_employees_dict)
                if emplo == None:
                    print("Could not find person. Please try again.")
                else:
                    try:
                        printEmployeesN(headers, {emplo.card:emplo})
                        #evers_and_sons_employees_dict.pop(emplo.card)
                    except:
                        print("Could not find person. Please try again.") 

    saveData("newDatabase.csv", headers, evers_and_sons_employees_dict)

def main():
    headers, evers_and_sons_employees_dict = getData("newDatabase.csv")
    userIn = ""
    menu(userIn, headers, evers_and_sons_employees_dict)  

if __name__ == "__main__":
    main()


# elif userIn == '3': # AT&T updates
#     ATTFile = input('What is the name of the file?: ').strip()
#     dups, ATTData = ATTUpdate(ATTFile)
#     #print(ATTData)
#     dup_sorter(dups)

#     for sim_card in ATTData:
#         employee_attributes = ATTData[sim_card].attributes()
#         if (sim_card in evers_and_sons_employees_dict) and (evers_and_sons_employees_dict[sim_card].ename == ATTData[sim_card].ename):
#             change_made = False
#             for i in range(len(employee_attributes)):
#                 if employee_attributes[i] != evers_and_sons_employees_dict[sim_card].attributes()[i]:
#                     change_made = True
#                     print(f'{ATTData[sim_card].ename} attribute: {employee_attributes[i]} was not in database.\nUpdating now')
#                     employee_attributes[i] = evers_and_sons_employees_dict[sim_card].attributes()[i]
#             if change_made:
#                 print("Employee has been updated to the correct data.")
#         else: 
#             print(f'Owner of {sim_card} was not in the system.\nAdding now.')
#             evers_and_sons_employees_dict.update({sim_card:ATTData[sim_card]})