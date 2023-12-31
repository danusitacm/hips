from django.shortcuts import render
from function.utils import execute_process
from django.contrib.auth.decorators import login_required
@login_required
def check_user_connected(request):
    """
    Verifica y muestra la lista de usuarios actualmente conectados al sistema.

    Args:
        request: La solicitud HTTP enviada por el usuario.

    Returns:
        Renderiza la página web "user_connected_verifi.html" con la información de los usuarios conectados.
    """
    command="w -h | awk '{print $1,$2,$3}'"
    list_user=execute_process(command)
    user_list = []
    if(list_user):
        print(list_user)
        for user in list_user:
            user=user.split()
            if("tty" in user[1]):
                user[2]='localhost'
            user_dicc={
                'user_name':user[0],
                'user_terminal':user[1],
                'user_ip':user[2],
            }   
            user_list.append(user_dicc)
            
        return render(request, "user_connected_verifi.html", {'users': user_list})
    else:
        message = "No se encontraron usuarios conectados en este momento."
        return render(request, "user_connected_verifi.html", {'message': message})