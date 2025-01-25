from datetime import datetime

def ym() -> tuple[str, str]:
  return datetime.now().strftime("%Y"), datetime.now().strftime("%m")

def ymd() -> tuple[str, str, str]:
  return datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d")

def datetime_string() -> str:
  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def datetime_string_for_filename() -> str:
  return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def date_string() -> str:
  return datetime.now().strftime("%Y-%m-%d")