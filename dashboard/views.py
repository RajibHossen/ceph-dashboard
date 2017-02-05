from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login

def index(request):
    template = loader.get_template('index.html')
    context = {
        'user':request.user,
    }
    output = template.render(context,request)
    return HttpResponse(output)

#def login_user(request):
#    username = request.POST['username']
#    password = request.POST['password']
#
#    user = authenticate(username=username,password=password)
#    if user in not None:
#        login(request,user)
#        redirect_to = reverse("home")
#        return HttpResponseRedirect(redirect_to)
#    else:
#        redirect_to = reverse("login")
#        return HttpResponseRedirect(redirect_to)


