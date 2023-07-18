import math
from astro_functions import reduceAngle, toGregorian, julianDay, daysSinceNewYears
from general_util import importXlColumnToPythonList
import openpyxl as xl
from openpyxl import load_workbook
from datetime import datetime, date

_date = date.today()

def eccentricity(T):
	return round(1 - 0.002516*T - 0.0000074*math.pow(T,2),7)

def determine_k_value(year):
	return round((year - 2000)*12.3685,0)

def determine_T_value(k):
	return round(k/1236.85,9)

def determine_jd_date(k,T):
	jde = 2451550.09766 + 29.530588861*k + 0.00015437*T*T - 0.000000150*T*T*T + 0.00000000073*T*T*T*T
	return jde

def solarMeanAnomaly(k,T):
	return 2.5534 + 29.10535670*k - 0.0000014*T*T - 0.00000011*T*T*T

def lunarMeanAnomaly(k,T):
	return 201.5643 + 385.81693528*k + 0.0107582*T*T + 0.00001238*T*T*T - 0.000000058*T*T*T*T

def lunarlatitudeArgument(k,T):
	return 160.7108 + 390.67050284*k - 0.0016118*math.pow(T,2) - 0.00000227*math.pow(T,3) + 0.000000011*math.pow(T,4)

def longitudeAscendingNode(k,T):
	return 124.7746 - 1.56375588*k + 0.0020672*math.pow(T,2) + 0.00000215*math.pow(T,3)

def planetaryArgumentCalc(k,T):
	A = []
	#A1
	A.append(299.77 + 0.107408*k - 0.009173*math.pow(T,2))
	#A2
	A.append(251.88 + 0.016321*k)
	#A3
	A.append(251.83 + 26.651886*k)
	#A4
	A.append(349.42 + 36.412478*k)
	#A5
	A.append(84.66 + 18.206239*k)
	#A6
	A.append(141.74 + 53.303771*k)
	#A7
	A.append(207.14 + 2.453732*k)
	#A8
	A.append(154.84 + 7.306860*k)
	#A9
	A.append(34.52 + 27.261239*k)
	#A10
	A.append(207.19 + 0.121824*k)
	#A11
	A.append(291.34 + 1.844379*k)
	#A12
	A.append(161.72 + 24.198154*k)
	#A13
	A.append(239.56 + 25.513099*k)
	#A14
	A.append(331.55 + 3.592518*k)

	sumOfTerms = 0.0
	ac_coeffs = [0.000325, 0.000165, 0.000164, 0.000126, 0.000110, 0.000062, 0.000060, 0.000056, 0.000047, 0.000042, 0.000040, 0.000037, 0.000035, 0.000023]
	for j in range(len(A)):
		A[j] = reduceAngle(A[j])
		A[j] = math.radians(A[j])
		sumOfTerms = round(sumOfTerms + ac_coeffs[j]*math.sin(A[j]),6)

	return sumOfTerms

def quarter_W_value(e, m, mPrime, f):
	#M is Sun's mean anomaly
	#mPrime is Moon's mean anomaly
	#F is Moon's argument of latitude

	m = math.radians(m)
	mPrime = math.radians(mPrime)
	f = math.radians(f)

	W = 0.00306 - 0.00038*e*math.cos(m) + 0.00026*math.cos(mPrime) - 0.00002*math.cos(mPrime - m) + 0.00002*math.cos(mPrime + m) + 0.00002*math.cos(2*f)

	return W

