 QUEUE INSERT AT END DELETE AT BEGINING

import sys as s
    
def en_queue():
    value = int(input('Enter the value to be added :'))
    queue.append(value)
    print(f'The value {value} is inserted')
    
def de_queue():
    print(f'the value {queue[-1]} is removed ')
    del queue[0]
    
def view():
    print(queue)

def invalid_choice():
    print('invalid choice')
    
def exit():
    s.exit('print the program has ended successfully')
    
menu = {
    1 : en_queue,
    2 : de_queue,
    3 : view,
    4 : exit
}
queue=[]
while True:
        print('1 : insert  2: delete  3:view  4:exit')
        choice = int(input('Enter your choice please :'))
        menu.get(choice,invalid_choice)()
        
        
        