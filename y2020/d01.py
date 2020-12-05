from itertools import combinations

from aoc_input import get_input

DAY = 1
YEAR = 2020

def sol0(puzzle_in):
	set0 = {int(i) for i in puzzle_in.split()}
	set1 = set0.copy()

	for i in set0:
		set1.remove(i)
		for j in set1:
			if i+j == 2020:
				return i*j

def sol1(puzzle_in):
	puzzle_in = [int(i) for i in puzzle_in.split()]

	for a,b,c in combinations(puzzle_in, 3):
		if a + b + c == 2020:
			return a * b * c

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
