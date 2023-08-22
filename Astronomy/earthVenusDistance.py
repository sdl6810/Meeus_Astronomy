import planetaryPositions
import innerPlanetPositions
from astro_functions import julianDay, toGregorian

jde = julianDay(8,16,2023)
venusCoords = innerPlanetPositions.venus_heliocentric_coordinates(jde)
earthCoords = planetaryPositions.earth_heliocentric_coordinates(jde)

print(venusCoords)
print(earthCoords)

for i in range(0,5):
	jde = julianDay(3, 1, 2023) + i
	venusRV = innerPlanetPositions.venusRadiusVector(jde)
	earthRV = planetaryPositions.radiusVector(jde)


	print(f"{i})", venusRV, earthRV)