INSERT IN THE END(STACK)

import sys as s

def push():
    n = int(input('Enter the value to push :'))
    stack.append(n)
    print("The element is added successfully")

def pop():
    stack.remove(stack[-1])
    print('The top value is popped successfully')

def view():
    print(stack)

def invalid_choice():
    print("invalid_choice")

def exit():

   s.exit('program is ended successfully')


menu = {
    1 : push,
    2 : pop,
    3 : view,
    4 : exit
}

stack = []
while True:
    
    print('1:push 2:pop 3:view 4:exit')
    choice = int(input('Your choice Plz: '))
    menu.get(choice, invalid_choice) ()
    