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

reg_values = [0,0,0,0,0,0,0,0]
opcode = {'add':'00000','sub':'00001', 'mov':'00011', 'ld':'00100', 'st':'00101', 'mul':'00110', 
'div':'00111', 'rs':'01000', 'ls':'01001', 'xor':'01010', 'or':'01011', 'and':'01100', 'not':'01101', 
'cmp':'01110', 'jmp':'01111', 'jlt':'10000', 'jgt':'10001', 'je':'10010', 'hlt':'10011'}

typea = ["00000", "00001","00110","01010","01011","01100"]

typeb = ["00010","01000","01001"]

typec = ["00011","00111","01110","01101"]

typed = ["00100","00101"]

typee = ["01111","10000","10001","10010"]
flags=[0,0,0,0]

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
    return str(str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7])


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
    return str(str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7])



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
        
    if a=="00011" :
        if reg_y == "111" :
            reg_values[pos1] = int(reg_values[7],2)
        else:
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
    return str(str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7])

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
    return str(str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7])


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
    flagger()
    d=str(str(f'{pc:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7])
    list_i0_memadd_i1_bin = [q,d]
    
    
    return list_i0_memadd_i1_bin 

def main():
    code=[]
    for line in stdin :
        if line=="":
            break
        code.append(line)
#     file = open('code.txt', 'r')
#     code = file.readlines()
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
    global count1
    count1=0
    
    global list_count
    list_count = []
    global timecount
    timecount = []
    tcount = 0 
    while k < n-1 :
        args = code[k]
        x=starter(args,count1)
        if x!=0 :
            k=x
            timecount.append(tcount)
            list_count.append(count1)
            
            
        else:
            timecount.append(tcount)
            list_count.append(count1)

        tcount=tcount + 1 
        count1=count1+1
        k += 1

    plt.plot(list_count.timecount)
    plt.xlabel("Cycle")
    plt.ylabel("Address")
    plt.title("Memory Accesses V/S Cycles")
    plt.show()
        
    zero_dump_counter = 0
    
    var=sys.stdout
    for i in code_output:
        var.write(i)
        # zero_dump_counter += 1
    for i in code:
        var.write(i)
        zero_dump_counter+=1
    print_var = list(qw.values())
    
    for x in print_var :
        
        var.write("\n")
        var.write(f'{x:016b}')
        zero_dump_counter += 1
        
    while(zero_dump_counter!=256):
        var.write("\n")
        var.write("0000000000000000")
        zero_dump_counter += 1
#     file1 = open('output.txt', 'w')
#     file1.writelines(code_output)
#     for item in code:
#         file1.writelines(item)
#         zero_dump_counter += 1
#     for x in reg_values :
#         if type(x)==str :
#             if x != "0000000000000000" :
#                 file1.writelines("\n")
#                 file1.writelines(str(f'{x:016b}'))
#                 zero_dump_counter += 1
                
#         elif str(f'{x:016b}')!="0000000000000000" :
#             file1.writelines("\n")
#             file1.writelines(str(f'{x:016b}'))
#             zero_dump_counter += 1
#         else :
#             continue 

#     while(zero_dump_counter!=256):
#         file1.writelines("\n")
#         file1.writelines("0000000000000000")
#         zero_dump_counter += 1
#     file1.close()
            
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
    
    elif args in typee :
        
        code_out = type_e(args,arg,count1)
        if code_out[0] == -1 :
            code_output.append(str(code_out[1])+"\n")
            return 0

        elif code_out[0]<=n-1 :
            code_output.append(code_out[1]+"\n")
            i= code_out[0]
            return code_out[0]

  
    elif args == "10011":
        code_output.append(str(str(f'{count1:08b}') + " " + f'{reg_values[0]:016b}' + " " + f'{reg_values[1]:016b}' + " " + f'{reg_values[2]:016b}' + " " + f'{reg_values[3]:016b}' + " " + f'{reg_values[4]:016b}' + " " + f'{reg_values[5]:016b}' + " " + f'{reg_values[6]:016b}' + " " + reg_values[7]) + "\n")
        return n
    
    else:
        code_output.append("madhav on line :" + str(count1) + "\n")
        return 0
main()

        
