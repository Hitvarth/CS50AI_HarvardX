import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
	if len(sys.argv) != 2:
		sys.exit("Usage: python pagerank.py corpus")
	corpus = crawl(sys.argv[1])
	ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
	print(f"PageRank Results from Sampling (n = {SAMPLES})")
	for page in sorted(ranks):
		print(f"  {page}: {ranks[page]:.4f}")
	ranks = iterate_pagerank(corpus, DAMPING)
	print(f"PageRank Results from Iteration")
	for page in sorted(ranks):
		print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
	"""
	Parse a directory of HTML pages and check for links to other pages.
	Return a dictionary where each key is a page, and values are
	a list of all other pages in the corpus that are linked to by the page.
	"""
	pages = dict()

	# Extract all links from HTML files
	for filename in os.listdir(directory):
		if not filename.endswith(".html"):
			continue
		with open(os.path.join(directory, filename)) as f:
			contents = f.read()
			links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
			pages[filename] = set(links) - {filename}

	# Only include links to other pages in the corpus
	for filename in pages:
		pages[filename] = set(
			link for link in pages[filename]
			if link in pages
		)

	return pages


def transition_model(corpus, page, damping_factor):
	"""
	Return a probability distribution over which page to visit next,
	given a current page.

	With probability `damping_factor`, choose a link at random
	linked to by `page`. With probability `1 - damping_factor`, choose
	a link at random chosen from all pages in the corpus.
	"""
	prob_dis=dict()
	d=damping_factor

	for key in corpus:
		prob=0.0
		if key in corpus[page]:
			prob+=d/len(corpus[page])
		prob+=(1-d)/len(corpus)
		prob_dis[key]=prob

	return prob_dis

	raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
	"""
	Return PageRank values for each page by sampling `n` pages
	according to transition model, starting with a page at random.

	Return a dictionary where keys are page names, and values are
	their estimated PageRank value (a value between 0 and 1). All
	PageRank values should sum to 1.
	"""
	PageRanks=dict()
	for key in corpus:
		PageRanks[key]=0

	page=random.choice(list(corpus))
	PageRanks[page]+=1/n

	for i in range(1,n):
		prob_dis=transition_model(corpus,page,damping_factor)
		limits=[]             # to divide the number line between 0 and 1 in parts equal to the probabilities
		links=list(prob_dis)  # stores all the keys of the prob_dis in the same order
		limits.append(prob_dis[links[0]])
		for j in range(1,len(links)):
			limits.append(limits[j-1]+prob_dis[links[j]])
		limits.append(0.0)	
		
		r=random.random()  # returns a random number in [0.0,1.0)
	
		for i in range(0,len(limits)-1):
			if limits[i-1]<=r<limits[i]:
				page=links[i]
				PageRanks[page]+=1/n
				break 

	return PageRanks

	raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
	"""
	Return PageRank values for each page by iteratively updating
	PageRank values until convergence.

	Return a dictionary where keys are page names, and values are
	their estimated PageRank value (a value between 0 and 1). All
	PageRank values should sum to 1.
	"""
	def sigma(PageRanks,corpus,p):           # function to find the sigma term for page p
		linking_pages=[]
		for page in corpus:
			if p in corpus[page]:
				linking_pages.append(page)
		sigma=0
		for i in linking_pages:
			sigma+=PageRanks[i]/len(corpus[i])
		return sigma


	d=damping_factor
	N=len(corpus)
	PageRanks=dict()
	for key in corpus:
		PageRanks[key]=1/N

	new_PRs=dict()	

	while True:
		
		for page in PageRanks:
			new_PRs[page]=(1-d)/N + d*sigma(PageRanks,corpus,page)
		
		if all((-0.001<new_PRs[page]-PageRanks[page]<0.001) for page in PageRanks):
			break
		
		for page in PageRanks:
			PageRanks[page]=new_PRs[page]

	return new_PRs		

	raise NotImplementedError


if __name__ == "__main__":
	main()
