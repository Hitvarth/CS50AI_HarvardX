import csv
import itertools
import sys
from heredity import joint_probability


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]    

people = load_data(sys.argv[1])
names = set(people)
print(people)
print(names)
print(powerset(names))

print(joint_probability(people, {"Harry"}, {"James"}, {"James"}))


# for have_trait in powerset(names):

#         # Check if current set of people violates known information
#         fails_evidence = any(
#             (people[person]["trait"] is not None and
#              people[person]["trait"] != (person in have_trait))
#             for person in names
#         )
#         if fails_evidence:
        	
#             print('\n fails_evidence is True')
#             print(have_trait)
#             continue

#         else:
        	
#         	print('\n fails_evidence is False')
#         	print(have_trait)