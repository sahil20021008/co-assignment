#NOTE:THIS CODE IS WRITTEN IN PYTHON 3 
import math

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

global list_error

global count_error

count_error=[]

list_error = []

register_dict = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

flags=[0,0,0,0]

reg_values = [0,0,0,0,0,0,0,0,"000000000000"+str(flags[0])+str(flags[1])+str(flags[2])+str(flags[3])]
opcode = {'add':'00000','sub':'00001', 'mov':'00011', 'ld':'00100', 'st':'00101', 'mul':'00110', 
'div':'00111', 'rs':'01000', 'ls':'01001', 'xor':'01010', 'or':'01011', 'and':'01100', 'not':'01101', 
'cmp':'01110', 'jmp':'01111', 'jlt':'10000', 'jgt':'10001', 'je':'10010', 'hlt':'10011'}

typea = ["add", "sub","mul","xor","or","and"]

typeb = ["mov","rs","ls"]

typec = ["mov","div","cmp","not"]

typed = ["ld","st"]

typee = ["jmp","jlt","jgt","je"]

def flagger(a=0, b=0, c=0, d=0):
    flags[0] = a
    flags[1] = b
    flags[2] = c
    flags[3] = d
    reg_values[8] = "000000000000" + str(flags[0]) + str(flags[1]) + str(flags[2]) + str(flags[3])

def type_a(a):
    unused = "00"
    if len(args) != 4:
        return -1
    for i in range(1, 4):
        if args[i] not in register_dict:
            return -1
    re_x = args[1]
    re_y = args[2]
    re_z = args[3]
    opcode_num = opcode[a]
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(re_x)
    pos2 = reg_list_temp.index(re_y)
    pos3 = reg_list_temp.index(re_z)
    reg_x = int(reg_values[pos1])
    reg_y = int(reg_values[pos2])
    reg_z = int(reg_values[pos3])
    if a == "add":
        if reg_y+reg_z>65535:
            flags[0] = 1
        reg_values[pos1] = reg_y + reg_z  
    elif a == "sub":
        if bin(reg_z) > bin(reg_y):
            flags[0] = 1
            reg_values[pos1] = 0
        else:
            reg_values[pos1] = reg_y - reg_z
    elif a == "mul":
        if reg_y*reg_z>65535:
            flags[0] = 1
        reg_values[pos1] = reg_y * reg_z 
    elif a == "xor":
        reg_values[pos1] = reg_y ^ reg_z
    elif a == "or":
        reg_values[pos1] = reg_y | reg_z
    elif a == "and":
        reg_values[pos1] = reg_y & reg_z
    else:
        return "error"
    if reg_values[pos1]>65535:
        reg_values[pos1]-=65536
    return opcode_num + unused + register_dict[args[1]] + register_dict[args[2]] + register_dict[args[3]]

def type_b(a):
    opcode_num = opcode[str(a)]
    temp = "00000000"

    reg_x = args[1]
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(reg_x)
    n = int(args[2][1:])
    boo=args[2][1:].isdigit()
    if not boo:
        return "error"
    if n<0 or n>255:
        return "error"
    q = bin(n).replace("0b", "")
    if a == "mov":
        reg_values[pos1] = n
        opcode_num = "00010"
    elif a == "rs":
        reg_values[pos1] = reg_values[pos1] >> n
    elif a == "ls":
        reg_values[pos1] = reg_values[pos1] << n
    g = temp[0:int(len(temp) - len(q))]

    return opcode_num + register_dict[args[1]] + g + q

def type_c(a):
    unused = "00000"
    reg_x = args[1] 
    reg_y = args[2]
        
    reg_list_temp = list(register_dict.keys())
    pos1 = reg_list_temp.index(reg_x)
    if a=="mov" and args[2]=="FLAGS" :
        reg_values[pos1]=int(reg_values[8],2)#reg_values[8]
    pos2 = reg_list_temp.index(reg_y)
    opcode_num = opcode[a]
    
    
    if a=="mov" :
        opcode_num="00011"
        reg_values[pos1]=reg_values[pos2]

    elif a=="div" :
        x=reg_values[pos1]
        y=reg_values[pos2]
        if x==0 and y==0 :
            q=0
            r=0
        else :
            q = x//y
            r = x%y
        reg_values[0]=q 
        reg_values[1]=r

    elif a=="not":

        n=reg_values[pos2]
        q = bin(n).replace("0b", "")
        reg_values[pos1] = ~n #v=~n
        

    elif a=="cmp" :

        x=int(reg_values[pos1])
        y=int(reg_values[pos2])

        if x>y :

            flags[1]=1 

        elif x<y : 

            flags[2]=1

        elif x==y :

            flags[0]=1

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
    opcode_num = opcode[a]

    if a=="ld":
        if args[2] not in var_name :
            return -1
        else : 
            reg_values[pos1]=qw[x]
    elif a=="st":
        if args[2] not in var_name :
            return -1
        else :
            qw[x]=reg_values[pos1]

    g=temp[0:int(len(temp)-len(q))]

    return opcode_num+register_dict[args[1]]+g+q
        
