# python simulator file
import sys
from sys import stdin 

import math

import matplotlib as plt

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

reg_values = [0,0,0,0,0,0,0,"000000000000"+str(flags[0])+str(flags[1])+str(flags[2])+str(flags[3])]
opcode = {'add':'00000','sub':'00001', 'mov':'00011', 'ld':'00100', 'st':'00101', 'mul':'00110', 
'div':'00111', 'rs':'01000', 'ls':'01001', 'xor':'01010', 'or':'01011', 'and':'01100', 'not':'01101', 
'cmp':'01110', 'jmp':'01111', 'jlt':'10000', 'jgt':'10001', 'je':'10010', 'hlt':'10011'}

typea = ["00000", "00001","00110","01010","01011","01100"]

typeb = ["00010","01000","01001"]

typec = ["00011","00111","01110","01101"]

typed = ["00100","00101"]

typee = ["01111","10000","10001","10010"]

def flagger(a=0, b=0, c=0, d=0):
    flags[0] = a
    flags[1] = b
    flags[2] = c
    flags[3] = d
    reg_values[7] = "000000000000" + str(flags[0]) + str(flags[1]) + str(flags[2]) + str(flags[3])

def type_a(a,arg,pc):
    

    r1 = arg[slice(7,10)]
    r2 = arg[slice(10,13)]
    r3 = arg[slice(13,16)]

    reg_list_temp=list(register_dict.values())

    
    pos1 = reg_list_temp.index(r1)
    pos2 = reg_list_temp.index(r2)
    pos3 = reg_list_temp.index(r3)
    
    reg_y = int(reg_values[pos2])
    reg_z = int(reg_values[pos3])
    
    if a == "00000":
        if reg_y + reg_z > 65535:
            flagger(1)  # flags[0] = 1
        else:
            flagger()
        reg_values[pos1] = reg_y + reg_z
    elif a == "00001":
        if bin(reg_z) > bin(reg_y):
            flagger(1)  # flags[0] = 1
            reg_values[pos1] = 0
        else:
            flagger()
            reg_values[pos1] = reg_y - reg_z
    elif a == "00110":
        if reg_y * reg_z > 65535:
            flagger(1)  # flags[0] = 1
        else:
            flagger()
        reg_values[pos1] = reg_y * reg_z
    elif a == "01010":
        flagger()
        reg_values[pos1] = reg_y ^ reg_z
    elif a == "01011":
        flagger()
        reg_values[pos1] = reg_y | reg_z
    elif a == "01100":
        flagger()
        reg_values[pos1] = reg_y & reg_z
    else:
        return "error"
    while reg_values[pos1] > 65535:
        reg_values[pos1] -= 65536
    return str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}'

# def type_a(a,count):
#     unused = "00"
#     if len(args) != 4:
#         return -1
#     for i in range(1, 4):
#         if args[i] not in register_dict:
#             return -2
#     re_x = args[1]
#     re_y = args[2]
#     re_z = args[3]
#     opcode_num = opcode[a]
#     reg_list_temp = list(register_dict.keys())
#     pos1 = reg_list_temp.index(re_x)
#     pos2 = reg_list_temp.index(re_y)
#     pos3 = reg_list_temp.index(re_z)
#     reg_x = int(reg_values[pos1])
#     reg_y = int(reg_values[pos2])
#     reg_z = int(reg_values[pos3])
#     if a == "00000":
#         if reg_y+reg_z>65535:
#             flagger(1) #flags[0] = 1
#         else:
#             flagger()
#         reg_values[pos1] = reg_y + reg_z  
#     elif a == "00001":
#         if bin(reg_z) > bin(reg_y):
#             flagger(1) #flags[0] = 1
#             reg_values[pos1] = 0
#         else:
#             flagger()
#             reg_values[pos1] = reg_y - reg_z
#     elif a == "00110":
#         if reg_y*reg_z>65535:
#             flagger(1) #flags[0] = 1
#         else:
#             flagger()
#         reg_values[pos1] = reg_y * reg_z 
#     elif a == "01010":
#         flagger()
#         reg_values[pos1] = reg_y ^ reg_z
#     elif a == "01011":
#         flagger()
#         reg_values[pos1] = reg_y | reg_z
#     elif a == "01100":
#         flagger()
#         reg_values[pos1] = reg_y & reg_z
#     else:
#         return "error"
# #     if reg_values[pos1]>65535:
# #         reg_values[pos1]-=65536
#     while reg_values[pos1] > 65535: #replaced overflow if else with while loop
#         reg_values[pos1] -= 65536
#     return opcode_num + unused + register_dict[args[1]] + register_dict[args[2]] + register_dict[args[3]]

def type_b(a,arg,pc):
    reg_x = arg[slice(5,8)]
    reg_list_temp = list(register_dict.values())
    pos1 = reg_list_temp.index(reg_x)
    n=int(arg[slice(8,16)],2)
    flagger()
    if a == "00010":
        reg_values[pos1] = n
    elif a == "01000":
        reg_values[pos1] = reg_values[pos1] >> n
    elif a == "01001":
        reg_values[pos1] = reg_values[pos1] << n
        if reg_values[pos1] > 65535:  # added overflow check
            flagger(1)
    while reg_values[pos1] > 65535:  # added overflow condition
        reg_values[pos1] -= 65536
    return str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}'


# def type_b(a,count1):
#     opcode_num = opcode[str(a)]
#     temp = "00000000"

