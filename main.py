def infix_to_postfix(inf_expression):

    operators_dict = {"=":0, "(":1, "+":2 , "-":2 , "*":3, "/":3, "^":4} #Dictionary of operators and their priorities

    opstack = []
    output = []
    inf_expression = inf_expression.split(' ') #Slpit up the expression into each term
    for value in inf_expression:

        if value == "(": #If its a (, add to opstack
            opstack += str(value)
        elif value == ")": #If its a close bracket, pop from opstack until ( is found

            while opstack[len(opstack) - 1] != "(":
                b = opstack.pop()
                output.append(b)
            opstack.pop()


        elif value in operators_dict: #If the value is an operator:
            if len(opstack) > 0:
                if operators_dict[(opstack[(len(opstack) - 1)])] < operators_dict[value]: #If previous has lower  priority, add to stack
                    opstack += str(value)
                elif operators_dict[opstack[len(opstack) - 1]] >= operators_dict[value]: #If previous has higher priority or equal, pop stack until something lower is beneath, then add to stack
                    try:
                        while operators_dict[opstack[len(opstack) - 1]] >= operators_dict[value]:
                            b = opstack.pop()
                            output.append(b)
                        opstack += str(value)
                    except: #2 operators of same precedence cause crash if nothing less on stack, so continue to pop off all.
                        while len(opstack) > 0:
                            output.append(opstack.pop())
                        opstack += value
            else:
                opstack += str(value) #Add any other

        else:
            output.append(value)

    if len(opstack) > 0:
        opstack.reverse()
        output += opstack #Add all remaining values from opstack in order
    return output


def evaluate_postfix(postfix): #Function to evalutate the postfix expression
    stack = []
    ops = ['+', '-', '*', '/', '^','='] #List of operators
    for char in postfix:
        if char in ops:
            a = stack.pop()
            b = stack.pop()
            # take 2 numbers off, apply the operator, add result back to stack
            if char == '+':
                stack.append(float(b) + float(a))
            elif char == '-':
                stack.append(float(b) - float(a))
            if char == '*':
                stack.append(float(b) * float(a))
            if char == '/':
                stack.append(float(b) / float(a))
            if char == '^':
                stack.append(float(b) ** float(a))
            if char == '=':
                stack.append(float(b) == float(a))
            pass
        else:
            stack.append(char)
    return stack


def calculation_formatter(inp): #Function to put calculations into the correct format. "non" --> "n o n" and "no n" --> "n o n"
    out = ""
    ops = ['(', ')', '+', '-', '*', '/', '^','=']
    prev = ''
    for char in inp:
        if char == ' ' and prev == ' ': #If space proceeds space
            pass

        elif (char == ' ') and (prev in ops): #Space proceeds symbol
            out += char

        elif prev in ops and char in ops: #Double symbol
            out += ' ' + char

        elif (prev != ' ') and (not prev in ops) and (char in ops): #Symbol proceeds char w no space
            out += ' ' + char

        elif (prev != ' ') and (prev in ops) and (not char in ops): #Char proceeds symbol w no space
            out += ' ' + char

        else:
            out += char

        prev = char
    return out

def new_entry(question,answer): #Write an entry to the file containing the question and answer
    f = open("history.txt", "a")
    f.write(">> "+str(question) + '\n')
    f.write(""+ str(answer) + '\n \n')
    f.close()

def reset_file(): #Clear the file
    f = open("history.txt", "w")
    f.write("")

    f.close()

def modify_history(): #Allows user to see history (from file) and use commands
    print("---------------------")
    print("View History:")
    f = open("history.txt", "r")
    lines = f.readlines()
    amnt = 0

    for line in lines:
        strchar = ""
        if line[0:2] == ">>":

            amnt += 1
            char = amnt
            strchar = str(char) + str('. ')

        print(strchar + line, end='')

    f.close()
    print("Amount:",amnt)

    print("---------------------")
    print("Type a command, or enter to return to menu:")
    print("Comands: DELETE, DELETE ALL, NEWCALC")
    command = input()
    print("---------------------")
    if ("DELETE" in command):
        if ("ALL" in command):
            reset_file()
        else:
            num = int(input("QNum To Delete:"))
            deletefromfile(num)
    if (command == "NEWCALC"):
        input_calculation()



