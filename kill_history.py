class Kill_history:
  def __init__(self, killer_id, killed_id, date_of_kill):
    self.killer_id = killer_id
    self.killed_id = killed_id
    self.date_of_kill = date_of_kill

  def get_killer_id(self):
    return self.killer_id

  def get_killed_id(self):
    return self.killed_id

  def get_date_of_kill(self):
    return self.date_of_kill

  def to_json_string(self):
    return_string = 'killer_id: {}, killed_id: {}, date_of_kill: {}'
    return (return_string.format(self.killer_id, self.killed_id, self.date_of_kill))