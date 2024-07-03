from datetime import datetime

# Получение текущего времени и даты
def get_now_time():
  now = datetime.now()
  formatted_date = now.strftime("%H:%M / %d%B %Y")
  formatted_date = formatted_date.lower().replace(" ", "")
  months = {'january':'января', 'february':'февраля', 
            'march':'марта', 'april':'апреля',
            'may':'мая', 'june':'июня',
            'july':'июля', 'august':'августа',
            'september':'сентября', 'october':'октября',
            'november':'ноября', 'december':'декабря'}
  for ang, rus in months.items():
    formatted_date = formatted_date.replace(ang, rus)
  return formatted_date