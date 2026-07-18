from src.solar import getSolarPosition
from src.control import solarVector


azimuth, elevation = getSolarPosition()


vector = solarVector(
    azimuth,
    elevation
)


print("Posición actual del Sol")
print("----------------------")

print(f"Azimut: {azimuth:.2f}°")
print(f"Elevación: {elevation:.2f}°")

print("\nVector solar:")
print(f"X: {vector[0]:.4f}")
print(f"Y: {vector[1]:.4f}")
print(f"Z: {vector[2]:.4f}")