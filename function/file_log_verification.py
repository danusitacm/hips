import logs
from utils import write_to_file,execute_process,file_to_list
import os
path_hosts_allow="/etc/hosts.allow"
path_hots_deny="etc/hosts.deny"

path_hosts_allow=file_to_list(path_hosts_allow)
path_hots_deny=file_to_list(path_hots_deny)

def get_dict(log):
    log=log.split()
    log_result={
        'uid': '',
        'tty': '',
        'ruser': '',
        'rhost': '',
        'user': ''
    }
    for word in log[9:]:
        for key in log_result:
            if key in word:
                log_result[key]=word.split("=")[1]           
    return log_result  

def login_auth(dic_log,user_count_login):
    try: 
        user = dic_log['user']
        user_count_login[user] = user_count_login.get(user, 0) + 1
        if(user_count_login[user]>=3):
            logs.log_alarm(f"Autenticacion fallida","",f"Se itento acceder "+ str(user_count_login[user])+f" veces en el user: { user }")
            print(f"Autenticacion fallida","",f"Se itento acceder "+ str(user_count_login[user])+f" veces en el user: { user }")
            print("Al 5to intento se bloqueara el usuario")
        elif(user_count_login[user]==5):
            os.system(f"usermod -L {user}")
            print(f"Se bloqueo el usuario {user}. Comunicarse con admin para desbloquear el user")
            logs.log_prevention(f"Autenticacion fallida MASIVA","",f"Se bloqueo el usuario {user} al llegar a la cantidad maximas de intentos")
        return user_count_login
    except Exception as e:
        print(e)

def su_auth(dic_log,user_count_su):
    try:
        ruser=dic_log['ruser']
        user_count_su[ruser] = user_count_su.get(ruser, 0) + 1
        if(user_count_su[ruser]>=3):
            logs.log_alarm(f"Autenticacion fallida","",f"Se detecto que el user { ruser } intento acceder "+ str(user_count_su[ruser])+" veces en otro usuario")
            print(f"Autenticacion fallida","",f"Se detecto que el user { ruser } intento acceder "+ str(user_count_su[ruser])+" veces en otro usuario")
            print("Al 5to intento se bloqueara el usuario")
        elif(user_count_su[ruser]==5):
            os.system(f"usermod -L {ruser}")
            print(f"Se bloqueo el usuario {ruser}. Comunicarse con admin para desbloquear el user")
            logs.log_prevention(f"Autenticacion fallida MASIVA","",f"Se bloqueo el usuario {ruser} al llegar a la cantidad maximas de intentos")
        return user_count_su
    except Exception as e:
        print(e)

def check_authentication_failure():
    try:
        user_count_login = {}
        user_count_su = {}
        command_auth="cat /var/log/secure | grep -i \":auth\" |grep -i \"authentication failure\" "
        output=execute_process(command_auth)
        for log in output:
            if "login:auth" in log:
                print("Auth login")
                user_count_login=login_auth(get_dict(log),user_count_login)
            elif "su-l:auth" in log:
                print("Auth su")
                user_count_su=su_auth(get_dict(log),user_count_su)
    except Exception as error:
      print('Error al verificar el /var/log/secure',error)
    

def check_access_httpd_error():
    pass
def check_massive_email():
    pass

check_authentication_failure()