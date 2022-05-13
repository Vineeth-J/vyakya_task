import json
import re
import xlsxwriter

phone_numbers = []
data = []
website = []
email = []
numbers = []
Withdrawals = []
Deposits = []

with open('task_input_list.json') as json_file:
    data = json.load(json_file)
    
for i in data:
    match_object = re.search("\.com$", i)    
    if match_object != None:
        website.append(match_object.string)
        pass
    
    match_object = re.search("[\d]{1}-[\d]{3}-[\d]{3}-[\d]{3}",i)
    if match_object != None:
        start, end = match_object.span()
        phone_numbers.append(i[start:end])
        pass   
     
    match_object = re.search("\([\d]{3}\) [\d]{3}-[\d]{3}",i)
    if match_object != None:
        start, end = match_object.span()
        phone_numbers.append(i[start:end])
        pass
    
    match_object = re.search('\S+@\S+\.[a-zA-Z]+', i)
    if match_object != None:
        email.append(match_object.string)
        pass     
    
for i in data:
    match_object = re.search('(^-[\d]+,[\d]+\.[\d]+)|(^-[\d]+\.[\d]+)', i)
    if match_object != None:
        index = data.index(i)
        match_date = re.search('[\d]{2}\/[\d]{2}\/[\d]{2}', data[index-2])
        match_des = re.search('[a-zA-Z ]+',data[index-1])
        match_date1 = re.search('[\d]{2}\/[\d]{2}\/[\d]{2}', data[index-4])
        match_des1 = re.search('.\/.',data[index-1])
        if (match_date != None or match_date1 != None) and match_des != None and match_des1 == None:
            numbers.append(float(match_object.string.replace(",","")))
        
        if match_date != None and match_des != None and match_des1 == None:
            Withdrawals.append(list([data[index-2],data[index-1],data[index]]))
        if match_date1 != None and match_des != None and match_des1 == None:
            Withdrawals.append(list([data[index-4],data[index-3]+" "+data[index-2]+" "+data[index-1],data[index]]))

for i in data:
    match_object = re.search('(^[\d]+,[\d]+\.[\d]+)|(^[\d]+\.[\d]+)', i)
    if match_object != None:
        index = data.index(i)
        match_date = re.search('[\d]{2}\/[\d]{2}\/[\d]{2}', data[index-2])
        match_des = re.search('[a-zA-Z ]+',data[index-1])
        match_date1 = re.search('[\d]{2}\/[\d]{2}\/[\d]{2}', data[index-4])
        match_des1 = re.search('.\/.',data[index-1])
        if (match_date != None or match_date1 != None) and match_des != None and match_des1 == None:
            numbers.append(float(match_object.string.replace(",","")))
            
        if match_date != None and match_des != None and match_des1 == None:
            Deposits.append(list([data[index-2],data[index-1],data[index]]))
        if match_date1 != None and match_des != None and match_des1 == None:
            Deposits.append(list([data[index-4],data[index-3]+" "+data[index-2]+" "+data[index-1],data[index]]))
            
comma = ","

workbook = xlsxwriter.Workbook('Outputfile.xlsx')

worksheet = workbook.add_worksheet("Deposits")
worksheet.write('A1', 'DATE')
worksheet.write('B1', 'DESCRIPTION')
worksheet.write('C1', 'AMOUNT')
worksheet.write('D1', 'DAY')
worksheet.write('E1', 'MONTH')
worksheet.write('F1', 'YEAR')
i = 2
for deposit in Deposits:
    day, month, year = deposit[0].split("/")
    worksheet.write('A'+str(i), deposit[0])
    worksheet.write('B'+str(i), deposit[1])
    worksheet.write('C'+str(i), deposit[2])
    worksheet.write('D'+str(i), month)
    worksheet.write('E'+str(i), day)
    worksheet.write('F'+str(i), year)
    i = i+1

worksheet = workbook.add_worksheet("Withdrawals")
worksheet.write('A1', 'DATE')
worksheet.write('B1', 'DESCRIPTION')
worksheet.write('C1', 'AMOUNT')
worksheet.write('D1', 'DAY')
worksheet.write('E1', 'MONTH')
worksheet.write('F1', 'YEAR')
i = 2
for withdraws in Withdrawals:
    day, month, year = withdraws[0].split("/")
    worksheet.write('A'+str(i), withdraws[0])
    worksheet.write('B'+str(i), withdraws[1])
    worksheet.write('C'+str(i), withdraws[2])
    worksheet.write('D'+str(i), month)
    worksheet.write('E'+str(i), day)
    worksheet.write('F'+str(i), year)
    i = i+1

worksheet = workbook.add_worksheet("Insights")
worksheet.write('A1', 'Key')
worksheet.write('A2', 'website')
worksheet.write('A3', 'email')
worksheet.write('A4', 'phone_number')
worksheet.write('A5', 'max amount')
worksheet.write('A6', 'min amount')
worksheet.write('B1', 'Value')
worksheet.write('B2', comma.join(website) if website else "NA")
worksheet.write('B3', comma.join(email) if email else "NA")
worksheet.write('B4', comma.join(phone_numbers) if phone_numbers else "NA")
worksheet.write('B5', max(numbers) if numbers else "NA" )
worksheet.write('B6', min(numbers) if numbers else "NA")

workbook.close()