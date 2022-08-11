import csv
class Employee:
    def __init__(self, employeeName, phoneNumber, IMEI, SIM, cost_center, device_model, serviceCarrier, line_status) -> None:
        self.ename = employeeName
        self.numb = phoneNumber
        self.deviceID = IMEI
        self.card = SIM
        self.costCenter = cost_center
        self.device = device_model
        self.carrier = serviceCarrier
        self.status = line_status
    def attributes(self):
        return [self.ename, self.numb, self.status, self.deviceID, self.card, self.costCenter, self.device, self.carrier]

def verizonUpdate(filename):
    """Read input from VerizonCSV and update the Employee Data"""

    with open(filename, 'r') as INFILE:
        dataReader = csv.DictReader(INFILE)
        dict = {} # Return dict 
        dups = []
        #headers = ['Username', 'Mobile Number', 'Status', 'Device ID', 'SIM ID', 'Cost Center', 'Equipment Model', 'Carrier']
        #firstTime = True
        for item in dataReader:
            employeeNameFirstLastList = item['Username'].split()
            employeeUsername = employeeNameFirstLastList[0] + ' ' + employeeNameFirstLastList[1]
            employee = Employee(employeeUsername.strip(), item['Mobile Number'].strip(), item['Device ID'].strip(), item['SIM ID'].strip(), item['Cost Center'].strip(), item['Equipment Model'].strip(), "Verizon", item['Service Status'].strip())
            if employee.card in dict:
                dups.append(employee)
            else:
                dict.update({employee.card:employee})
        #print()
    return dups, dict


