import xmlrpclib

s = xmlrpclib.Server('http://localhost:7080/')
print(s.read('Patient','1032702'))
