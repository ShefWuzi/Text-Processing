import re, sys

if len(sys.argv) != 2:
	print("Usage: %s <filename>" %sys.argv[0])
	sys.exit(0)


token_re =  re.compile("[A-Za-z]+")

#Get tokens and count
word_dict = {}
with open(sys.argv[1], "r") as file:
	for z in file:
		tokens = token_re.findall(z.lower())
		for t in tokens:
			if t not in word_dict:
				word_dict[t] = 1
			else:
				word_dict[t] = word_dict[t] + 1

#Sort in descending order
word_dict = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))

print("Total number of words", sum(word_dict.values()))
print("Number of distinct words", len(word_dict.keys()))
print("20 top words with their frequencies\n", "\n".join(['{} -> {}'.format(w, c) for w,c in list(word_dict.items())[:20]]))


import pylab as plt

plt.subplot(511)
plt.title("Top 100 words")
plt.plot([i+1 for i in range(100)], [v for v in list(word_dict.values())[:100]])


plt.subplot(512)
plt.title("Top 1000 words")
plt.plot([i+1 for i in range(1000)], [v for v in list(word_dict.values())[:1000]])


plt.subplot(513)
plt.title("Full set")
plt.plot([i+1 for i in range(len(word_dict))], [v for v in list(word_dict.values())])

plt.subplot(514)
plt.title("Cumulative count")
rank = [i+1 for i in range(1, len(word_dict))]
cum_count = [sum(list(word_dict.values())[:i]) for i in range(1, len(word_dict.items()))]
plt.plot(rank, cum_count)

import math

plt.subplot(515)
plt.title("Power law relationships - Log Cumulative count")
rank = [i+1 for i in range(1, len(word_dict))]
cum_count = [sum(list(word_dict.values())[:i]) for i in range(1, len(word_dict.items()))]
plt.plot([math.log(r) for r in rank], [math.log(c) for c in cum_count])
plt.show()



