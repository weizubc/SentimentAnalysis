import urllib2


def get_next_target(page):
      start_link = page.find('<td')
      if start_link == -1:
          return None, 0
      start_quote = page.find('>', start_link)
      end_quote = page.find('</td>', start_quote + 1)
      cell = page[start_quote + 1:end_quote]
      valuecheck = cell.find('wx-value')
      if valuecheck != -1:
          start = page.find('>', valuecheck)
          end = page.find('<', start + 1)
          cell = page[start + 1:end]
      else:
           if cell.find('\n') != -1:
               cell = '99999'
      return cell, end_quote


def get_all_cells(page):
      delete = (page.find('Windchill') != -1)
      #some pages do not report Windchill column, need to drop the column to be consistent
      start = page.find('Hourly Weather History')
      page = page[start:]
      clist = []
      while True:
          cell, endpos = get_next_target(page)
          if cell:
              clist.append(cell)
              page = page[endpos:]
          else:
              break
      return clist, delete


def dailyweather(month,day):
    url = 'https://www.wunderground.com/history/airport/KSFO/2017/' + str(month) + '/' + str(day) +'/DailyHistory.html'
    response = urllib2.urlopen(url)
    page = response.read()
    toprint,delete = get_all_cells(page)

    if delete:
        nrows = len(toprint)/13
        for i in range(nrows):
            #skip the windchill column
            row = toprint[i*13:i*13+2]+toprint[i*13+3:(i+1)*13]
            print str(month) + ',' + str(day) + ',' +','.join(row)
    else:
        nrows = len(toprint)/12
        for i in range(nrows):
            row = toprint[i*12:(i+1)*12]
            print str(month) + ',' + str(day) + ',' +','.join(row)



calendar = []
for month in range(1,13):
    days = 30
    if month in (1,3,5,7,8,10,12):
        days = 31
    if month == 2:
        #might add leap year option here.
        days = 28
    for day in range(1,days+1):
        calendar.append((month,day))


def printout(start,end):
    dates = calendar[start:end+1]
    for date in dates:
        month, day = date
        dailyweather(month,day)


start = calendar.index((2,24))
#input start/end date as a tuple, the printout function would report all the data within the period
end = calendar.index((4,3))
print 'month,day,time,temp,dew,humidity,pressure,visibility,winddir,windspeed,gustspeed,precip,events,conditions'
printout(start,end)


#python crawl.py  > weather.csv


