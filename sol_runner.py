import importlib
import sys

from aoc_input import get_input

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Specify which file to run! [year, day]")
		sys.exit()

	try:
		year = int(sys.argv[1])
		day = int(sys.argv[2])
	except ValueError:
		print("Integer required!")
		sys.exit()

	module = importlib.import_module(f"y{year}.d{day:>02}")
	module.main()
