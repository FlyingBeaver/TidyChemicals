import re
from django.shortcuts import render
from django.http import HttpResponse
from simple_base_project.settings import NOTATION_FOR_RENDERING
from base_app.search import find_superstructures
from base_app.render_pics import render_pics


def search_view(request):
    if request.POST:
        mol_block = request.POST["mol"]
        search_result = find_superstructures(mol_block)
        files_names = render_pics(search_result[:20])
        return render(request, "search_page_draft.html", {"images": files_names})
        # return HttpResponse(f'<h1>Ok!</h1><br>Mol file content is:'
        #                     f'<br>{request.POST["mol"]}'
        #                     f'<b><p>found {len(search_result)}</p></b>')
    else:
        return render(request, 'search_page.html')

