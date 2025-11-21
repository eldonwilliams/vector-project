"""
  This program uses outside libraries which certain runtimes may not be okay with.
  Dr. Bego has said they are able to run this.
  
  Thank you,
  Eldon W.
  
  I have included a test suite, run using `python3 main.py test` to make it a bit easier.
  You can check the cases I have included for comprehensiveness.
"""

import os
import sys
import math
import re

# Constants

DMS_PATTERN = r"(\d+)°(\d+)'(\d+(?:\.\d*)?)''"
DEGREE_SYMBOL = "°"
C = 40000
R = 6371

running = True

# Function Definitions

def coordinate_conversion():
  dms = input(f"DMS Degrees{DEGREE_SYMBOL}Minutes\'Seconds\'\': ")
  m = re.match(DMS_PATTERN, dms)
  if not m:
    print("Input did not match the correct formatting, enter it again")
    coordinate_conversion()
    return
  degrees, minutes, seconds = map(float, m.groups())
  decimal = degrees + minutes / 60 + seconds / 60 ** 2
  print(f"Decimal Conversion: {decimal:.3f}{DEGREE_SYMBOL}")

def haversine():
  long1 = input("Longitude 1 (Decimal Degrees): ")
  lat1 = input("Latitude 1 (Decimal Degrees): ")
  long2 = input("Longitude 2 (Decimal Degrees): ")
  lat2 = input("Latitude 2 (Decimal Degrees): ")
  
  try:
    long1 = float(long1)
    lat1 = float(lat1)
    long2 = float(long2)
    lat2 = float(lat2)
  except:
    print("Some of the values you provided were not valid! Enter them again")
    haversine()
    return
  
  dlon = math.radians(long2 - long1)
  dlat = math.radians(lat2 - lat1)
  a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) ** 2
  d = 2 * R * math.asin(math.sqrt(a))
  
  theta = math.atan((math.sin(dlon) * math.cos(lat2)) / (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)))
  print(f"Distance: {d} km, Bearing: {theta}{DEGREE_SYMBOL} decimal degrees")
  

def vector_distance():
  long1 = input("Longitude 1 (Decimal Degrees): ")
  lat1 = input("Latitude 1 (Decimal Degrees): ")
  long2 = input("Longitude 2 (Decimal Degrees): ")
  lat2 = input("Latitude 2 (Decimal Degrees): ")
  
  try:
    long1 = float(long1)
    lat1 = float(lat1)
    long2 = float(long2)
    lat2 = float(lat2)
  except:
    print("Some of the values you provided were not valid! Enter them again")
    vector_distance()
    return
  
  x1 = long1 * (C / 360)
  y1 = lat1 * (C / 360)
  x2 = long2 * (C / 360)
  y2 = lat2 * (C / 360)
  
  ihat = x2 - x1
  jhat = y2 - y1
  
  print(f"ihat, jhat: ({ihat:.3f} km, {jhat:.3f})")
  
  r = math.sqrt(ihat ** 2 + jhat ** 2)
  theta = math.atan2(jhat, ihat)
  
  print(f"r, theta: ({r:.3f}, {theta:.3f})")

def exit():
  global running
  running = False

# Options Definition

OPTIONS = [
  {
    "title": "Coordinate Conversion",
    "function": coordinate_conversion,
  },
  {
    "title": "Vector Distance",
    "function": vector_distance,
  },
  {
    "title": "Haversine",
    "function": haversine,
  },
  {
    "title": "Exit",
    # While I could exit using a sentinel as described in the Rubric,
    # This gives me more control over exit success states (i.e. in this case 0 is a graceful exit)
    "function": exit,
  }
]

# Menu

def run_menu():
  # Display each option
  for option_index in range(0, len(OPTIONS)):
    option = OPTIONS[option_index]
    print(f"{option_index + 1}. {option["title"]}")
  
  # Get selection as a integer
  selection = input()
  
  # If a number out of range or some bad value was given, exit
  try:
    selection = int(selection) - 1
  except:
    print("You did not provide a integer")
    run_menu()
    return
  
  if not selection in range(0, len(OPTIONS)):
    print("That is not an option")
    run_menu()
    return
  
  # Select the option and execute
  # Should be of signature void -> any
  option = OPTIONS[selection]
  
  option["function"]()

tests = [
  {
    "name": "DMS Conversion",
    "stdin": """1
-1
BAD INPUT
38°63'83''
4""",
    "expect": """1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
DMS X°Y'Z'': Input did not match the correct formatting, enter it again
DMS X°Y'Z'': Input did not match the correct formatting, enter it again
DMS X°Y'Z'': Decimal Conversion: 39.073°
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
"""
  },
  {
    "name": "Menu",
    "stdin": """this
-1
5
4""",
    "expect": """1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
You did not provide a integer
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
That is not an option
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
That is not an option
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
"""
  },
  {
    "name": "Haversine",
    "stdin": """3
0
0
0
1
3
-85.0
38.0
-85.0
38.0
3
-85.12345
38.54321
-85.52345
38.94321
3
potato
40
-75
40
0
90
0
80
4
""",
    "expect": """1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Distance: 6371.0 km
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Distance: 0.0 km
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Distance: 2811.0376881719144 km
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Some of the values you provided were not valid! Enter them again
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Distance: 16350.347184082291 km
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
"""},
  {
    "name": "Vector Distance",
    "stdin": """2
0
0
1
1
2
-85
40
-90
35
2
10
10
10.001
10.002
2
not_a_number
50
20
20
0
0
0
0
4
""",
    "expect": """1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: ihat, jhat: (111.111 km, 111.111)
r, theta: (157.135, 0.785)
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: ihat, jhat: (-555.556 km, -555.556)
r, theta: (785.674, -2.356)
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: ihat, jhat: (0.111 km, 0.222)
r, theta: (0.248, 1.107)
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
Longitude 1: Latitude 1: Longitude 2: Latitude 2: Some of the values you provided were not valid! Enter them again
Longitude 1: Latitude 1: Longitude 2: Latitude 2: ihat, jhat: (0.000 km, 0.000)
r, theta: (0.000, 0.000)
1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
"""
  }
]

def run_test_suite():
  for test in tests:
    with open("stdin.bin", "w") as stdin:
      stdin.write(test["stdin"])
    
    status = os.spawnl(os.P_WAIT, sys.executable, sys.executable, "main.py", "case_runner")
    if status != 0:
      print(f"Test ({test["name"]}) had an exception, however, this does not mean an error")
    
    # Now we've ran the tests, but need to validate
    with open("stdout.bin", "r") as mock_stdout:
      result = mock_stdout.read()
      if result == test["expect"]:
        print(f"Test ({test["name"]}) passed!\n")
      else:
        print(f"""
=================
Test ({test["name"]}) Failed!
=================
Expected:
=================
{test['expect']}
=================
Got:
=================
{result}
=================
""")
  print(f"Finished Tests")
  # I'll clean up those files for you Dr. Bego
  os.remove("stdin.bin")
  os.remove("stdout.bin")

def case_runner():
  with open("stdin.bin", "r") as mock_stdin, open("stdout.bin", "w") as mock_stdout:
    sys.stdout = mock_stdout
    sys.stdin = mock_stdin
    while running:
      run_menu()

def main():
  cli = sys.argv[1:]
  if "test" in cli:
    run_test_suite()
    return
  if "case_runner" in cli:
    case_runner()
    return
  
  while running:
    run_menu()

if __name__ == "__main__":
  main()