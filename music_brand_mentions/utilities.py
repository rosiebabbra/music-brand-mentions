from datetime import date, timedelta 
  
def retrieve_saturday_dates(year): 

    d = date(year, 1, 1)
    d += timedelta(days = 5 - d.weekday() + 7 % 7)

    while d.year == year: 
        yield d 
        d += timedelta(days = 7)