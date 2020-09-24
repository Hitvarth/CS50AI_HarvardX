import csv 
import sys

people={}

names={}

directory=sys.argv[1]

with open(f'{directory}''/people.csv',encoding="utf-8") as f:
	reader=csv.DictReader(f)

	for row in reader:
		# for element in row:
		# 	print(element)
		# print(row)	
		people[row["id"]] = {"name": row["name"],"birth": row["birth"],"movies": set() }
		if row["name"].lower() not in names:
			names[row["name"].lower()]={row["id"]}
		else:
			names[row["name"].lower()].add(row["id"])
	print(people)

    