def deletefromfile(deletenum): #Function to delete a specific entry from a file
    f = open("history.txt", "r")
    newf = ""
    lines = f.readlines()
    amnt = 0
    for line in lines:
        strchar = ""
        if line[0:2] == ">>":
            amnt += 1

        if (amnt != deletenum):
            newf += line

    f.close()
    f = open("history.txt", "w")
    f.write(newf)
    f.close()
def input_calculation(): #Function to allow user to input a calculation
    print("---------------------")
    print("Input A Calculations, Type STOP To Return To Menu:")
    inp = ""
    while (inp.upper() != "STOP"):
        try:
            inp = input(">>")
            inf_expression = inp
            inp_ftd = (calculation_formatter(inf_expression))
            psf = infix_to_postfix(inp_ftd)
            val = evaluate_postfix(psf)
            ans = val[len(val) -1]
            print(ans)
            print()
            try:
                new_entry(inp_ftd, ans)
            except:
                print("Error writing to file")

        except:
            print("Unknown Error: Please try again.")


def unit_convert_calc(amount,unit1,ratio,unit2): #Function to convert beterrn a unit using a ratio
    result = float(amount) * float(ratio)
    print(f"{amount} {unit1}'s = {result} {unit2}'s" )
    try:
        new_entry(f"{amount} {unit1}'s in {unit2}'s",result)
    except:
        print("Error writing to file")

def number_base_converter(): #Function to ask a user to convert between number bases
    basefrom = int(input("Input Base To Convert From:"))
    baseto = int(input("Input Base To Convert To:"))
    num = int(input("Input Number:"))
    if basefrom == 10:
        print(base_10_to_any(baseto,num))
    else:
        inb10 = (any_to_base_to(basefrom,num))
        print(base_10_to_any(baseto,inb10))

def any_to_base_to(base, num): #Function to convert any base into base 10
    strnum = str(num)
    power = 0
    value = 0
    for char in strnum:
        n = int(char)
        value += (n * (base ** power))
        power += 1
    return value


def base_10_to_any(base,num): #Function to convert base 10 into any base
    n = num / base
    output = ""
    while (n > 0):
        n = int(num / base)
        value = num % base
        if (value > 9):
            value = chr(value + 55)
        output += str(value) + ' '

        num = n

    output = reverse_string(output)
    return output

def reverse_string(text): #Function to reverse a string
    ar = []
    out = ""
    for l in text:
        ar.append(l)
    ar.reverse()
    for i in ar:
        out += i
    return out

def unit_convert(): #Menu for converting between different units
    print("---------------------")
    print("What would you like to convert between:")
    print("1 - KG to Stone")
    print("2 - Stone to KG")
    print("3 - GB to Bytes")
    print("4 - Bytes to GB")
    print("5 - Inch to CM")
    print("6 - CM to Inch")
    print("7 - Days to Seconds")
    print("8 - Seconds to Days")
    print("9 - Number Bases")
    opt = input(">>")
    if (opt == "9"):
        number_base_converter()
    else:
        amount = input("Amount: \n>>")
        if opt == "1":
            unit_convert_calc(amount,"Kg",0.157473,"Stone")
        elif opt == "2":
            unit_convert_calc(amount,"Stone",1/0.157473,"KG")
        elif opt == "3":
            unit_convert_calc(amount,"GigaByte",1000,"Byte")
        elif opt == "4":
            unit_convert_calc(amount,"Byte",1/1000,"Gigabyte")
        elif opt == "5":
            unit_convert_calc(amount,"Inch",1/0.393701,"CM")
        elif opt == "6":
            unit_convert_calc(amount,"CM",0.393701,"Inch")
        elif opt == "7":
            unit_convert_calc(amount,"Day",86400,"Second")
        elif opt == "8":
            unit_convert_calc(amount,"Second",1/86400,"Day")


def menu(): #Main menu function
    reset_file() #Resets the file upon login since asked for as objective, could easily be removed and allowed for cross-session
    inp = ""
    while inp != "4": #Main menu system
        print("---------------------")
        print("Welcome To Calculator")
        print("1 - Enter Calculation")
        print("2 - View History")
        print("3 - Conversion Mode")
        print("4 - Quit")
        print("---------------------")
        inp = input("Input:")
        if inp == "1":
            input_calculation()
        elif inp == "2":
            modify_history()
        elif inp == "3":
            unit_convert()


if __name__ == '__main__':
    menu()