#     reg_x = args[1]
#     reg_list_temp = list(register_dict.keys())
#     pos1 = reg_list_temp.index(reg_x)
#     #n = int(args[2][1:])
#     boo=args[2][1:].isdigit()
#     if not boo:
#         return "Type error on line:" + str(count1) + " , int expected"
#     n = int(args[2][1:])#moved n after checking if int
#     if n<0 or n>255:
#         return "Error on line :" + str(count1) + " , illegal immediate value\n"
#     q = bin(n).replace("0b", "")
#     flagger()
#     if a == "mov":
#         reg_values[pos1] = n
#         opcode_num = "00010"
#     elif a == "rs":
#         reg_values[pos1] = reg_values[pos1] >> n
#     elif a == "ls":
#         reg_values[pos1] = reg_values[pos1] << n
#         if reg_values[pos1] > 65535:#added overflow check
#             flagger(1)
#     while reg_values[pos1] > 65535: #added overflow condition
#         reg_values[pos1] -= 65536
#     g = temp[0:int(len(temp) - len(q))]

#     return opcode_num + register_dict[args[1]] + g + q

def type_c(a,arg,pc):
    unused = "00000"
    reg_x = arg[slice(10,13)] 
    reg_y = arg[slice(13,16)]
        
    reg_list_temp = list(register_dict.values())
    pos1 = reg_list_temp.index(reg_x)
#     if a=="mov" and args[2]=="FLAGS" :
#         reg_values[pos1]=int(reg_values[8],2)#reg_values[8]
        
    pos2 = reg_list_temp.index(reg_y)

#    if len(args)!=3:
#        return "Syntax error on line :" + str(pc) + " ,instructions of type C should have 3 arguments\n"
        
    if a=="00011" :#turned if to elif
        reg_values[pos1]=reg_values[pos2]
        flagger()
        
    elif a=="00111" :
        x=reg_values[pos1]
        y=reg_values[pos2]
        if x==0 and y==0 :
            q=0
            r=0
        elif y==0:
            return "ZeroDivisionError on line:" + str(pc) + " ,integer division by zero\n"
        else :
            q = x//y
            r = x%y
        reg_values[0]=q 
        reg_values[1]=r
        flagger()
        
    elif a=="01101":
        flagger()
        n=reg_values[pos2]
        q = bin(n).replace("0b", "")
        reg_values[pos1] = ~n #v=~n
        

    elif a=="01110" :

        x=int(reg_values[pos1])
        y=int(reg_values[pos2])

        if x>y :
            flagger(b=1)
            #flags[1]=1 

        elif x<y : 
            flagger(c=1)
            #flags[2]=1

        elif x==y :

            flagger(d=1)#flags[0]=1 this set overflow flag instead of equal flag

        else : 

            return "Error"
    
    else : 
    
        return "Error"  
    return str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}'

def type_d(a,arg,pc):

    n=pc
    q = bin(n).replace("0b", "")
    reg_list_temp = list(register_dict.values())
    temp="00000000"
    reg_x=arg[slice(5,8)]
    pos1 = reg_list_temp.index(reg_x)
    x=arg[slice(8,16)] 

    if a=="00100":
        reg_values[pos1]=qw[x]
    elif a=="00101":
        qw[x]=reg_values[pos1]
        
    flagger()
    g=temp[0:int(len(temp)-len(q))]
    return str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}'


def type_e(a,arg,pc):
    
    type_e_dict_temp = list(type_e_dict.values())
    q = int(arg[slice(8,16)],2)
    
    if a=="01111":
        q=q       

    elif a=="10000" :

        if flags[1]==1 :
            q=q
          
        else : 
            q=-1
            
    elif a=="10001":

        if flags[2]==1 :
            q=q  
        else :
            q=-1
            

    elif a=="10010":

        if flags[3]==1 :
            q=q
        else : 
            q=-1 
    d=str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}'       
    list_i0_memadd_i1_bin = [q,d]
    flagger()
    
    return list_i0_memadd_i1_bin 

def main():
    code=[]
    for line in stdin :
        if line=="":
            break
        code.append(line)
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
            code_output.append("ERROR on line :" + str(count1) + "\n")
            k=k+1
        else :
            x=starter(args,count1)
            if x!=0 :
                k=x
            else :
                k=k+1
    
    
    var=sys.stdout
    for i in code_output:
        var.write(i)
         
def starter(arg,count1):
    global args
    type_checker = arg[slice(5)]
    args = type_checker
    if len(args)==0:
        code_output.append("General Syntax Error on line :" + str(count1) + "\n")
        return 0
    
    if args in typea:
        code_out = type_a(args,arg,count1)
        code_output.append(code_out+"\n")
        return 0
    elif args in typeb:
        code_out = type_b(args,arg,count1)
        code_output.append(code_out+"\n")
        return 0

    elif args in typec:
        code_out = type_c(args,arg,count1)
        code_output.append(code_out+"\n")
        return 0

    elif args in typed :
        code_out = type_d(args,arg,count1)
        code_output.append(code_out+"\n")
        return 0
            

    elif args[0] in typee :
        code_out = type_e(args[0],count1)
        if code_out[1] == -1 :
            code_out.append("Undefined label:" + str(count1) +"\n")
            return 0
        if code_out[0] == -1 :
            code_output.append(str(code_out[1])+"\n")
            return 0

        elif code_out == -2:
            code_output.append("Syntax error on line :" + str(count1) + " ,instructions of type E should have 2 arguments\n")


        elif code_out[0]<=n-1 :
            code_output.append(code_out[1]+"\n")
            i= code_out[0]
            return code_out[0]

        else :
            code_output.append("ERROR on line :" + str(count1) + "\n")
            return 0
        
    elif args == "10011":
        code_output.append(str(f'{count1:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + f'{reg_values[7]:016b}' + "\n")
        return n
    else:
        code_output.append("ERROR on line :" + str(count1) + "\n")
        return 0
main()          