def determineLunarPhase(month,day,year,decimal):
	#k value is set to an integer find the nearest new moon date
		#k + .25 gives first quarter,
		#k + .5 gives full,
		#k + .75 gives last quarter,

	path = '/home/sdl5384/Desktop/Python_SRC/Astronomy/lunar_phases.xlsx'
	#calculation for nearest new moon
	yearFrac = round(daysSinceNewYears(month,day,year)/365.25,2)
	k = determine_k_value(year+yearFrac)
	k = k + decimal
	T = determine_T_value(k)
	jd = round(determine_jd_date(k,T),5)

	e = eccentricity(T)
	M = math.radians(reduceAngle(solarMeanAnomaly(k,T)))
	mPrime = math.radians(reduceAngle(lunarMeanAnomaly(k,T)))
	f = math.radians(reduceAngle(lunarlatitudeArgument(k,T)))
	omega = math.radians(reduceAngle(longitudeAscendingNode(k,T)))

	w = quarter_W_value(eccentricity(T),solarMeanAnomaly(k,T), lunarMeanAnomaly(k,T), lunarlatitudeArgument(k,T))

	correctionsForAllPhases = planetaryArgumentCalc(k,T)

	lunarSheetData = load_workbook(path)
	newFullSht = lunarSheetData['newFull']
	quarterSht = lunarSheetData['quarters']

	correctionsSumNM = 0.0
	correctionsSumFM = 0.0
	correctionsSumQtrs = 0.0
	eIsHere = [1,4,5,9,11,12,13]

	coeffs = importXlColumnToPythonList(path,'newFull','B',0)
	coeffs.remove('New Moon')
	eccCoeffs = importXlColumnToPythonList(path,'newFull','D',0)
	eccCoeffs.remove('eccentricity')
	mPrimeCoeffs = importXlColumnToPythonList(path,'newFull','E',0)
	mPrimeCoeffs.remove(mPrimeCoeffs[0])
	mCoeffs = importXlColumnToPythonList(path,'newFull','F',0)
	mCoeffs.remove(mCoeffs[0])
	omegaCoeffs = importXlColumnToPythonList(path,'newFull','H',0)
	omegaCoeffs.remove('Long of Ascending Node')
	lattArgCoeffs = importXlColumnToPythonList(path,'newFull','G',0)
	lattArgCoeffs.remove(lattArgCoeffs[0])

	#New Moon corrections
	for j in range(0,25):
		if j not in eIsHere:
			if j == 14:
				correctionsSumNM = correctionsSumNM + newFullSht['B'+str(5+j)].value*math.sin(newFullSht['H'+str(5+j)].value*omega)
			else:	
				correctionsSumNM = correctionsSumNM + newFullSht['B'+str(5+j)].value*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)
		elif j in eIsHere:
			if j == 6:
				correctionsSumNM = correctionsSumNM + newFullSht['B'+str(5+j)].value*newFullSht['D'+str(5+j)].value*(e*e)*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)
			else:
				correctionsSumNM = correctionsSumNM + newFullSht['B'+str(5+j)].value*newFullSht['D'+str(5+j)].value*e*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)

	#Full Moon corrections
	j = 0
	for j in range(0,25):
		if j not in eIsHere:
			if j == 14:
				correctionsSumFM = correctionsSumFM + newFullSht['C'+str(5+j)].value*math.sin(newFullSht['H'+str(5+j)].value*omega)
			else:	
				correctionsSumFM = correctionsSumFM + newFullSht['C'+str(5+j)].value*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)
		elif j in eIsHere:
			if j == 6:
				correctionsSumFM = correctionsSumFM + newFullSht['C'+str(5+j)].value*newFullSht['D'+str(5+j)].value*(e*e)*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)
			else:
				correctionsSumFM = correctionsSumFM + newFullSht['C'+str(5+j)].value*newFullSht['D'+str(5+j)].value*e*math.sin(newFullSht['E'+str(5+j)].value*mPrime + newFullSht['F'+str(5+j)].value*M + newFullSht['G'+str(5+j)].value*f)

	#Quarter corrections
	qtrCoeffs = importXlColumnToPythonList(path,'quarters','C',0)
	qtrCoeffs.remove('Coefficients')
	eccCoeffsQtr = importXlColumnToPythonList(path,'quarters','D',0)
	eccCoeffsQtr.remove(eccCoeffsQtr[0])
	mPrimeCoeffsQtr = importXlColumnToPythonList(path,'quarters','E',0)
	mPrimeCoeffsQtr.remove(mPrimeCoeffsQtr[0])
	mCoeffsQtr = importXlColumnToPythonList(path,'quarters','F',0)
	mCoeffsQtr.remove(mCoeffsQtr[0])
	omegaCoeffsQtr = importXlColumnToPythonList(path,'quarters','H',0)
	omegaCoeffsQtr.remove(omegaCoeffsQtr[0])
	lattArgCoeffsQtr = importXlColumnToPythonList(path,'quarters','G',0)
	lattArgCoeffsQtr.remove(lattArgCoeffsQtr[0])

	j = 0
	for j in range(0,25):
		if j not in eIsHere:
			if j == 15:
				correctionsSumQtrs = correctionsSumQtrs + qtrCoeffs[j]*math.sin(lattArgCoeffsQtr[j]*omega)
			else:
				correctionsSumQtrs = correctionsSumQtrs + qtrCoeffs[j]*math.sin(mPrimeCoeffsQtr[j]*mPrime + mCoeffsQtr[j]*M + lattArgCoeffsQtr[j]*f)
		elif j in eIsHere:
			if j == 6 or j == 13:
				correctionsSumQtrs = correctionsSumQtrs + qtrCoeffs[j]*eccCoeffsQtr[j]*(e*e)*math.sin(mPrimeCoeffsQtr[j]*mPrime + mCoeffsQtr[j]*M + lattArgCoeffsQtr[j]*f)
			else:
				correctionsSumQtrs = correctionsSumQtrs + qtrCoeffs[j]*eccCoeffsQtr[j]*e*math.sin(mPrimeCoeffsQtr[j]*mPrime + mCoeffsQtr[j]*M + lattArgCoeffsQtr[j]*f)

	jde = 0.0
	if k-int(k) == 0:
		jde = jd+correctionsSumNM+correctionsForAllPhases
	elif k-int(k) == 0.25:
		jde = jd+correctionsSumQtrs+correctionsForAllPhases+w
	elif k-int(k) == 0.5:
		jde = jd+correctionsSumFM+correctionsForAllPhases
	elif k-int(k) == 0.75:
		w = -1*w
		jde = jd+correctionsSumQtrs+correctionsForAllPhases+w

	return jde

def main():
	jdPhases = determineLunarPhase(8,10,2023,0)
	print(toGregorian(jdPhases))

main()