from django.shortcuts import redirect, render

def main(request):
    if request.user.is_authenticated:
        return redirect('/mrchampions/')
    else:
        return redirect('/mrchampions/login')
