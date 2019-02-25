from django.db import models


class Image(models.Model):
    partNumber = models.TextField(primary_key=True)
    image_path = models.TextField(null=True)


class Device(models.Model):
    serialNumber = models.TextField(primary_key=True)
    mac = models.TextField()
    apGroupName = models.TextField(null=True)
    deviceDescription = models.TextField(null=True)
    deviceFullName = models.TextField(null=True)
    deviceName = models.TextField(null=True)
    firstSeen = models.TextField(null=True)
    folder = models.TextField(null=True)
    folderId = models.TextField(null=True)
    inventoryDate = models.TextField(null=True)
    lastAosVersion = models.TextField(null=True)
    lastBootVersion = models.TextField(null=True)
    lastSeen = models.TextField(null=True)
    partCategory = models.TextField(null=True)
    partNumber = models.ForeignKey(Image, on_delete=models.CASCADE)
    sourceIpAddress = models.TextField(null=True)
    status = models.TextField(null=True)
