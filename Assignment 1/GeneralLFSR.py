import sys
class LFSR:
    def __init__(self, state:int, size:int, list:list):
        self.state = state
        self.size =size
        self.list =list
        
    def _state(self):
        return f'{self.state:0{self.size}b}'
    
    def new_bit(self):
        newbit = 0
        for l in self.list:
            newbit ^= (self.state >> l) & 1
        self.state = (self.state >> 1) | (newbit << (self.size -1))
        return newbit
    
    def reset(self, newbit):
        self.state = newbit

def get_input():
    choise = input("Gunakan nilai default?Y/n : ")
    if choise in ['N', 'n']:
        try:
            state = int(input("masukan state (dalam biner, contoh 0b0110) : "), 2)
            size = int(input("Masukan size(contoh 4) : "))
            list_input = input("Masukan list posisi(misal 3 0) : ").split()
            list_post =[int(x) for x in list_input]
            return state, size, list_post
        except ValueError:
            print("input tidak valid!")
            sys.exit(1)
    elif choise in ['y', 'Y']:
        state = 0b0110
        size = 4
        list_post = [3, 0]
        print("Menggunakan input default: state = 0b0110, size = 4, list_post = [3, 0] ")
        return state, size, list_post
    else:
        print("Pilihan tidak Valid!!")
        sys.exit(1)

state, size, input_post = get_input()

lfsr = LFSR(state=state, size=size, list=input_post)
        
print("---------------------")
print(" t |", "state |", 'newbit |')
for i in range(20):
    print("---------------------")
    print(f'{i:02d} | {lfsr._state()}  |    {lfsr.new_bit()}   |')
    
