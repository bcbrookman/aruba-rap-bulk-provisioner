from django.shortcuts import render
from . models import Device, Image
from django.db.models import Q
from django.http import JsonResponse


def index(request):
    return render(request, 'search/search.html')


def about(request):
    return render(request, "search/about.html")


def api_search(request, query):
    result = {
        'devices': []
    }

    query = query.strip()
    resp = Device.objects.select_related('image_path').filter(Q(deviceFullName__icontains=query) |
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

    for r in resp:
        device = {
            'additionalData': {
                'apGroupName': r['apGroupName'],
                'deviceDescription': r['deviceDescription'],
                'deviceFullName': r['deviceFullName'],
                'deviceName': r['deviceName'],
                'firstSeen': r['firstSeen'],
                'folder': r['folder'],
                'folderId': r['folderId'],
                'img': r['partNumber__image_path'],
                'lastAosVersion': r['lastAosVersion'],
                'lastBootVersion': r['lastBootVersion'],
                'lastSeen': r['lastSeen'],
                'partCategory': r['partCategory'],
                'sourceIpAddress': r['sourceIpAddress'],
            },
            'firstSeen': r['firstSeen'],
            'folderId': r['folderId'],
            'inventoryDate': r['inventoryDate'],
            'lastSeen': r['lastSeen'],
            'mac': r['mac'],
            'serialNumber': r['serialNumber'],
            'partNumber': r['partNumber'],
            'status': r['status'],
        }
        result['devices'].append(device)

    # If there are no results, return Not Found error instead
    if len(result['devices']) == 0:
        result = {'error': "Not Found"}

    return JsonResponse(result)
