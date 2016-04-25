import hyperdex.client

print("1.initiating client")
c=hyperdex.client.Client('127.0.0.1',1984)

print("2.trying to put")
c.put('phonebook', 'jsmith1', {'first': 'John', 'last': 'Smith', 'phone': 6075551024})

print("3.trying to get")
c.get('phonebook','jsmith1')
