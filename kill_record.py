class Kill_record:
  def __init__(self, user_id, user_name, kill_count):
    self.user_id = str(user_id)
    self.user_name = user_name
    self.kill_count = kill_count
  
  def from_json(cls, record_as_json: str):
  	record = json.loads(record_as_json)
  	return cls(user_id=record['user_id'], user_name=record['user_name'], kill_count=record['kill_count'])  

  def to_json_string(self):
    return_string = '"user_id": "{}", "killed_id": "{}", "kill_count": "{}""'
    return ('{' + return_string.format(self.user_id, self.user_name, self.kill_count) + '}')
