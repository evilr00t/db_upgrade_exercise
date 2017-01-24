#!/usr/bin/env python

  
import os
import re
import subprocess
import collections
import sys

db_user='karol'
db_pass='test123'
db_name='testdb'

if sys.platform == 'win32':
  current_id = "\"C:/Program Files/MySQL/MySQL Server 5.6/bin/mysql.exe\" -N -u {} -p{} -e \"SELECT version FROM migrations order by id desc limit 1\" {}".format(db_user, db_pass, db_name)
else:
  current_id = "mysql -N -u {} -p{} -e 'SELECT version FROM migrations order by id desc limit 1' {} 2>/dev/null".format(db_user, db_pass, db_name)

p = subprocess.Popen(current_id,stdout=subprocess.PIPE,shell=True)
current_id,stderr = p.communicate()
retcode = p.wait()
  
#if retcode != 0:
#  print 'Please check your credentials...'
#  os._exit(1)

print 'Current migration id: %s' % current_id
id_migrations = {}

# fetch current migration files in sql/ 
# they will be matched using regex...
# migration files need to start with id
# i.e. 10-added-index.sql
for f in os.listdir('sql/'):
   match = re.search(r'^[0-9]{1,5}', f) 
   if match is not None and f.endswith('.sql'):
     id_migrations[int(match.group())] = f

# sort our id list
id_migrations = collections.OrderedDict(sorted(id_migrations.items()))

for k, v in id_migrations.iteritems():
  if int(id_migrations.keys()[-1]) == int(current_id):
    print 'All migrations applied... nothing to do!'
    os._exit(0)
  if int(k) > int(current_id):
    print 'Applying {} migration'.format(v)
    if sys.platform == 'win32':
      restore_db = "\"C:/Program Files/MySQL/MySQL Server 5.6/bin/mysql.exe\" -u {} -p{} {} < sql/{}".format(db_user, db_pass, db_name, v)
    else:
      restore_db = "mysql -u {} -p{} {} < sql/{} 2>/dev/null".format(db_user, db_pass, db_name, v)
    
    p = subprocess.Popen(restore_db,stdout=subprocess.PIPE,shell=True)
    stdout,stderr = p.communicate()
    retcode = p.wait()
    if retcode != 0:
      print 'Something went wrong with SQL... check your migration file!'
      os._exit(1)
