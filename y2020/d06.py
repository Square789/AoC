from aoc_input import get_input
import aoc_helpers as ah

DAY = 6
YEAR = 2020

def sol0(pzin):
	pass

def sol1(pzin):
	pass

def main():
	puzzle_in = get_input(YEAR, DAY)

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
