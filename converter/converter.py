import datetime
import psycopg2
import hyperdex.admin
import hyperdex.client

# Initialize hyperdex admin
a = hyperdex.admin.Admin('127.0.0.1', 1337)
c = hyperdex.client.Client('127.0.0.1', 1337)
# Connect
try:
	conn=psycopg2.connect("dbname='fhir' user='fhir' password='fhir'")
except:
	print "I am unable to connect to the database."

def convert(table,first_run):
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
#	types = []
#	for attr in rows[0]:
#		types.append(type(attr))
#	print(types)
	
	# Establish a new hyperdex space
	#if(not first_run):
#		a.rm_space(table)
	if(table == "resource_compartment"):
		s = 'space '+table+' '+\
		'key '+colnames[1] +' '+\
		'attributes string '+colnames[0]+', string '+colnames[2]+' '+\
		'subspace '+colnames[0]+' '+\
		'create 8 partitions tolerate 2 failures'
		a.add_space(s)
		for row in rows:
			c.put(table,row[1], {colnames[0]:row[0], colnames[2]:str(row[2])})
	elif(table == "resource_index_term"):
                s = 'space '+table+' '+\
                'key '+colnames[0] +' '+\
                'attributes string '+colnames[1]+', string '+colnames[2]+', string '+colnames[3]+', int '+\
		colnames[4]+', string '+colnames[5]+', float '+colnames[6]+', float '+colnames[7]+', string '+\
		colnames[8]+', string '+colnames[9]+', string '+colnames[10]+', string '+colnames[11]+', string '+\
		colnames[12]+', string '+colnames[13]+', string '+colnames[14]+', string '+colnames[15]+', string '+\
		colnames[16]+', timestamp(minute) '+colnames[17]+', timestamp(minute) '+colnames[18]+' '+\
                'subspace '+colnames[1]+' '+\
                'create 8 partitions tolerate 2 failures'
		a.add_space(s)
                for row in rows:
			long_replacements = [row[0],row[4]]
			
			for idx,entry in enumerate(long_replacements):
				if long_replacements[idx] is not None:
					long_replacements[idx] = int(entry)
				else:
					long_replacements[idx] = 0
			
			real_replacements = [row[6],row[7]]
			
			for idx,entry in enumerate(real_replacements):
                                if real_replacements[idx] is not None:
                                        real_replacements[idx] = float(entry)
                                else:
                                        real_replacements[idx] = 0.0

			string_replacements = [row[1],row[2],row[3],row[5],
			row[8],row[9],row[10],row[11],row[12],row[13],row[14],
			row[15],row[16]]

			for idx,entry in enumerate(string_replacements):
				if string_replacements[idx] is None:
					string_replacements[idx] = "isNone"
			
			date_replacements = [row[17],row[18]]
			for idx,entry in enumerate(date_replacements):
				if date_replacements[idx] is None:
					date_replacements[idx] = datetime.datetime(1970, 1, 1, 0, 0)

			c.put(table,long_replacements[0], {colnames[1]:string_replacements[0], colnames[2]:string_replacements[1],
			colnames[3]:string_replacements[2], colnames[4]:long_replacements[1], colnames[5]:string_replacements[3],
			colnames[6]:real_replacements[0], colnames[7]:real_replacements[1], colnames[8]:string_replacements[4],
			colnames[9]:string_replacements[5], colnames[10]:string_replacements[6], colnames[11]:string_replacements[7],
			colnames[12]:string_replacements[8], colnames[13]:string_replacements[9], colnames[14]:string_replacements[10],
			colnames[15]:string_replacements[11], colnames[16]:string_replacements[12], 
			colnames[17]:date_replacements[0], colnames[18]:date_replacements[1]})		
	elif(table == "resource_version"):
		s = 'space '+table+' '+\
		'key '+colnames[0]+' '+\
		'attributes string '+colnames[1]+', string '+colnames[2]+', string '+colnames[3]+', timestamp(minute)'+\
		colnames[4]+', string '+colnames[5]+' '+\
		'subspace '+colnames[1]+' '+\
		'create 8 partitions tolerate 2 failures'
		a.add_space(s)
		for row in rows:
			long_replacements = [row[0]]

			for idx,entry in enumerate(long_replacements):
				long_replacements[idx] = int(entry)
			
			c.put(table,long_replacements[0], {colnames[1]:row[1], colnames[2]:row[2],
			colnames[3]:row[3], colnames[4]:row[4], colnames[5]:row[5]})
	elif(table == "launch_context"):
		s = 'space '+table+' '+\
		'key '+colnames[0]+' '+\
		'attributes string '+colnames[1]+', timestamp(minute) '+colnames[2]+', string '+colnames[3]+', string '+\
		colnames[4]+' '+\
		'subspace '+colnames[1]+' '+\
		'create 8 partitions tolerate 2 failures'
		a.add_space(s)
		for row in rows:
			print(row)
			long_replacements = [row[0]]
			for idx,entry in enumerate(long_replacements):
				long_replacements[idx] = int(entry)

			c.put(table,long_replacements[0], {colnames[1]:row[1], colnames[2]:row[2],
			colnames[3]:row[3], colnames[4]:row[4]})
	elif(table == "launch_context_params"):
		s = 'space '+table+' '+\
		'key '+colnames[0]+' '+\
		'attributes int '+colnames[1]+', string '+colnames[2]+', string '+colnames[3]+' '+\
		'subspace '+colnames[1]+' '+\
		'create 8 partitions tolerate 2 failures'
		a.add_space(s)
		for row in rows:
			long_replacements = [row[0]]
			for idx,entry in enumerate(long_replacements):
				long_replacements[idx] = int(entry)

			c.put(table,long_replacements[0], {colnames[1]:long_replacements[1], colnames[2]:row[2],
			colnames[3]:row[3]})

	else:
		print("no conversion of this table")

convert("resource_compartment",False)
convert("resource_index_term",True)
convert("resource_version",True)
convert("launch_context",True)
convert("launch_context_params",True)
