from openpyxl import Workbook, load_workbook
from lunarPhases import determineLunarPhase
from jm_lunar import periApo, earthMoonDistance
from astro_functions import toGregorian, daysSinceNewYears, julianDay
import matplotlib
from matplotlib import pyplot as plt

def dateComparison(jde1, jde2):
	return None

def convertToFullGregDate(gregorianDate):
	return None

def generateColumnData(iterations,julianDate):
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	wbk = Workbook()
	sht = wbk.active
	sht['B2'] = 'Date of Full Moon (JDE)'
	sht['C2'] = 'Gregorian Calendar Date'
	sht['D2'] = 'Date of Perigee (JDE)'
	sht['E2'] = 'Gregorian Calendar Date'
	sht['G2'] = 'Earth - Moon Distance'
	sht['H2'] = 'Absolute Value Difference between dates'
	month = toGregorian(julianDate)[0]
	day = toGregorian(julianDate)[1]
	year = toGregorian(julianDate)[2]
	for i in range(0,iterations):
		fullMoonJDE = determineLunarPhase(month,day+29.53059*i,year,0.5)
		yearWithDecimals = round(year+daysSinceNewYears(month,day+29.53059*i,year)/365.25,6)
		sht['B'+str(3+i)] = fullMoonJDE
		fullMoonGregorianDate = toGregorian(fullMoonJDE)
		printDate = f"{str(months[fullMoonGregorianDate[0]-1])}" + " " + f"{str(int(round(fullMoonGregorianDate[1],0)))}" + " " + f"{str(fullMoonGregorianDate[2])}"
		sht['C'+str(3+i)] = printDate

		periApoDateJDE = periApo(yearWithDecimals)
		periApoDateGregorian = toGregorian(periApoDateJDE)
		printPeriApoDate = f"{str(months[periApoDateGregorian[0]-1])}" + " " + f"{str(int(round(periApoDateGregorian[1],0)))}" + " " + f"{str(periApoDateGregorian[2])}"
		sht['D'+str(3+i)] = periApoDateJDE
		sht['E'+str(3+i)] = printPeriApoDate
		sht['G'+str(3+i)] = earthMoonDistance(month,day+29.53059*i,year)
		sht['H'+str(3+i)] = round(abs(sht['B'+str(3+i)].value - sht['D'+str(3+i)].value),3)
	wbk.save('/home/sdl5384/Desktop/Astronomy/Super Blue Moons.xlsx')

def main():
	month = 7
	day = 13
	year = 2023

	generateColumnData(2000,julianDay(month,day,year))

main()