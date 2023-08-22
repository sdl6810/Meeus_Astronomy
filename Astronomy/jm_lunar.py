import math
from astro_functions import julianDay, toGregorian, reduceAngle, daysSinceNewYears
from datetime import datetime, date
import openpyxl
from openpyxl import load_workbook
from general_util import importXlColumnToPythonList

_date = date.today()

def determine_T_value(yearInJD):
	return (yearInJD - 2451545)/36525

#variable is L'
def lunarMeanLongitude(T):
	return 218.3164477 + 481267.88123421*T - 0.0015786*T*T + (T*T*T)/545868 - (T*T*T*T)/65194000

#variable is D
def lunarMeanElongation(T):
	return 297.8501921 + 445267.1114034*T - 0.0018819*T*T + (T*T*T)/545868 - (T*T*T*T)/113065000

#variable is M
def solarMeanAnomaly(T):
	return 357.5291092 + 35999.0502909*T - 0.0001536*T*T + (T*T*T)/24490000

#variable is M'
def lunarMeanAnomaly(T):
	return 134.9633964 + 477198.8675055*T + 0.0087414*T*T + (T*T*T)/69699 - (T*T*T*T)/14712000

#variable is F
def lunarArgOfLatitute(T):
	return 93.2720950 + 483202.0175233*T - 0.0036539*T*T - (T*T*T)/3526000 + (T*T*T*T)/863310000

def furtherArguments(T):
	A = []
	A.append(math.radians(round(reduceAngle(119.75 + 131.849*T),2)))
	A.append(math.radians(round(reduceAngle(53.09 + 479264.290*T),2)))
	A.append(math.radians(round(reduceAngle(313.45 + 481266.484*T),2)))
	return A

def eccentricity(T):
	return 1 - 0.002516*T - 0.0000074*T*T

def earthMoonDistance(m,d,y):
	jd = julianDay(m,d,y)
	t = round(determine_T_value(jd),12)
	e = round(eccentricity(t),6)

	lPrime = math.radians(round(reduceAngle(lunarMeanLongitude(t)),6))
	D = math.radians(round(reduceAngle(lunarMeanElongation(t)),6))
	m = math.radians(round(reduceAngle(solarMeanAnomaly(t)),6))
	mPrime = math.radians(round(reduceAngle(lunarMeanAnomaly(t)),6))
	f = math.radians(round(reduceAngle(lunarArgOfLatitute(t)),6))

	args = furtherArguments(t)

	earthBk = load_workbook('/home/sdl5384/Desktop/Python_SRC/Astronomy/earthMoonData.xlsx')

	lunarData = earthBk['LBR_Moon']

	luna_lSum = 0.0
	luna_bSum = 0.0
	luna_rSum = 0.0

	for j in range(0,60):
		if abs(lunarData['E'+str(4+j)].value) != 1 and abs(lunarData['E'+str(4+j)].value) != 2:
			luna_lSum = luna_lSum + lunarData['B'+str(4+j)].value*math.sin(lunarData['D'+str(4+j)].value*D+lunarData['E'+str(4+j)].value*m+lunarData['F'+str(4+j)].value*mPrime+lunarData['G'+str(4+j)].value*f)
		if abs(lunarData['E'+str(4+j)].value) == 1:
			luna_lSum = luna_lSum + lunarData['B'+str(4+j)].value*e*math.sin(lunarData['D'+str(4+j)].value*D+lunarData['E'+str(4+j)].value*m+lunarData['F'+str(4+j)].value*mPrime+lunarData['G'+str(4+j)].value*f)
		if abs(lunarData['E'+str(4+j)].value) == 2:
			luna_lSum = luna_lSum + lunarData['B'+str(4+j)].value*(e*e)*math.sin(lunarData['D'+str(4+j)].value*D+lunarData['E'+str(4+j)].value*m+lunarData['F'+str(4+j)].value*mPrime+lunarData['G'+str(4+j)].value*f)	

	luna_lSum = round(luna_lSum + 3958*math.sin(args[0]) + 1962*math.sin(lPrime - f) + 318*math.sin(args[1]),0)

	for k in range(0,60):
		if abs(lunarData['I'+str(4+k)].value) != 1 and abs(lunarData['I'+str(4+k)].value) != 2:
			luna_bSum = luna_bSum + lunarData['I'+str(4+k)].value*math.sin(lunarData['J'+str(4+k)].value*D+lunarData['K'+str(4+k)].value*m+lunarData['L'+str(4+k)].value*mPrime+lunarData['M'+str(4+k)].value*f)
		if abs(lunarData['I'+str(4+k)].value) == 1:
			luna_bSum = luna_bSum + lunarData['I'+str(4+k)].value*e*math.sin(lunarData['J'+str(4+k)].value*D+lunarData['K'+str(4+k)].value*m+lunarData['L'+str(4+k)].value*mPrime+lunarData['M'+str(4+k)].value*f)
		if abs(lunarData['I'+str(4+k)].value) == 2:
			luna_bSum = luna_bSum + lunarData['I'+str(4+k)].value*(e*e)*math.sin(lunarData['J'+str(4+k)].value*D+lunarData['K'+str(4+k)].value*m+lunarData['L'+str(4+k)].value*mPrime+lunarData['M'+str(4+k)].value*f)

	luna_bSum = int(luna_bSum - 2235*math.sin(lPrime) + 382*math.sin(args[2]) + 175*math.sin(args[0]-f) + 175*math.sin(args[0]+f) + 127*math.sin(lPrime - mPrime) - 115*math.sin(lPrime + mPrime))

	luna_rSum = 0.0
	for r in range(0,60):
		if abs(lunarData['E'+str(4+r)].value) != 1 and abs(lunarData['E'+str(4+r)].value) != 2:
			luna_rSum = luna_rSum + lunarData['C'+str(4+r)].value*math.cos(lunarData['D'+str(4+r)].value*D+lunarData['E'+str(4+r)].value*m+lunarData['F'+str(4+r)].value*mPrime+lunarData['G'+str(4+r)].value*f)
		if abs(lunarData['E'+str(4+r)].value) == 1:
			luna_rSum = luna_rSum + lunarData['C'+str(4+r)].value*e*math.cos(lunarData['D'+str(4+r)].value*D+lunarData['E'+str(4+r)].value*m+lunarData['F'+str(4+r)].value*mPrime+lunarData['G'+str(4+r)].value*f)
		if abs(lunarData['E'+str(4+r)].value) == 2:
			luna_rSum = luna_rSum + lunarData['C'+str(4+r)].value*(e*e)*math.cos(lunarData['D'+str(4+r)].value*D+lunarData['E'+str(4+r)].value*m+lunarData['F'+str(4+r)].value*mPrime+lunarData['G'+str(4+r)].value*f)

	#inaccurate coordinates
	# _lambda = lPrime + (luna_lSum/1000000)
	# beta = luna_bSum/1000000

	#print(math.degrees(_lambda), math.degrees(beta))
	#in kilometers
	moonEarthDistanceInKm = round(385000.56 + (luna_rSum/1000),1)
	moonEarthDistanceInMi = round(moonEarthDistanceInKm/1.609344,2)

	return moonEarthDistanceInMi

