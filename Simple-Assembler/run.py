#NOTE:THIS CODE IS WRITTEN IN PYTHON 3 
import re
import sys
global qw 
qw = {}
global typea

global typeb

global typec

global typed

global typee

global register_dict

global reg_values

global flags

global opcode

register_dict = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

reg_values = [0,0,0,0,0,0,0,0]

flags=[0,0,0,0]

opcode = {'add':'00000','sub':'00001','mov':'00010', 'mov':'00011', 'ld':'00100', 'st':'00101', 'mul':'00110', 
'div':'00111', 'rs':'01000', 'ls':'01001', 'xor':'01010', 'or':'01011', 'and':'01100', 'not':'01101', 
'cmp':'01110', 'jmp':'01111', 'jlt':'10000', 'jgt':'10001', 'je':'10010', 'hlt':'10011'}

typea = ["add", "sub","mul","xor","or","and"]

typeb = ["mov","rs","ls"]

typec = ["mov","div","cmp","not"]

typed = ["ld","st"]

typee = ["jmp","jlt","jgt","je"]

def type_a(a):
    unused = "00"
    re_x = args[1]
    re_y = args[2]
    re_z = args[3]
    opcode_num = opcode[a]
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(re_x)
    pos2 = reg_list_temp.index(re_y)
    pos3 = reg_list_temp.index(re_z)
    reg_x = reg_values[pos1]
    reg_y = int(reg_values[pos2])
    reg_z = int(reg_values[pos3])

    over = len(bin(max(reg_y,reg_z)))


    if a == "add":

        if len(bin(reg_y+reg_z)) > over:
            flags[0] = 1

        elif bin(reg_y)[0] == bin(reg_z)[0]:
            if  bin(reg_y+reg_z)[0] != bin(reg_z)[0]:
                flags[0] = 1

        else:
            reg_values[pos1] = reg_y + reg_z
    
    elif a == "sub":

        if bin(reg_z)>bin(reg_y):
            flags[0] = 1
            reg_values[pos1] = 0
        else:
            reg_values[pos1] = reg_y - reg_z
    
    elif a == "mul":
        if reg_y*reg_z> sys.maxsize:
            flags[0]=1
        else :
            reg_values[pos1]=reg_y*reg_z
    
    elif a == "xor":
        reg_values[pos1] = reg_y^reg_z
    
    elif a == "or":
        reg_values[pos1] = reg_y|reg_z

    
    elif a == "and":
        reg_values[pos1] = reg_y&reg_z
    else:
        return "error"
    
    return opcode_num + unused + register_dict[args[1]] + register_dict[args[2]] + register_dict[args[3]] 

def type_b(a):
    opcode_num = opcode[str(a)]
    temp="00000000"
    
    reg_x = args[1]
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(reg_x)
    n=int(args[2][1:])
    q = bin(n).replace("0b", "")
    
    if a == "mov":
        reg_values[pos1] = args[2][1:]
        opcode_num="00010"
    
    elif a == "rs":
        reg_values[pos1] = reg_values[pos1]>>args[2]
    
    elif a == "ls":
        reg_values[pos1] = reg_values[pos1]<<args[2]
    g=temp[0:int(len(temp)-len(q))]
    
    return opcode_num + register_dict[args[1]] + g + q

def type_c(a):
    unused = "00000"
    reg_x = args[1] 
    reg_y = args[2]
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(reg_x)
    pos2 = reg_list_temp.index(reg_y)
    opcode_num = opcode[a]
    
    if a=="mov" :
        opcode_num="00011"
        reg_values[pos1]=reg_values[pos2]

    elif a=="div" :

        x=reg_values[pos1]
        y=reg_values[pos2]
        q = x//y
        r = x%y
        reg_values[0]=q 
        reg_values[1]=r

    elif a=="not":

        n=reg_values[pos2]
        x = (int)(math.floor(math.log(n) /math.log(2))) + 1;
        reg_values[pos1] = ((1 << x) - 1) ^ n

    elif a=="cmp" :

        x=reg_values[pos1]
        y=reg_values[pos2]

        if x>y :

            flags[1]=1 

        elif x<y : 

            flags[2]=1

        elif x==y :

            flags[3]=1

        else : 

            return "error in code"
    
    else : 
    
        return "error in code "
    
    return opcode_num+unused+register_dict[args[1]]+register_dict[args[2]]

def type_d(a,count):
    n=count 
    q = bin(n).replace("0b", "")
    reg_list_temp = list(register_dict.keys())
    temp="00000000"
    reg_x=args[1]
    pos1 = reg_list_temp.index(reg_x)
    x=args[2]
    qw[x]= count 
    opcode_num = opcode[a]

    if a=="ld":
        reg_values[pos1]=count

    elif a=="st":
        reg_values[pos1]=qw[x]

    g=temp[0:int(len(temp)-len(q))]

    return opcode_num+register_dict[args[1]]+g+q
        
def type_e(a):
    opcode_num = opcode[a]
    args[1]=args[1][1:]
    q=args[1]
    
    d=opcode_num+q

    if a=="jmp":

        list_i0_memadd_i1_bin = [j,d]
        return list_i0_memadd_i1_bin

    elif a=="jlt" :

        if flags[1]==1 :
            j=int(q,2)
        else : 
            j=-1 
        list_i0_memadd_i1_bin = [j,d]
        return list_i0_memadd_i1_bin

    elif a=="jgt":

        if flags[2]==1 :
            j=int(q,2)
        else : 
            j=-1
        list_i0_memadd_i1_bin = [j,d]
        return list_i0_memadd_i1_bin

    elif a=="je":

        if flags[3]==1 :
            j=int(q,2)
        else : 
            j=-1 
        list_i0_memadd_i1_bin = [j,d]
        return list_i0_memadd_i1_bin    

def main():
    file = open('code.txt', 'r')
    code = file.readlines()
    n = len(code) + 1
    length = len(code)
    code_output=[]
    i=0
    count=0
    while i<n :
        length_code = len(code[i])
        global args
        args = re.split(" " , code[i])
        args[len(args)-1]=args[len(args)-1][0 : -1]

        if args[0] in typea   :

            code_out = type_a(args[0])
            code_output.append(code_out+"\n")
            i=i+1
            count=count+1

        elif args[0] in typeb and args[2][0:1]=="$" :

            code_out = type_b(args[0])
            code_output.append(code_out+"\n")
            i=i+1
            count=count+1

        elif args[0] in typec :

            code_out = type_c(args[0])
            code_output.append(code_out+"\n")
            i=i+1
            count=count+1

        elif args[0] in typed :
            count=count+1
            code_out = type_d(args[0],count)
            code_output.append(code_out+"\n")
            i=i+1
            

        elif args[0] in typee :

            code_out = type_e(args[0])
            if code_out[0]==-1 :

                code_output.append(code_out[1]+"\n")
                i=i+1
            elif code_out[0]<=length :

                code_output.append(code_out[1]+"\n")
                i= code_out[0]
            else :

                code_output.append("ERROR\n")
                i=n
            count=count+1

        elif args[0] == "hl" :

            i=n
            code_output.append("1001100000000000\n")
            count=count+1
        elif args[0]=="var" :
            i=i+1
            count=count+1
        elif args[0]=="" :
            i=i+1
        else:
           code_output.append("ERROR\n")
           i=n

    file1 = open('output.txt', 'w')
    file1.writelines(code_output)
    file1.close()
    
                               
                
main()            
            
            
        
        
    

