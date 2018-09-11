text='a'*10+'b'*15+'c'*30+'d'*16+'e'*29
realText="One of the big picture issues in looking at compiled C code is the function-calling conventions. These are the methods that a calling function and a called function agree on how parameters and return values should be passed between them, and how the stack is used by the function itself. The layout of the stack constitutes the stack frame, and knowing how this works can go a long way to decoding how something works.In C and modern CPU design conventions, the stack frame is a chunk of memory, allocated from the stack, at run-time, each time a function is called, to store its automatic variables. Hence nested or recursive calls to the same function, each successively obtain their own separate frames.Physically, a function's stack frame is the area between the addresses contained in esp, the stack pointer, and ebp, the frame pointer (base pointer in Intel terminology). Thus, if a function pushes more values onto the stack, it is effectively growing its frame.This is a very low-level view: the picture as seen from the C/C++ programmer is illustrated elsewhere:"

def getFreqs(text):
    freqs={}
    for c in text:
        freqs[c]=freqs.get(c,0)+1
    afreqs=[]
    for c in freqs:
        afreqs.append({'tree':c, 'count':freqs[c]})
    return afreqs

def sortFreqs(freqs):
    return sorted(freqs, key=lambda k:k['count'])

def buildTree(text):
    freqs=getFreqs(text)
    while(len(freqs)>1):
        freqs=sortFreqs(freqs)
        tree={0:freqs[0]['tree'], 1:freqs[1]['tree']}
        freqs=freqs[2:]+[{'tree':tree, 'count': freqs[0]['count']+freqs[1]['count']}]
    return freqs[0]['tree']

def getTreeDepth(tree, depth=0):
    if(isinstance(tree, basestring)):
        return depth
    else:
        return max(getTreeDepth(tree[0], depth+1), getTreeDepth(tree[1], depth+1))

def buildKeys(tree, bi=""):
    if(isinstance(tree, basestring)):
        return {tree: bi}
    else:
        b=buildKeys(tree[0], bi+'0')
        b.update(buildKeys(tree[1], bi+'1'))
        return b


def encode(text, keys):
    encoded=""
    for c in text:
        encoded+=keys[c]
    return encoded

def decode(encoded, tree):
    text=""
    while(encoded):
        t=tree
        while(True):
            if(isinstance(t, basestring)):
                text+=t
                break
            else:
                t=t[int(encoded[0])]
            encoded=encoded[1:]
    return text

import hashlib
def printASM(tree, root=True):
    if(isinstance(tree, basestring)):
        return ord(tree)
    else:
        l=printASM(tree[0], False)
        r=printASM(tree[1], False)
        label='h'+hashlib.sha256(str(l)+str(r)).hexdigest() # len(label)<=4096
        if(root):
            label="root"
        line=label+': db '+str(l)+','+str(r)
        if(isinstance(l, int)):
            if(isinstance(r, int)):
                line+=",0"
            else:
                line+=",1"
        elif(isinstance(r, int)):
            line+=",2"
        print(line)
        return label

def fullEncode(text):
    tree=buildTree(text)
    printASM(tree)
    print('')
    keys=buildKeys(tree)
    return encode(text, keys)

if __name__ == "__main__":
    print(hex(int(fullEncode(realText), 2)))
