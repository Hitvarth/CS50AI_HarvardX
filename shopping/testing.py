import csv

evidence=list()
label=list()

def num_month(Month):
	mapping={ 'Jan':0, 'Feb':1, 'Mar':2, 'Apr':3, 'May':4, 'June':5, 'Jul':6, 'Aug':7, 'Sep':8, 'Oct':9, 
	'Nov':10, 'Dec':11 }
	return mapping[Month]

def visitor_type(VisitorType):
	if VisitorType=='Returning_Visitor':
		return 1
	return 0

def Weekend(Weekend):
	if Weekend=='True':
		return 1
	return 0	

def Revenue(Revenue):
	if Revenue=='True':
		return 1
	return 0	


with open('shopping.csv',newline='') as f:
	data=csv.DictReader(f)
	for row in data:
		entry=list()
		entry.append(int(row['Administrative']))
		entry.append(float(row['Administrative_Duration']))
		entry.append(int(row['Informational']))
		entry.append(float(row['Informational_Duration']))
		entry.append(int(row['ProductRelated']))
		entry.append(float(row['ProductRelated_Duration']))
		entry.append(float(row['BounceRates']))
		entry.append(float(row['ExitRates']))
		entry.append(float(row['PageValues']))
		entry.append(float(row['SpecialDay']))
		entry.append(num_month(row['Month']))
		entry.append(int(row['OperatingSystems']))
		entry.append(int(row['Browser']))
		entry.append(int(row['Region']))
		entry.append(int(row['TrafficType']))
		entry.append(visitor_type(row['VisitorType']))
		entry.append(Weekend(row['Weekend']))
		
		label.append(Revenue(row['Revenue']))

		print(entry)
		print(bool(row['Revenue']))

		evidence.append(entry)



print('\n\n', evidence[1])