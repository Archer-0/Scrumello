from django.shortcuts import render


def about(request):
    # HttpResponseRedirect("/welcome/")
    return render(request, 'about.html')