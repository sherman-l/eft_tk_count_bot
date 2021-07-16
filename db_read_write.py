import os
import json

db_name = "kill_db.json"

def load_db_json():
  if not os.path.isfile(db_name):
    with open(db_name, "w") as db_file:
      db_file.write(json.dumps({}))
  db = open(db_name, "r")
  json_obj = json.load(db)
  db.close()
  return json_obj
  
def write_db_json(json_obj):
  db = open(db_name, "w")
  json.dump(json_obj, db, indent=4)
  db.close()