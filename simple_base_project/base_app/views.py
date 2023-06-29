from time import time
from uuid import uuid4
import re
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from django import template
from base_app.search import find_superstructures
from base_app.rendering_paginator import RenderingPaginator


register = template.Library()


@register.filter()
def filename_item(page_obj):
    return page_obj.filename_item()


def process_mol_block(mol_block, request, page_number=1):
    search_result = find_superstructures(mol_block)
    query_id = str(uuid4())
    paginator = RenderingPaginator(search_result, 20)
    page_obj = paginator.get_page(page_number)
    cache.set(query_id, paginator, 1800)
    cache.set(query_id + "_post", request.POST, 12 * 3600)
    return render(request,
                  "search_page_pagination.html", 
                  {"page_obj": page_obj,
                   "query_id": query_id})


def search_view(request):
    if request.POST and "query_id" not in request.POST:
        mol_block = request.POST["mol"]
        return process_mol_block(mol_block, request)
    elif request.POST and "query_id" in request.POST:
        query_id = request.POST["query_id"]
        page_number = int(request.POST["page_no"])
        paginator = cache.get(query_id, "expired")
        if paginator != "expired":
            page_obj = paginator.get_page(page_number)
            return render(request,
                          "search_page_pagination.html",
                          {"page_obj": page_obj,
                           "query_id": query_id})
        else:
            post_dict = cache.get(query_id + "_post", "expired")
            page_number = int(request.POST["page_no"])
            if post_dict != "expired":
                mol_block = post_dict["mol"]
                return process_mol_block(mol_block, request, page_number=page_number)
            else:
                return render(request,
                              "search_results_deleted.html")
    else:
        return render(request, 'search_page.html')
