class Config:
  def __init__(self, quotechar, delimiter, ignore_header, schema, log_to_file, logfile):
    self.quotechar = quotechar
    self.delimiter = delimiter
    self.ignore_header = ignore_header
    self.schema = schema
    self.logfile = logfile
    self.log_to_file = log_to_file