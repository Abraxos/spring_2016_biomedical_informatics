import hyperdex.client

c=hyperdex.client.Client('127.0.0.1',1984)


def getRecord(space, id):
	print("...trying to get")
	print(c.get(space,id))

getRecord("resource_compartment","1032702")
	

