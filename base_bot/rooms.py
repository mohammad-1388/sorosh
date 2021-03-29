import csv
from os import chdir , remove

def writer (text , loc , back_salsh=True , mode='a'):
    with open(loc , mode) as file:
        file.write(text)
        if back_salsh:
            file.write('\n')
        file.close()

def random_string ():
    from string import ascii_letters
    from random import choice
    return ''.join(choice(ascii_letters) for i in range(10))

def create_room ():
    try:
        chdir('base_bot/server_tmp/')
    except:
        pass

    x = random_string() + '.csv'
    with open(x , 'w+') as f:
        f.close()
    writer(x , 'server_list.txt')
    return x

def find_room (user_id):
    try:
        chdir('base_bot/server_tmp/')
    except:
        pass

    loc = 0

    with open('server_list.txt' , 'r+') as list_server:
        list_server = list_server.readlines()
        for har_server in list_server:
            har_server = har_server.strip('\n')
            with open(har_server , 'r') as csv_tmp:
                csv_text = csv_tmp.readlines()
                if len(csv_text) <= 6:
                    writer(user_id , har_server)
                    loc = har_server
                    csv_tmp.close()
                    return loc
                else:
                    csv_tmp.close()
        if loc == 0:
            tmp = create_room()
            writer(user_id , tmp)
            loc = tmp

        return loc

def delete_room (loc):
    try:
        chdir('base_bot/server_tmp/')
    except:
        pass

    remove(loc)
    with open ('server_list.txt' , 'r+') as server_list:
        lines = server_list.readlines()
        server_list.close()
    with open ('server_list.txt' , 'w') as server_list:
        for line in lines:
            if line.rstrip() != loc:
                server_list.write(line)

