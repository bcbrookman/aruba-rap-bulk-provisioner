from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from . models import Device


def search_index(request):
    page_context = {
        "title": "Search"
    }

    # Retrieve the query value from the URL
    query = request.GET.get('query')
    print(type(query))
    if query is not None and query != "":
        devices = Device.objects.select_related('image_path').filter(Q(deviceFullName__icontains=query) |
                                                                     Q(mac__icontains=query) |
                                                                     Q(serialNumber__icontains=query) |
                                                                     Q(deviceDescription__icontains=query) |
                                                                     Q(deviceName__icontains=query)
                                                                     ).values('apGroupName',
                                                                              'deviceDescription',
                                                                              'deviceFullName',
                                                                              'deviceName',
                                                                              'folder',
                                                                              'folderId',
                                                                              'partNumber__image_path',
                                                                              'partNumber',
                                                                              'lastAosVersion',
                                                                              'lastBootVersion',
                                                                              'lastSeen',
                                                                              'partCategory',
                                                                              'sourceIpAddress',
                                                                              'firstSeen',
                                                                              'inventoryDate',
                                                                              'mac',
                                                                              'serialNumber',
                                                                              'status',
                                                                              )
        # Store total count of results before pagination
        total_count = devices.count()
        page_context["total_count"] = total_count

        # Paginate the results
        paginator = Paginator(devices, 10)
        page = request.GET.get('page')

        # Add paginated results and the query string to the page context
        devices = paginator.get_page(page)
        page_context["devices"] = devices
        page_context["query"] = query

    return render(request, 'search/search.html', page_context)


def search_about(request):
    page_context = {
        "title": "About",
    }

    return render(request, "search/about.html", page_context)
