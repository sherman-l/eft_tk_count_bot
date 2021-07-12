class Kill_record:
  def __init__(self, user_id, user_name, kill_count):
    self.user_id = user_id
    self.user_name = user_name
    self.kill_count = kill_count
  
  def add_kill(self, kill_history):
    self.kill_count = self.kill_count + 1

  def to_json_string(self):
    return_string = 'user_id: {}, killed_id: {}, date_of_kill: {}'
    return '{' + return_string.format(self.user_id, self.user_name, self.kill_count) + '}'
