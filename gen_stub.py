from pathlib import Path
import sys

SCRIPT = """from aoc_input import get_input
import aoc_helpers as ah

DAY = {day}
YEAR = {year}

def sol0(setup_data, puzzle_data):
	pass

def sol1(setup_data, puzzle_data):
	pass

def get_data():
	puzzle_data = get_input(YEAR, DAY).strip().split("\\n")
	return puzzle_data

def setup(puzzle_data):
	return puzzle_data

def main():
	ah.print_solution2(get_data, setup, DAY, YEAR, sol0, sol1)

if __name__ == "__main__":
	main()
"""

def make_file(year, day):
	try:
		year = int(year)
		day = int(day)
	except ValueError:
		print("Grrrr, those aren't numbers")
		return

	tgt_path = Path(f"./y{year}/d{day:>02}.py")
	if tgt_path.exists():
		print("File exists!")
		return

	with open(tgt_path, "w") as fp:
		fp.write(SCRIPT.format(year = year, day = day))

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Need year and day as arguments!")
		sys.exit()

	make_file(sys.argv[1], sys.argv[2])
