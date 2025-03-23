
def state():
    state = 0b0110
    print("State :")
    for i in range(20):
        print("{:04b}".format(state))
        newbit = ((state >> 3) ^ state) & 1
        state = (state >> 1) | (newbit << 3)
def newbit():
    state = 0b0110
    print("Newbit :")
    for i in range(20):
        print(state & 1, end="")
        newbit = ((state >> 3) ^ state) & 1
        state = (state >> 1) | (newbit << 3)

state()
newbit()