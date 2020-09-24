import os
import random
import re
import sys
# from pagerank import transition_model, sample_pagerank

# pages = dict()
# directory='corpus0'
#     # Extract all links from HTML files
# for filename in os.listdir(directory):
#     if not filename.endswith(".html"):
#         continue
#     with open(os.path.join(directory, filename)) as f:
#         contents = f.read()
#         links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
#         pages[filename] = set(links) - {filename}

# # Only include links to other pages in the corpus
# for filename in pages:
#     pages[filename] = set(
#         link for link in pages[filename]
#         if link in pages
#     )

# # print(len(pages))
# print(pages)

# # print(list(pages))
# # print(random.choice(list(pages)))
# # print(transition_model(pages,'4.html',0.85))
# # print(sample_pagerank(pages,0.85,10000))
# for key in pages:
# 	print(key)
# 	print(type(key))

# x=60
# for i in range(15):
# 	x=x+(x*0.05)

# print(x)

x=[1,2,3,4]
y=[2,3,4,5]

print(all((x[i]-y[i]==-1) for i in range(4)))