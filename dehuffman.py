ifile = open("pg100.phc")
ofile = open("pg100.phd","w")

def parse():
    c = ifile.read(1)
    if c=="\x00":
        left = parse()
        assert ifile.read(1) == "\x01"
    else:
        b=c
        while 1:
            c = ifile.read(1)
            if c=="\x01":
                left = b
                break
            else: b+=c
    c = ifile.read(1)
    if  c=="\x00":
        right = parse()
        assert ifile.read(1) == "\x02"
    else:
        b = c
        while 1:
            c = ifile.read(1)
            if c=="\x02":
                right=b
                break
            else: b+=c
    return left, right

ifile.read(1)
nodes = parse()
bytes = ifile.read()

i = -1
def nextbit():
    global i
    i+=1
    return (ord(bytes[i/8]) >> (7-(i%8)))%2

def decrypt(node):
    if isinstance(node, basestring): return node
    if nextbit(): return decrypt(node[1])
    else: return decrypt(node[0])

while 1:
    c = decrypt(nodes)
    if c == '\x03': break
    else: ofile.write(c)