import math
from datetime import datetime, date
from astro_functions import reduceAngle, julianDay, daysSinceEpoch, daysSinceNewYears

def calculate_T(startingPoint,currentJD):
	return (currentJD - startingPoint)/36525

def eccentricity(epochDate,jd):
	T = calculate_T(epochDate,jd)
	return 0.01675104 - 0.0000418*T - 0.000000126*math.pow(T,2)

def solarMeanLongPerigee(T):
	return math.radians(reduceAngle(round(281.2208444 + 1.719175*T + 0.000452778*math.pow(T,2),6)))

def solarLongAtEpoch(T):
	return math.radians(reduceAngle(round(279.6966778 + 36000.76892*T + 0.0003025*math.pow(T,2),6)))

def solarMeanAnomaly(epoch,jd):
	T = calculate_T(epoch,jd)
	eclLongAtEpoch = solarLongAtEpoch(T)
	eclLongAtPerigee = solarMeanLongPerigee(T)
	return math.radians(reduceAngle(round((360/365.242191)*(jd - 2451545) + eclLongAtEpoch - eclLongAtPerigee,6)))

def solarTrueAnomaly(epoch,jd):
	T = calculate_T(epoch,jd)
	e = eccentricity(epoch,jd)
	#m is already converted radians in the previous function
	m = solarMeanAnomaly(epoch,jd)
	return m + (360/math.pi)*e*math.sin(m)

def positionOfMoon(jd):
	jd1990 = julianDay(12,30,1989)
	D = daysSinceEpoch(jd1990,jd)
	lunarMeanLongitude = 13.1763966*D + 318.351548
	lunarMeanAnomaly = lunarMeanLongitude - 0.111404*D - 36.340410
	
	#this variable is represented by N
	ascendingNodeOFMeanLongitude = 318.510107 - 0.0529539*D

	meanAnomalyOfSun = solarTrueAnomaly(jd1990,jd)
	trueAnomalyOfSun = solarMeanAnomaly(jd1990,jd)
	solarEclipLong = trueAnomalyOfSun + 282.768422

	c = lunarMeanLongitude - solarEclipLong

	Ev = 1.2739*math.sin(math.radians(2*c - lunarMeanAnomaly))
	Ae = 0.1858*math.sin(math.radians(meanAnomalyOfSun))
	A3 = 0.37*math.sin(math.radians(meanAnomalyOfSun))

	correctedLunarMeanAnomaly = lunarMeanAnomaly + Ev - Ae - A3

	#corrections for the equation of the center
	Ec = 6.2886*math.sin(math.radians(correctedLunarMeanAnomaly))
	A4 = 0.214*math.sin(math.radians(2*correctedLunarMeanAnomaly))

	correctedLunarLong = lunarMeanLongitude + Ev + Ec - Ae + A4
	correctedLunarMeanAnomalyVariation = 0.6583*math.sin(math.radians(2*correctedLunarLong - solarEclipLong))
	trueLunarOrbitalLong = correctedLunarLong + correctedLunarMeanAnomalyVariation

	#compute the longitude of the ecliptic
	#N is the corrected longitude of the node
	nPrime = ascendingNodeOFMeanLongitude - 0.16*math.sin(math.radians(meanAnomalyOfSun))
	#5.145396 is inclination of lunar orbit
	numerator = math.sin(math.radians(trueLunarOrbitalLong - nPrime))*math.cos(5.145396)
	denominator = math.cos(math.radians(trueLunarOrbitalLong - nPrime))
	moonLambda = math.atan(numerator/denominator) + ascendingNodeOFMeanLongitude

	moonBeta = math.asin(math.sin(math.radians(trueLunarOrbitalLong - nPrime))*math.sin(math.radians(5.145396)))
	return [moonLambda, moonBeta]

def main():
	#February 26 1979 at 16h and 50s
	secondsTodayFrac = ((50/60)/60)
	dayFrac = round((16 + secondsTodayFrac)/24,6)
	sinceJan1 = daysSinceNewYears(2,26+dayFrac,1979)
	jd = julianDay(2,(26+secondsTodayFrac),1979)
	jd1990 = julianDay(1,1,1990)

	D = daysSinceEpoch(jd,julianDay(1,1,1990))
	print(D)
	meanAnomalyOfSun = solarMeanAnomaly(1990,jd)
	trueAnomalyOfSun = solarTrueAnomaly(1990,jd)
main()