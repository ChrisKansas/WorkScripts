#!/usr/bin/python3

#Parsing json for specific fields

import json, openpyxl, argparse

#Args
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--json_file',
                    required=True,
                    help="This is the JSON file for conversion."
                   )
parser.add_argument('--output',
                    required=True,
                    help="This is the excel file for the final output."
                   )
parser.add_argument('--type',
                    required=True,
                    help="What are we working with: matches, rules, sites"
                   )
args = parser.parse_args()

#Open workbook/get sheet
wb = openpyxl.load_workbook(args.output)
sheet = wb['Sheet1']

#Empty variables
hostnames = []
backends = []
dictionary = {}
col_count = 0
row_count = 0
match_num = 0

#Open json file and load json
jsonFile = open(args.json_file, 'r')
values = json.load(jsonFile)

#Recursive extraction function
def extract_values(obj, key):
	arr = []

	def extract(obj, arr, key):
	
		if isinstance(obj,dict):
			for k, v in obj.items():
				if k == key and isinstance(v, (dict, list)):
					arr.append(v[0][0])
				elif isinstance(v, (dict,list)):
					extract(v, arr, key)
				elif k == key:
					arr.append(v)
		elif isinstance(obj,list):
			for item in obj:
				extract(item, arr, key)
		return arr
	
	results = extract(obj, arr, key)
	return results

#Checking Arg Type
if args.type:
    #Working with Sites JSON
    if args.type == "sites":
        hostnames = extract_values(values, 'hostname')
        backends = extract_values(values, 'backend')

        #Write each value to the spreadsheet
        for rowNum in range(1, len(hostnames)+1):
            sheet.cell(row=rowNum+1, column=1).value = hostnames[rowNum-1]
            sheet.cell(row=rowNum+1, column=2).value = backends[rowNum-1]

        #Sanity Check
        print(hostnames[-1], backends[-1])

    #Working with Matches JSON
    elif args.type == "matches":
        for i in values[0]:
            row_count+=1
            for key in i.keys():
                col_count+=1
                if key == "rules":
                    for k in values['Ok'][row_count-1]['rules']:
                        match_num+=1
                        for key2 in k.keys():
                            sheet.cell(row=1, column=col_count).value = "rule match " + str(match_num) + " - " + key2
                            key2 = extract_values(k, key2)
                            if key2[0] == 1:
                                sheet.cell(row=row_count, column=col_count).value = "True"
                            elif key2[0] == 0:
                                sheet.cell(row=row_count, column=col_count).value = "False"
                            else:
                                sheet.cell(row=row_count, column=col_count).value = key2[0]
                            col_count+=1
                    match_num=0
                elif key == "risk":
                    col_count-=1
                    continue
                else:
                    sheet.cell(row=1, column=col_count).value = key
                    header = key
                    key = extract_values(i, key)
                    if key[0] == 1:
                        sheet.cell(row=row_count, column=col_count).value = "True"
                    elif key[0] == 0:
                        sheet.cell(row=row_count, column=col_count).value = "False"
                    else:
                        try:
                            sheet.cell(row=row_count, column=col_count).value = key[0]
                        except:
                            print("**This is the problem child**")
                            print("Row #:" + str(row_count))
                            print(header)
                            print(key[0])
                            continue
            col_count=0

#Save spreadsheet
wb.save(args.output)
        
#Close out the files
wb.close()
jsonFile.close()