def type_e(a):
    opcode_num = opcode[a]
    q=args[1]+":"
    type_e_dict_temp = list(type_e_dict.keys())
    temp="00000000"
    if a=="jmp":
        if q not in type_e_dict_temp :
            return [-1,-1]
        else :
            pos1 = type_e_dict_temp.index(q)
            j=type_e_dict[q]
            x = bin(j).replace("0b", "")
            g=temp[0:int(len(temp)-len(x))]
            d=opcode_num+"000"+g+q

    elif a=="jlt" :

        if flags[1]==1 :
            if q not in type_e_dict_temp :
                return [-1,-1]
            else :
                pos1 = type_e_dict_temp.index(q)
                j=type_e_dict[q]
                x = bin(j).replace("0b", "")
                g=temp[0:int(len(temp)-len(x))]
                d=opcode_num+"000"+g+x
                
        else : 
            j=-1
            j=type_e_dict[q]
            x = bin(j).replace("0b", "")
            g=temp[0:int(len(temp)-len(x))]
            d=opcode_num+"000"+g+x
            

    
    elif a=="jgt":

        if flags[2]==1 :
            if q not in type_e_dict_temp :
                return [-1,-1]
            else :
                pos1 = type_e_dict_temp.index(q)
                j=type_e_dict[q]-1
                j1=type_e_dict[q]-1-len(var_name)
                x = bin(j1).replace("0b", "")
                g=temp[0:int(len(temp)-len(x))]
                d=opcode_num+"000"+g+x     
        else :
            j=-1
            j1=type_e_dict[q]-1-len(var_name)
            x = bin(j1).replace("0b", "")
            g=temp[0:int(len(temp)-len(x))]
            d=opcode_num+"000"+g+x
            

    elif a=="je":

        if flags[3]==1 :
            if q not in type_e_dict_temp :
                return [-1,-1]
            else :
                pos1 = type_e_dict_temp.index(q)
                j=type_e_dict[q]
                x = bin(j).replace("0b", "")
                g=temp[0:int(len(temp)-len(x))]
                d=opcode_num+"000"+g+x     
        else : 
            j=-1
            j=type_e_dict[q]
            x = bin(j).replace("0b", "")
            g=temp[0:int(len(temp)-len(x))]
            d=opcode_num+"000"+g+x
    list_i0_memadd_i1_bin = [j,d]
    return list_i0_memadd_i1_bin    

def main():
    file = open('code.txt', 'r')
    code = file.readlines()
    global n
    n = len(code) + 1
    length = len(code)
    global code_output
    code_output=[]
    count=0
    count1=0
    global var_name
    var_name = []
    global type_e_dict
    type_e_dict = {}
    for a in range(0,n-1):
        if code[a]=="" :
            continue
        else :
            args = code[a].split()
            count=count+1
            for bv in args :
                if bv.find(":")!=-1:
                    if bv not in list_error :
                        list_error.append(bv)
                    else :
                        count_error.append(count)
                    type_e_dict[str(bv)]=count
    a=list(set(count_error))
    k=0
    while k < n-1 :
        args = code[k].split()
        count1=count1+1
        for j in args :
            if j.find(":")!=-1 :
                args.remove(j)
            else :
                continue
        if k in count_error :
            code_output.append("ERROR\n")
            k=k+1
        else :
            x=starter(args,count1)
            if x!=0 :
                k=x
            else :
                k=k+1
    
    file1 = open('output.txt', 'w')
    file1.writelines(code_output)
    file1.close()
            
def starter(arg,count1):
    global args
    args=arg
    if len(args)==0 :
        code_output.append("ERROR\n")
        return 0
    if args[0] in typea   :
        code_out = type_a(args[0])
        if code_out==-1 :
            code_output.append("ERROR\n")
        else :
            code_output.append(code_out+"\n")
        return 0
    elif args[0] in typeb and args[2][0:1]=="$" :
        code_out = type_b(args[0])
        code_output.append(code_out+"\n")
        return 0

    elif args[0] in typec :
        code_out = type_c(args[0])
        code_output.append(code_out+"\n")
        return 0

    elif args[0] in typed :
        code_out = type_d(args[0],count1)
        if code_out==-1 :
            code_output.append("ERROR\n")
        else :
            code_output.append(code_out+"\n")
        return 0
            

    elif args[0] in typee :
        print(args[0])
        code_out = type_e(args[0])
        if code_out[0]==-1 :
            code_output.append(str(code_out[1])+"asf\n")
            return 0
        elif code_out[0]<=n-1 :
            code_output.append(code_out[1]+"\n")
            i= code_out[0]
            return code_out[0]
        else :
            code_output.append("ERROR\n")
            return 0
    elif args[0] == "hlt" :
        code_output.append("1001100000000000\n")
        return n
    elif args[0]=="var" :
        if args[1] not in var_name :
            var_name.append(args[1])
        return 0
    elif args[0]=="" :
            return 0
    else:
        code_output.append("ERROR\n")
        return 0
main()            
     
