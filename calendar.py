#! /usr/bin/python

'''Solved by looking at a month as being a padded array.  Padded because
the first and last weeks of the month may be partial ones, but need to be
represented on the calendar.'''


def startDay():
  return 5

def monthLength():
  return 30

def main():
  calendar = []
  weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
  start_day = startDay()
  month_length = monthLength()
  # START PADDING IS DEFINED BY THE START DAY
  for i in range(start_day): calendar.append(" ") 
  # ADD THE NUMBERS FOR THE MONTH
  day = 1
  while day <= month_length:
    calendar.append(day)
    day += 1
  # FIGURE OUT THE END PADDING BY DIVIDING BY 7 AND CHECKING FOR 0 REMAINDER
  while len(calendar) % 7 != 0:
    calendar.append(" ")
  # PRINT IT NICELY
  print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (weekdays[0], weekdays[1], weekdays[2], weekdays[3], weekdays[4], weekdays[5], weekdays[6])
  while calendar:
    week = calendar[0:7]
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (week[0], week[1], week[2], week[3], week[4], week[5], week[6])
    del calendar[0:7]

if __name__ == '__main__':
  main()
