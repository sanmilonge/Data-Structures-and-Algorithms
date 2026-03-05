year_1grades = [97, 93, 90]
print(year_1grades)
year_2grades = year_1grades.copy()
year_2grades.extend([100, 100, 100])
print(year_2grades)
import sys
print(f"\nSize of year_1grades: {sys.getsizeof(year_1grades)} bytes")
print(f"Size of year_2grades: {sys.getsizeof(year_2grades)} bytes")