import math
import astro_functions as af
from datetime import date, datetime

venusInfConj = [2451412.706, 583.921361, 82.7311, 215.513058]
trigArgCoeffs = [1,1,2,2,3,3]
_date = date.today()

venusInfConjCoeffs = [[-0.0096, 0.0002, -0.00001], 
						[2.0009 -.0033, -0.00001], 
						[0.5980, -.0104, 0.00001],
						[0.0967, -0.0018, -0.00003],
						[0.0913, 0.0009, -0.00002],
						[0.0046, -0.0002, 0],
						[0.0079, 0.0001, 0]]

def determine_k(m,d,y):
	yearWithDecimal = round(_date.year + (af.daysSinceNewYears(_date.month, _date.day, _date.year))/365.25,4)
	k = float(round((365.2425*yearWithDecimal + 1721060 - venusInfConj[0])/venusInfConj[1],0))
	return k

def determine_jde(k_value):
	return round(venusInfConj[0] + k_value*venusInfConj[1],3)

def meanAnomaly(k_value):
	ma = round(af.reduceAngle(venusInfConj[2] + k_value*venusInfConj[3]),6)
	return ma

def determine_T(jde0):
	return round((jde0 - 2451545)/36525,5)

def determine_infConjDate(julianDay, k_value, T_value):
	correctionsToJDE = 0.0
	m = meanAnomaly(k_value)
	coefficientSums = []
	coefficientSum = 0.0
	julianDay = julianDay + (-0.0096 + 0.00002*T_value) #- 0.00001*math.pow(T_value,2))
	for i in range(0,len(venusInfConjCoeffs)):
		for j in range(0,len(venusInfConjCoeffs[i])-1):
			coefficientSum = coefficientSum + venusInfConjCoeffs[i][j]*math.pow(T_value,j)
			coefficientSums.append(coefficientSum)

	print(len(coefficientSums))

	for r in range(0,len(coefficientSums)-1):
		if r%2 == 0:
			julianDay = round(julianDay + coefficientSums[r]*math.sin(trigArgCoeffs[r]*math.radians(m)),3)
			print(julianDay, trigArgCoeffs[r], "sin")
		elif r%2 == 1:
			julianDay = round(julianDay + coefficientSums[r]*math.cos(trigArgCoeffs[r]*math.radians(m)),3)
			print(julianDay, trigArgCoeffs[r], "cos")

	return julianDay

def main():
	k = determine_k(_date.month, _date.day, _date.year)
	j = determine_jde(k)
	T = determine_T(j)
	jde = determine_infConjDate(j,k,T)
	print(jde)

main()
