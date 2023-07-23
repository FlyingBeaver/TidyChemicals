from time import time
from uuid import uuid4
import re
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django import template
from base_app.models import StoragePlace, DatabaseException
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


def tree_api(request):
    if request.method != "POST":
        return HttpResponceNotAllowed(["POST"])
    if "give_root" in request.POST:
        roots = StoragePlace.objects.filter(Q(parent=None) | Q(level=0))
        if len(roots) > 1:
            raise DatabaseException(f"Two or more root storages: {roots}")
        elif len(roots) == 0:
            raise DatabaseException(f"No root storage!")
        elif len(roots) == 1:
            root = roots[0]
            return JsonResponse({root.id: [root.name, root.terminal]})
    elif "give_children_of" in request.POST:
        parent_id = int(request.POST["give_children_of"])
        try:
            parent = StoragePlace.objects.get(id=parent_id)
        except MultipleObjectsReturned:
            return JsonResponse({"error":
                                 "Multiple objects for parent"})
        except ObjectDoesNotExist:
            return JsonResponse({"error":
                                 "Parent with such id does not exist"})
        else:
            if parent.terminal:
                chemicals = Chemical.objects.filter(storage_place=parent)
                response_dict = dict()
                for chemical in chemicals:
                    response_dict[chemical.id] = chemical.name
                return JsonResponse(response_dict)
            else:
                children = StoragePlace.objects.filter(parent=parent)
                response_dict = dict()
                for child in children:
                    response_dict[child.id] = [child.name, child.terminal]
                return JsonResponse(response_dict)


def new_search(request):
    if request.method == "GET":
        return render(request, "form_vue.html")
    elif request.method == "POST":
        if "give_root" in request.POST:
            roots = StoragePlace.objects.filter(Q(parent=None) | Q(level=0))
            if len(roots) > 1:
                raise DatabaseException(f"Two or more root storages: {roots}")
            elif len(roots) == 0:
                raise DatabaseException(f"No root storage!")
            elif len(roots) == 1:
                root = roots[0]
                return JsonResponse({root.id: [root.name, root.terminal]})
        elif "give_children_of" in request.POST:
            parent_id = int(request.POST["give_children_of"])
            try:
                parent = StoragePlace.objects.get(id=parent_id)
            except MultipleObjectsReturned:
                return JsonResponse({"error":
                                     "Multiple objects for parent"})
            except ObjectDoesNotExist:
                return JsonResponse({"error":
                                     "Parent with such id does not exist"})
            else:
                if parent.terminal:
                    chemicals = Chemical.objects.filter(storage_place=parent)
                    response_dict = dict()
                    for chemical in chemicals:
                        response_dict[chemical.id] = chemical.name
                    return JsonResponse(response_dict)
                else:
                    children = StoragePlace.objects.filter(parent=parent)
                    response_dict = dict()
                    for child in children:
                        response_dict[child.id] = [child.name, child.terminal]
                    return JsonResponse(response_dict)