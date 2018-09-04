import time
listNum = [6, 4, 8, 9, 2, 5, 7, 676, 33, 334, 22222]

print(time.time())
listNum.sort()
print(time.time())
print(listNum)

nLen = len(listNum)
i = 0
j = 0
temp = 0
print(time.time())
while i < nLen:
    while j < nLen - i - 1:
        if listNum[j] > listNum[j+1]:
            temp = listNum[j+1]
            listNum[j+1] = listNum[j]
            listNum[j] = temp
        j = j + 1
    i = i + 1
print(time.time())
print(listNum)