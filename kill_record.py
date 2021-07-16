class KillRecord:
  def __init__(self, user_id, user_name, kill_count):
    self.user_id = user_id
    self.user_name = user_name
    self.kill_count = kill_count
  
  def from_json(cls, record_as_json: str):
  	record = json.loads(record_as_json)
  	return cls(user_id=record['user_id'], user_name=record['user_name'], kill_count=record['kill_count'])  

  def to_json(self):
    json = {}
    json["user_id"] = self.user_id
    json["user_name"] = self.user_name
    json["kill_count"] = self.kill_count
    return json
