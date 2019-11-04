goal = 4681

i = 255

bigI = -1
leftShift = 1
currNum = 0
bigNum = 0
bigShift = 1
while(i > 0):
    leftShift = 1
    currNum = i
    while(currNum <= goal):
        currNum = currNum<<1
        leftShift += 1
        if(currNum > bigNum):
            bigNum = currNum
            bigI = i
            bigShift = leftShift-2

    i -= 1
bigNum = bigI<<bigShift

print('big i = ' + str(bigI))
print('big num = ' + str(bigNum))
print('big2 = ' + str(bigShift))

print(str(goal - bigNum))
