import hyperdex.admin

a = hyperdex.admin.Admin('127.0.0.1', 1984)
a.rm_space('phonebook')
