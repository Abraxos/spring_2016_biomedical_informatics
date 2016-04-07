import datetime
import psycopg2
import hyperdex.admin
import hyperdex.client

# Initialize hyperdex admin
a = hyperdex.admin.Admin('127.0.0.1', 1984)
c = hyperdex.client.Client('127.0.0.1', 1984)
# Connect
try:
	conn=psycopg2.connect("dbname='fhir' user='fhir' password='fhir'")
except:
	print "I am unable to connect to the database."

def convert(table):
	# Execute Query
	cur = conn.cursor()
	try:
		query = "SELECT * from " + table
		cur.execute(query)
	except:	
		print "I can't SELECT from " + table

	# Output entries to  rows
	rows = cur.fetchall()

	# Output column names
	colnames = [desc[0] for desc in cur.description]
	
	# for dev (can delete after)
#	print(colnames)
#	print(rows[0])
#	types = []
#	for attr in rows[0]:
#		types.append(type(attr))
#	print(types)
	
	# Establish a new hyperdex space
	a.rm_space(table)
	if(table == "resource_compartment"):
		s = 'space '+table+' '+\
		'key '+colnames[1] +' '+\
		'attributes string '+colnames[0]+', list(string) '+colnames[2]+' '+\
		'subspace '+colnames[0]+' '+\
		'create 8 partitions tolerate 2 failures'
		a.add_space(s)
		for row in rows:
			c.put(table,row[1], {colnames[0]:row[0], colnames[2]:row[2]})
	elif(table == "resource_index_term"):
                s = 'space '+table+' '+\
                'key '+colnames[0] +' '+\
                'attributes string '+colnames[1]+', string '+colnames[2]+', string '+colnames[3]+', int '+\
		colnames[4]+', string '+colnames[5]+', int '+colnames[6]+', int '+colnames[7]+', string '+\
		colnames[8]+', string '+colnames[9]+', string '+colnames[10]+', string '+colnames[11]+', string '+\
		colnames[12]+', string '+colnames[13]+', string '+colnames[14]+', string '+colnames[15]+', string '+\
		colnames[16]+', timestamp(second) '+colnames[17]+', timestamp(second) '+colnames[18]+' '+\
                'subspace '+colnames[1]+' '+\
                'create 8 partitions tolerate 2 failures'
		a.add_space(s)
                for row in rows:
			replacements = [row[0],row[4],row[6],row[7]]
			if replacements[0] is not None:
				replacements[0] = int(replacements[0])
			if replacements[1] is not None:
				replacements[1] = int(replacements[1])
			if replacements[2] is not None:
				replacements[2] = int(replacements[2])
			if replacements[3] is not None:
				replacements[3] = int(replacements[3])

                        c.put(table,replacements[0], {colnames[1]:row[1], colnames[2]:row[2],
			colnames[3]:row[3], colnames[4]:replacements[1], colnames[5]:row[5],			
			colnames[6]:replacements[2], colnames[7]:replacements[3], colnames[8]:row[8],
			colnames[9]:row[9], colnames[10]:row[10], colnames[11]:row[11],
			colnames[12]:row[12], colnames[13]:row[13], colnames[14]:row[14],
			colnames[15]:row[15], colnames[16]:row[16], colnames[17]:row[17],
			colnames[18]:row[18]})		
	elif(table == "resource_version"):
		print("_")
	elif(table == "launch_context"):
		print("_")
	elif(table == "launch_context_params"):
		print("_")
	else:
		print("no conversion of this table")

#convert("resource_compartment")
convert("resource_index_term")
#convert("resource_version")
#convert("launch_context")
#convert("launch_context_params")