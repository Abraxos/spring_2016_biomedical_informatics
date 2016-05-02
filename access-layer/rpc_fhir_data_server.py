from twisted.web import xmlrpc, server
from twisted.internet import reactor
from hyperdex.client import Client
from re import compile

RPC_URL = '127.0.0.1'
RPC_PORT = 1337
VERSION_ID_PATTERN = compile(r'.*\"versionId\"\:\"(\d+)\".*')

class FHIRQueryResult(object):
    def __init__(self, version_id, fhir_id, fhir_type, rest_date, rest_operation, content):
        self.version_id = version_id
        self.fhir_id = fhir_id
        self.fhir_type = fhir_type
        self.rest_date = rest_date
        self.rest_operation = rest_operation
        self.content = content

class FHIRRPCAccessLayer(xmlrpc.XMLRPC):
    def connect_to_hyperdex(self, url=RPC_URL, port=RPC_PORT):
        self.client = Client(RPC_URL, RPC_PORT)
        print("Connected to {0}:{1}".format(RPC_URL,RPC_PORT))

    def xmlrpc_echo(self, x):
        return x
        
    def xmlrpc_read(self, fhir_type, fhir_id):
        R = [x for x in self.client.search('resource_version',{'fhir_id':fhir_id})][0]
        m = VERSION_ID_PATTERN.match(R['content'])
        # Correct the version_id weirdness
        if m:
            R['version_id'] = int(m.group(1))
        for r in R:
            print(r,R[r])
        return R
    
if __name__ == '__main__':
    r = FHIRRPCAccessLayer()
    r.connect_to_hyperdex()
    
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()
