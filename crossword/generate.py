import sys

from crossword import *


class CrosswordCreator():

	def __init__(self, crossword):
		"""
		Create new CSP crossword generate.
		"""
		self.crossword = crossword
		self.domains = {
			var: self.crossword.words.copy()
			for var in self.crossword.variables
		}

	def letter_grid(self, assignment):
		"""
		Return 2D array representing a given assignment.
		"""
		letters = [
			[None for _ in range(self.crossword.width)]
			for _ in range(self.crossword.height)
		]
		for variable, word in assignment.items():
			direction = variable.direction
			for k in range(len(word)):
				i = variable.i + (k if direction == Variable.DOWN else 0)
				j = variable.j + (k if direction == Variable.ACROSS else 0)
				letters[i][j] = word[k]
		return letters

	def print(self, assignment):
		"""
		Print crossword assignment to the terminal.
		"""
		letters = self.letter_grid(assignment)
		for i in range(self.crossword.height):
			for j in range(self.crossword.width):
				if self.crossword.structure[i][j]:
					print(letters[i][j] or " ", end="")
				else:
					print("█", end="")
			print()

	def save(self, assignment, filename):
		"""
		Save crossword assignment to an image file.
		"""
		from PIL import Image, ImageDraw, ImageFont
		cell_size = 100
		cell_border = 2
		interior_size = cell_size - 2 * cell_border
		letters = self.letter_grid(assignment)

		# Create a blank canvas
		img = Image.new(
			"RGBA",
			(self.crossword.width * cell_size,
			 self.crossword.height * cell_size),
			"black"
		)
		font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
		draw = ImageDraw.Draw(img)

		for i in range(self.crossword.height):
			for j in range(self.crossword.width):

				rect = [
					(j * cell_size + cell_border,
					 i * cell_size + cell_border),
					((j + 1) * cell_size - cell_border,
					 (i + 1) * cell_size - cell_border)
				]
				if self.crossword.structure[i][j]:
					draw.rectangle(rect, fill="white")
					if letters[i][j]:
						w, h = draw.textsize(letters[i][j], font=font)
						draw.text(
							(rect[0][0] + ((interior_size - w) / 2),
							 rect[0][1] + ((interior_size - h) / 2) - 10),
							letters[i][j], fill="black", font=font
						)

		img.save(filename)

	def solve(self):
		"""
		Enforce node and arc consistency, and then solve the CSP.
		"""
		self.enforce_node_consistency()
		self.ac3()
		return self.backtrack(dict())

	def enforce_node_consistency(self):
		"""
		Update `self.domains` such that each variable is node-consistent.
		(Remove any values that are inconsistent with a variable's unary
		 constraints; in this case, the length of the word.)
		"""
		for var in self.domains:
			rem_words=list()
			for word in self.domains[var]:
				if len(word)!=var.length:
					rem_words.append(word)
			for word in rem_words:
				self.domains[var].remove(word)

		# raise NotImplementedError

	def revise(self, x, y):
		"""
		Make variable `x` arc consistent with variable `y`.
		To do so, remove values from `self.domains[x]` for which there is no
		possible corresponding value for `y` in `self.domains[y]`.

		Return True if a revision was made to the domain of `x`; return
		False if no revision was made.
		"""
		(ix,iy)=self.crossword.overlaps[x,y]
		flag=0
		rem_words=list()
		for word_x in self.domains[x]:
			possible=0
			for word_y in self.domains[y]:
				if word_x[ix]==word_y[iy]:
					possible=1
			if possible==0 :
				rem_words.append(word_x)
				flag=1
		
		for word in rem_words:
			self.domains[x].remove(word)				

		if flag==1 :
			return True
		return False

		# raise NotImplementedError

	def ac3(self, arcs=None):
		"""
		Update `self.domains` such that each variable is arc consistent.
		If `arcs` is None, begin with initial list of all arcs in the problem.
		Otherwise, use `arcs` as the initial list of arcs to make consistent.

		Return True if arc consistency is enforced and no domains are empty;
		return False if one or more domains end up empty.
		"""
		if arcs==None:
			queue=list()
			for key in self.crossword.overlaps:
				if self.crossword.overlaps[key] is not None:
					queue.append(key)

			while len(queue)!=0:
				(x,y)=queue[0]
				queue.remove((x,y))
				
				if self.revise(x,y):

					if len(self.domains[x])==0:
						return False

					for neighbor in self.crossword.neighbors(x):
						queue.append((x,neighbor))

			return True

		# raise NotImplementedError

	def assignment_complete(self, assignment):
		"""
		Return True if `assignment` is complete (i.e., assigns a value to each
		crossword variable); return False otherwise.
		"""
		if len(list(assignment))!=len(self.crossword.variables):
			return False
		return True		

		# raise NotImplementedError

	def consistent(self, assignment):
		"""
		Return True if `assignment` is consistent (i.e., words fit in crossword
		puzzle without conflicting characters); return False otherwise.
		"""
		for var1 in assignment:             # for uniqueness
			for var2 in assignment:
				if var1==var2:
					continue
				if var1.length==var2.length:
					if assignment[var1]==assignment[var2]:
						return False

		for var in assignment:
			for neighbor in self.crossword.neighbors(var):
				if neighbor in assignment:
					(i,j)=self.crossword.overlaps[var,neighbor]
					if assignment[var][i]!=assignment[neighbor][j]:
						return False
						
		
		return True

		# raise NotImplementedError

	def order_domain_values(self, var, assignment):
		"""
		Return a list of values in the domain of `var`, in order by
		the number of values they rule out for neighboring variables.
		The first value in the list, for example, should be the one
		that rules out the fewest values among the neighbors of `var`.
		"""
		def second(element):
			return element[1]

		ordered_values=list()
		rule_out=list()
		for word_var in self.domains[var]:
			n=0
			for neighbor in self.crossword.neighbors(var):
				if neighbor not in assignment:
					i,j=self.crossword.overlaps[var,neighbor]
					for word_n in self.domains[neighbor]:
						if word_var[i]!=word_n[j]:
							n+=1
			rule_out.append((word_var,n))

		rule_out.sort(key=second)

		for i in range(len(rule_out)):
			ordered_values.append(rule_out[i][0])

		return ordered_values

		# return self.domains[var]
		# raise NotImplementedError

	def select_unassigned_variable(self, assignment):
		"""
		Return an unassigned variable not already part of `assignment`.
		Choose the variable with the minimum number of remaining values
		in its domain. If there is a tie, choose the variable with the highest
		degree. If there is a tie, any of the tied variables are acceptable
		return values.
		"""
		min_num=999
		choose_var=Variable(0,0,0,0)
		for var in self.crossword.variables:
			if var not in assignment:
				if len(self.domains[var])<min_num:
					min_num=len(self.domains[var])
					choose_var.i=var.i
					choose_var.j=var.j
					choose_var.direction=var.direction
					choose_var.length=var.length
				if len(self.domains[var])==min_num:
					if self.crossword.neighbors(var)>self.crossword.neighbors(choose_var):
						choose_var.i=var.i
						choose_var.j=var.j
						choose_var.direction=var.direction
						choose_var.length=var.length

		return choose_var
		
		# raise NotImplementedError

	def inference(self,assignment,var):
		inferences=dict()
		for z in self.crossword.neighbors(var):
			n=0   #num of values of z satisfying the newly assigned varaible var 
			ix,iz=self.crossword.overlaps[var,z]
			for value in self.domains[z]:
				if assignment[var][ix]==value[iz]:
					n+=1
					val=value
			if n==1:
				inferences[z]=val
		
		return inferences


	def backtrack(self, assignment):
		"""
		Using Backtracking Search, take as input a partial assignment for the
		crossword and return a complete assignment if possible to do so.

		`assignment` is a mapping from variables (keys) to words (values).

		If no assignment is possible, return None.
		"""
		if self.assignment_complete(assignment):
			return assignment

		var=self.select_unassigned_variable(assignment)
		for value in self.order_domain_values(var,assignment):
			assignment[var]=value
			inferred=False
			if self.consistent(assignment):
				inferences=self.inference(assignment,var)
				if len(inferences)!=0:
					inferred=True
					for key in inferences:
						assignment[key]=inferences[key]
				result=self.backtrack(assignment)
				if result is not None:
					return result
			assignment.pop(var)
			if inferred:
				for key in inferences:
					assignment.pop(key)
		return None		

		# raise NotImplementedError


def main():

	# Check usage
	if len(sys.argv) not in [3, 4]:
		sys.exit("Usage: python generate.py structure words [output]")

	# Parse command-line arguments
	structure = sys.argv[1]
	words = sys.argv[2]
	output = sys.argv[3] if len(sys.argv) == 4 else None

	# Generate crossword
	crossword = Crossword(structure, words)
	creator = CrosswordCreator(crossword)
	assignment = creator.solve()

	# Print result
	if assignment is None:
		print("No solution.")
	else:
		creator.print(assignment)
		if output:
			creator.save(assignment, output)


if __name__ == "__main__":
	main()
