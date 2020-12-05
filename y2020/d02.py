import re

from aoc_input import get_input

DAY = 2
YEAR = 2020

REGEX_SPEC = re.compile(r"(\d+)-(\d+) (.): (.*)")

def sol0(puzzle_in):
	valid = 0
	for spec in puzzle_in:
		cmin, cmax, c, pw = REGEX_SPEC.match(spec).groups()
		if int(cmin) <= pw.count(c) <= int(cmax):
			valid += 1
	return valid

def sol1(puzzle_in):
	valid = 0
	for spec in puzzle_in:
		i0, i1, c, pw = REGEX_SPEC.match(spec).groups()
		if (pw[int(i0) - 1] == c) ^ (pw[int(i1) - 1] == c):
			valid += 1
	return valid


def main():
	puzzle_in = get_input(YEAR, DAY)
	puzzle_in = puzzle_in.splitlines()

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
