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
        
def ListGambar():
    with open('ListLFSR.txt', 'r') as l:
        lg = l.read().splitlines()
    return [baris.strip() for baris in lg]
        
def LFSRBasic():
    state = 0b0110
    state_basic = []
    for i in range(16):
        state_basic.append(f'{state:04b}')
        newbit = ((state >> 3) ^ state) & 1
        state = (state >> 1) | (newbit << 3)
    return state_basic
        
def LFSRGeneral():
    lfsr = LFSR(state=0b0110, size=4, list=[3, 0])
    state_general = []
    for i in range(16):
        state_general.append(lfsr._state())
        lfsr.new_bit()
    return state_general

states_basic = LFSRBasic()
state_general = LFSRGeneral()
list_gambar = ListGambar()

print("Perbandingan LFSR Bacis dan LFSR General")
print(f' iter | List Gambar | LFSR Basic | LFSR Genaral | Match |')
print("---------------------------------------------------------")

for i in range(16):
    match = "O" if states_basic[i] == state_general[i] == list_gambar[i] else 'X'
    print(f'  {i:02}  |    {list_gambar[i]}     |    {states_basic[i]}    |    {state_general[i]}      |   {match}   | ')
    
if states_basic == state_general == list_gambar :
    print("Semua menghasilkan state yang sama")
else:
    print("Ada perbedaan Output")
    
# print(list_gambar)
# print(state_general)
# print(states_basic)