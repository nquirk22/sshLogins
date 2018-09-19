from django.shortcuts import render

from logins.models import Fail

from django.http import HttpResponse
 
def index(request):
    #return HttpResponse("The logins index.")
    fails = Fail.objects.all()
    #print(fails)
    context = {'fails': fails}
    return render(request, 'index.html', context)

def byLogin(request, login=None):
    #print(login)
    
    #print(Fail.objects.values_list('login').distinct())
    
    logins = Fail.objects.values_list('login', flat=True).distinct()
    #print(logins)
    
    fails = None
    if login:
        fails = Fail.objects.filter(login = login).order_by('initiated')
        #print(fails)
        
    context = {
        'logins': logins,
        'fails': fails,
        'login': login
    }
    
    return render(request, 'byLogin.html', context)

def byIP(request, ip=None):
    #print(ip)
    
    #print(Fail.objects.values_list('ip').distinct())
    
    ips = Fail.objects.values_list('ip', flat=True).distinct()
    #print(ips)
    
    fails = None
    if ip:
        fails = Fail.objects.filter(ip = ip).order_by('initiated')
        #print(fails)
        
    context = {
        'ips': ips,
        'fails': fails,
        'ip': ip
    }
    
    return render(request, 'byIP.html', context)
