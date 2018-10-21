from dahuffman import HuffmanCodec
import random
import collections
dic = {}

class MinHeapNode:
    def setNode(self, left, right, freq, char):
        self.left = left
        self.right = right
        self.freq = freq
        self.char = char
        return self
def huffmanCoding(arr, freq):
    heapArr = []

    for i in range(len(arr)):
        heapArr.append(MinHeapNode().setNode(None, None , freq[i], arr[i]))
        #print(heapArr[i].freq, heapArr[i].char)

    while(len(heapArr)>1):
       left = heapArr.pop(0)
       right = heapArr.pop(0)
       insertionSort(heapArr, MinHeapNode().setNode(left, right, left.freq+right.freq, left.char + right.char))

    rootheap= heapArr.pop()

    return rootheap


def printHeap(heap, str):
    if heap.left != None:
        printHeap(heap.left, str + '0')

    if heap.right !=None: 
        printHeap(heap.right, str + '1' )

    if heap.left == None:
        #print(heap.char, str)
        dic[heap.char] = str

def insertionSort(heapArr, heap):
    index = len(heapArr)
    for i in range(len(heapArr)):
        if heap.freq < heapArr[i].freq:
           index  = i
           break
    heapArr.insert(index, heap)

def makeNewString(arr, freq):

    freqcopy = freq[:]
    arrcopy = arr[:]
    strval = ''
    while len(freqcopy) >0:
        number = random.randrange(0,len(freqcopy))
        freqcopy[number] = freqcopy[number]-1
        strval = strval + arrcopy[number]
        if freqcopy[number] == 0:
            freqcopy.pop(number)
            arrcopy.pop(number)

    return strval

def endcoding(mtfres):
    strval = ""    
    for i in range(len(mtfres)):
        #print(dic)
        strval = strval + dic[mtfres[i]]

    return strval

def huffmandecode(rootheap, strvalencoded):

    index = 0
    orgstr = []

    while index < len(strvalencoded):
        str = getchar(rootheap, index, strvalencoded)
        index = index + len(dic[str])
        orgstr.append(str)
    return orgstr

def getchar(rootheap, index, strvalencoded):
    if rootheap.left == None:
        return rootheap.char

    number = int(strvalencoded[index])
    if number ==0:
        return getchar(rootheap.left, index+1, strvalencoded)

    if number ==1:
        return getchar(rootheap.right, index+1, strvalencoded)



def BandWTransformation(inp):

    inpToList = list(inp)
    originalInput = list(inp)
    index = 0
    lines = []
    result = []
    lastChars = ""

    for s in inpToList: #go through all chars of input

        poped = inpToList.pop() #remove the last char of the last index
        inpToList.insert(0, poped) #insert the last char in the first index
        res = inpToList.copy() #save string in temp var
        lines.append(res) #add to list of lines

    lines.sort() #sort every line in reverse

    index = lines.index(originalInput) #save the position of our original input in the table
    
    for s in range(len(lines)):
        result.append(lines[s][len(lines)-1]) #append the las char of every line to a list
    
    lastChars = lastChars.join(result) #convert that list of chars into a string
   
    return lastChars, index

def moveToFront(bwRes):

    bwRes = list(bwRes)
    result = []
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for s in range(len(bwRes)):
        index = abc.index(bwRes[s]) #get index of current char in the abc
        temp = index #save index in temp var
        result.append(str(temp)) #add index to result
        abc.insert(0,abc[index]) #move the current char to the front of the list
        abc.pop(index + 1)
    
    return result

def  huffman(mtfRes):
    arr = []
    freq = []
    for i in range(len(mtfRes)):
        if mtfRes[i] not in arr:
            arr.append(mtfRes[i])
            freq.append(0)
        else:
            freq[arr.index(mtfRes[i])] += 1

    

    rootheap = huffmanCoding(arr, freq)

    printHeap(rootheap, '')

    strval  =  mtfRes

    strvalencoded = endcoding(strval)

    return strvalencoded, rootheap

def compress(inp):

    rootheap = 0

    bwRes, index = BandWTransformation(inp) #save the returned value from Barrows and wheeler transofrmation and the index of the original input
    mtfRes = moveToFront(bwRes) #save the returned value from move to front
    compressed, rootheap = huffman(mtfRes) #save compressed mtf using huffman

    return compressed, rootheap, index

def decompress(compressedInp, rootheap, index):
    
    decompressedList = huffmandecode(rootheap, compressedInp)

    letters = []
    lines = []
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    for l in range(len(decompressedList)): 
        letter = abc[int(decompressedList[l])] # letter of the abc given the index by de mtfRes
        temp = letter
        letters.extend(temp) #save letter in letters[]
        abc.remove(temp) #remove letter in current index
        abc.insert(0, temp) #move the current char to the front of the list
        
    letters = list(letters)
    lines = [] 

    for l in range(len(letters)):
        lines.append([] * (l + 1)) #create a list of the length of the string

    for l in range(len(letters)): #for every column
        temp = letters.copy() #copy the original string
        for i in range(len(letters)): #for each line of the column
            lines[i].insert(0, temp[i]) #insert its corresponding char.
        lines.sort() #sort the list
    
    return lines[index] #return only the original line, which i could find thanks to the index


def main():
    codec = {}
    index = 0

    inp = input("Insert string to compress: ")
    compressedInp, rootheap, index = compress(inp)
    print("inp compressed weights", str(len(compressedInp)) +" bits" , "and it's string is:" ,compressedInp)
    decompressedInp = decompress(compressedInp, rootheap, index)
    print("inp decompressed weights", str(len(decompressedInp)* 8)  + " bits", "and it's string is:" ,decompressedInp)


main()



