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
  backup_json = load_db_json()
  try:
    db = open(db_name, "w")
    json.dump(json_obj, db, indent=4)
    db.close()
  except:
    print("error writing json! restoring to backup")
    db = open(db_name, "w")
    json.dump(backup_json, db, indent=4)
    db.close()    