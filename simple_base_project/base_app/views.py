import re
from django.shortcuts import render
from django.http import HttpResponse
from base_app.search import find_superstructures


def search_view(request):
    if request.POST:
        mol_block = request.POST["mol"]
        # found = re.findall(r"V3000[^Ы]+", mol)
        # mol_block = found[0]
        # with open('out.txt', "wt", encoding="utf-8") as file:
        #    file.write(mol_block)
        search_result = find_superstructures(mol_block)
        return HttpResponse(f'<h1>Ok!</h1><br>Mol file content is:'
                            f'<br>{request.POST["mol"]}'
                            f'\n\nfound {len(search_result)}')
    else:
        return render(request, 'search_page.html')

