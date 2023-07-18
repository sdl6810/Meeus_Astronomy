import math
from datetime import date, datetime

def julianDay(month, day, year):
	a = int(year/100)
	b = 2 - a + int(a/4)

	jd = int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + b - 1524.5
	return jd

def toGregorian(julianDate):
	julianDate = julianDate + 0.5
	z = int(julianDate)
	f = julianDate - z

	alpha = int((z - 1867216.25)/36524.25)
	a = z + 1 + alpha - int(alpha/4)

	b = a + 1524
	c = int((b - 122.1)/365.25)
	d = int(365.25*c)
	e = int((b - d)/30.6001)

	date = b - d - int(30.6001*e) + f
	month = None
	year = None

	if e < 14:
		month = e - 1
	elif e == 14 or e == 15:
		month = e - 13

	if month > 2:
		year = c - 4716
	elif month == 1 or month == 2:
		year = c - 4715

	return [month, date, year]

def isALeapYear(year):
	outcome = False
	if year%4 == 0:
		outcome = True
	elif year%100 == 0:
		outcome = True
	elif year%400 == 0:
		outcome = True
	else:
		outcome = False
	return outcome

def reduceAngle(angle):
	return angle - 360*math.floor(angle/360)

def daysSinceNewYears(month,day,year):
	#make this list a global variable
	months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if isALeapYear(year):
		months[1] = months[1] + 1

	#count days backward from today to January 1
	i = 1
	dayCount = day
	while i < month:
		dayCount = dayCount + months[i-1]
		if (i == month):
			dayCount = dayCount + day
		i = i + 1

	return dayCount

#result is accurate up to two decimal places
#needs to be accurate up to six decimal places
def daysSinceEpoch(epochJD,currentJD):
	count = 0
	if currentJD > epochJD:
		while (epochJD < currentJD):
			if isALeapYear(epochJD):
				count = count + 1
			else:
				count = count + 365
			epochJD = epochJD + 1
	elif currentJD < epochJD:
		while (epochJD > currentJD):
			if isALeapYear(epochJD):
				count = count - 1
			else:
				count = count - 365
			epochJD = epochJD - 1
	return count/365.224599

def determineCalendarDateFromDecimalYr(year):
	yearFrac = year - int(year)
	daysPassed = yearFrac*365.25
	gregMonth = None

	#make this list a global variable
	i = 0
	months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	gregMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	while daysPassed >= 31:
		daysPassed = daysPassed - months[i]
		i = i + 1

	calendarDate = [gregMonths[i], round(daysPassed,6), int(year)]

	return calendarDate

def determine_deltaT(m,d,y):
	deltaT = 0.0
	t = (y - 2000)/100

	if t < 948:
		deltaT = 2177 + 497*t + 44.1*t*t
	elif 948 <= y <= 1600 or y > 2000:
		deltaT = 102 + 102*t + 25.3*t*t
		correction = 0.37*(y - 2100)
		deltaT = deltaT + correction
	else:
		return 0