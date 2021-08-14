from django.shortcuts import render
from django.http import HttpResponse


def search_view(request):
    if request.POST:
        return HttpResponse(f'<h1>Ok!</h1><br>Mol file content is:'
                            f'<br>{request.POST["mol"]}')
    else:
        return render(request, 'search_page.html')

