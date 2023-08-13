from time import time
from uuid import uuid4
import re
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.defaults import page_not_found
from base_app.models import Chemical, StoragePlace, DatabaseException
from base_app.search import find_superstructures
from base_app.rendering_paginator import (RenderingPaginator,
                                          create_svg,
                                          PICS_DIRECTORY_PATH)


HAZARD_URLS = {
    "compressed_gas": "/static/base_app/hazard_pictograms/compressed_gas.svg",
    "corrosive": "/static/base_app/hazard_pictograms/corrosive.svg",
    "environmental_hazard": "/static/base_app/hazard_pictograms/environmental_hazard.svg",
    "explosive": "/static/base_app/hazard_pictograms/explosive.svg",
    "flammable": "/static/base_app/hazard_pictograms/flammable.svg",
    "harmful": "/static/base_app/hazard_pictograms/harmful.svg",
    "health_hazard": "/static/base_app/hazard_pictograms/health_hazard.svg",
    "ionizing_radiation": "/static/base_app/hazard_pictograms/ionizing_radiation.svg",
    "oxidizing": "/static/base_app/hazard_pictograms/oxidizing.svg",
    "toxic": "/static/base_app/hazard_pictograms/toxic.svg"
}


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


def chemical_view(request, chemical_id):
    try:
        chemical = Chemical.objects.get(id=chemical_id)
        if chemical.hazard_pictograms is None:
            hazard_list = []
        else:
            hazard_list = chemical.hazard_pictograms.split(", ")
        hazards = []
        for item in hazard_list:
            hazards.append(HAZARD_URLS[item])
        picture_file = create_svg(None, chemical)
        context = {
            "chemical": chemical,
            "picture_file": picture_file,
            "hazards": hazards
        }
        return render(request, "chemical_view.html", context)
    except ObjectDoesNotExist:
        return page_not_found(request)



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
