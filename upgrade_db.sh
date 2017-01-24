#!/usr/bin/env bash

# by Karol Czeryna

# catch only files with ID at the beginning, max id is 999 (3 chars...) but we can tune it (change grep)


db_user='karol'
db_pass='test123'
db_name='testdb'

# run script as a root
function am_i_evil() {
  if [[ $EUID -ne 0 ]]; then
	  echo "You need to be a root to run this script!"
		exit 1
	fi
}

# fetch from db latest id of migration
function current_id() {
  echo $(mysql -N -u $db_user -p$db_pass -e 'SELECT version FROM migrations order by id desc limit 1' $db_name)
}

# show the filename with highest id
function highest_id() {
  echo $(ls sql/|grep -Eo '^[0-9]{1,3}'|tail -n1)
}

# migration function
function migration() {
  if [ $(current_id) -eq $(highest_id) ]; then
    echo 'All migrations done - database up to date!'
    exit 0
  elif [ $(highest_id) -gt $(current_id) ]; then
    for file in $(ls sql/|grep -E '^[0-9]'); do
      cur_file=$(echo $file|grep -Eo '^[0-9]{1,3}')
      if [ $cur_file -gt $(current_id) ]; then
        echo 'Adding migration:' $file
        mysql -u $db_user -p$db_pass $db_name < sql/$file
      else
        echo 'Migration already in schema' $file
      fi
      sleep 1s
      done
    fi
}

am_i_evil
migration