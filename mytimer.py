import timeout
mylist = []
mycounter = 0

def append():
    global mycounter
    mylist.append(mycounter)
    mycounter += 1


try:
    with timeout.within(1):
        while True:
            append()

except timeout.TimeoutError:
    print(mycounter)
