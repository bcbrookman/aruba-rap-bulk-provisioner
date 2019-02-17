from peewee import *

db = SqliteDatabase('inventory/inventory.db')


class Image (Model):
    partNumber = TextField(primary_key=True)
    image_path = TextField(null=True)

    class Meta:
        database = db


class Device (Model):
    serialNumber = TextField(primary_key=True)
    mac = TextField()
    apGroupName = TextField(null=True)
    deviceDescription = TextField(null=True)
    deviceFullName = TextField(null=True)
    deviceName = TextField(null=True)
    firstSeen = TextField(null=True)
    folder = TextField(null=True)
    folderId = TextField(null=True)
    inventoryDate = TextField(null=True)
    lastAosVersion = TextField(null=True)
    lastBootVersion = TextField(null=True)
    lastSeen = TextField(null=True)
    partCategory = TextField(null=True)
    partNumber = ForeignKeyField(Image, backref='devices')
    sourceIpAddress = TextField(null=True)
    status = TextField(null=True)

    class Meta:
        database = db