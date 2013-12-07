import re

nodes = []
counts = {}

with open("pg100.txt") as f: words = re.compile(r'(\s+|\w+|\S+)').findall(f.read())

words.append("\x03")

for word in words:
    if word not in counts: counts[word] = 1
    else: counts[word] +=1

newcounts = {}
for word in counts:
    if counts[word] < 3:
        for letter in word:
            if letter in newcounts: newcounts[letter] += counts[word]
            else: newcounts[letter] = counts[word]
    else: newcounts[word] = counts[word]
nodes = [(newcounts[word], word) for word in newcounts]

while len(nodes) > 1:
    nodes.sort(lambda x,y: x[0]-y[0])
    s = nodes[0][0]+nodes[1][0]
    node = (s, (nodes.pop(0)[1], nodes.pop(0)[1]))
    nodes.insert(0,node)

codes = {}
tree = ""

def search(node, code):
    global tree
    if isinstance(node, basestring):
        tree += node
        codes[node]=code
        return
    tree+="\x00"
    search(node[0],code+[0])
    tree+="\x01"
    search(node[1],code+[1])
    tree+="\x02"

nodes = nodes[0][1]
search(nodes,[])
bits = []
bytes = []
for word in words:
    try: bits+=codes[word]
    except KeyError:
        for letter in word: bits+=codes[letter]
i=0
lb=-1
while i<len(bits):
    s = i%8
    if not s:
        lb+=1
        bytes.append(0)
        bytes[lb] += 128*bits[i]
    elif s == 1: bytes[lb] += 64*bits[i]
    elif s == 2: bytes[lb] += 32*bits[i]
    elif s == 3: bytes[lb] += 16*bits[i]
    elif s == 4: bytes[lb] += 8*bits[i]
    elif s == 5: bytes[lb] += 4*bits[i]
    elif s == 6: bytes[lb] += 2*bits[i]
    elif s == 7: bytes[lb] += bits[i]
    i+=1

with open("pg100.phc","wb") as f:
    f.write(tree)
    for byte in bytes: f.write(chr(byte))