class KillHistory:
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

  def to_json(self):
    json = {}
    json["killer_id"] = self.killer_id
    json["killed_id"] = self.killed_id
    json["date_of_kill"] = str(self.date_of_kill)
    return json