#set at low accuracy for right now
#lunar and solar coordinates need to be calculated for higher accuracy
def illuminatedFraction(jd):
	T = determine_T_value(jd)
	mPrime = math.radians(round(reduceAngle(lunarMeanAnomaly(T)),6))
	M = math.radians(round(reduceAngle(solarMeanAnomaly(T)),6))

	D = round(reduceAngle(lunarMeanElongation(T)),6)
	#use D in degrees to subtract from 180
	i = 180 - D

	#then convert D to radians to use in trig functions
	D = math.radians(round(reduceAngle(lunarMeanElongation(T)),6))

	#i is measured in degrees, but angles need to be converted to radians so they can be used in trig functions

	i = i - 6.289*math.sin(mPrime) + 2.100*math.sin(M) - 1.274*math.sin(2*D - mPrime) - 0.658*math.sin(2*D) - 0.214*math.sin(2*mPrime) - 0.110*math.sin(D)
	i = round(reduceAngle(i),2)
	i = math.radians(i)

	litFraction = round((1 + math.cos(i))/2,4)

	return litFraction

def periApo(year):
	k = int((year - 1999.97)*13.255)
	T = round((k/1325.55),6)

	jde = round(2451534.6698 + 27.55454989*k - 0.0006691*(T*T) - 0.000001098*(T*T*T) + 0.0000000052*(T*T*T*T),4)

	D = round(reduceAngle(round(171.9179 + 335.9106046*k - 0.0100383*(T*T) - 0.00001156*(T*T*T) + 0.000000052*(T*T*T*T),4)),4)

	M = round(reduceAngle(round(347.3477 + 27.1577721*k - 0.0008130*(T*T) - 0.0000010*(T*T*T),4)),4)

	F = round(reduceAngle(round(316.6109 + 364.5287911*k - 0.0125053*(T*T) - 0.0000148*(T*T*T),4)),4)

	sum_corrections = 0.0
	coeffs = importXlColumnToPythonList('/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx','periApo','B',0)
	d_coeffs = importXlColumnToPythonList('/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx','periApo','C',0)
	f_coeffs = importXlColumnToPythonList('/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx','periApo','D',0)
	m_coeffs = importXlColumnToPythonList('/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx','periApo','E',0)
	t_coeffs = importXlColumnToPythonList('/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx','periApo','F',0)

	for i in range(0,len(coeffs)):
		sum_corrections = sum_corrections + coeffs[i]*math.sin(d_coeffs[i]*D+f_coeffs[i]*F+m_coeffs[i]*M+t_coeffs[i]*T)

	jde = jde + sum_corrections
	return jde	

# def main():
# 	m = 8
# 	d = 16
# 	y = 2023
# 	dates = []
# 	# timeSinceNewYears = daysSinceNewYears(7,20,2023)
# 	# yearWithDecimal = year + timeSinceNewYears
# 	# numberOfYears = 15
# 	for i in range(0,1000):
# 		# yearWithDecimal = 2023 + daysSinceNewYears(7,)
# 		jd = julianDay(7,20,2023)
# 		litPart = illuminatedFraction(jd+1)
# 		print(litPart)

# main()