"""
  This program uses outside libraries which certain runtimes may not be okay with.
  Dr. Bego has said they are able to run this.
  
  Thank you,
  Eldon W.
  
  I have included a test suite, run using `python3 main.py test` to make it a bit easier.
  You can check the cases I have included for comprehensiveness.
"""

from os import _exit, remove
import sys
import math
import re

# Constants

DMS_PATTERN = r"(\d+)°(\d+)'(\d+)''"
DEGREE_SYMBOL = "°"
C = 40,000
R = 6,371

# Function Definitions

def coordinate_conversion():
  dms = input(f"DMS X{DEGREE_SYMBOL}Y\'Z\'\': ")
  m = re.match(DMS_PATTERN, dms)
  if not m:
    return
  degrees, minutes, seconds = map(int, m.groups())
  decimal = degrees + minutes / 60 + seconds / 60 ** 2
  print(f"Decimal Conversion: {decimal:.3f}{DEGREE_SYMBOL}")

def haversine():
  long1 = input("Longitude 1: ")
  lat1 = input("Latitude 1: ")
  long2 = input("Longitude 2: ")
  lat2 = input("Latitude 2: ")
  dlon = long2 - long1
  dlat = lat2 - lat1
  a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) ** 2
  d = 2 * R * math.asin(math.sqrt(a))
  print(f"Distance: {d} km")
  

def vector_distance():
  long1 = input("Longitude 1: ")
  lat1 = input("Latitude 1: ")
  long2 = input("Longitude 2: ")
  lat2 = input("Latitude 2: ")
  
  try:
    long1 = float(long1)
    lat1 = float(lat1)
    long2 = float(long2)
    lat2 = float(lat2)
  except:
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
    "function": lambda:_exit(0),
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
    return
  
  if not selection in range(0, len(OPTIONS)):
    return
  
  # Select the option and execute
  # Should be of signature void -> any
  option = OPTIONS[selection]
  
  option["function"]()

tests = [
  {
    "name": "DMS Conversion",
    "stdin": """1
38°63'83''""",
    "expect": """1. Coordinate Conversion
2. Vector Distance
3. Haversine
4. Exit
DMS X°Y'Z'': Decimal Conversion: 39.073°
"""
  }
]

def run_test_suite():
  original_stdout = sys.stdout
  for test in tests:
    original_stdout.write(f"Running test: {test["name"]}\n")
    # Write the stdin for the test
    with open("stdin.bin", "w") as f:
      f.write(test["stdin"])
    
    # Now that we've written stdin we can open it back up in read mode and open up stdout for writing
    with open("stdin.bin", "r") as mock_stdin, open("stdout.bin", "w") as mock_stdout:
      sys.stdin = mock_stdin
      sys.stdout = mock_stdout
      try:
        run_menu()
      except:
        original_stdout.write(f"\nTest ({test["name"]}) failed with an exception!\n")
    
    # Now we've ran the tests, but need to validate
    with open("stdout.bin", "r") as mock_stdout:
      result = mock_stdout.read()
      if result == test["expect"]:
        original_stdout.write(f"Test ({test["name"]}) passed!\n")
      else:
        original_stdout.write(f"\n=============\nTest ({test["name"]}) Failed!\n=============\nExpected:\n===========\n{test['expect']}\n===========\nGot:\n=============\n{result}============\n")
    
  sys.stdout = original_stdout
  print(f"Finished Tests")
  # I'll clean up those files for you Dr. Bego
  remove("stdin.bin")
  remove("stdout.bin")
  

def main():
  cli = sys.argv[1:]
  if "TEST" in cli:
    run_test_suite()
    return
  while True:
    run_menu()

if __name__ == "__main__":
  main()