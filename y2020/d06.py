from aoc_input import get_input
import aoc_helpers as ah

from string import ascii_lowercase

DAY = 6
YEAR = 2020

def sol0(pzin):
	q = 0
	for group in pzin:
		answered = set()
		for person in group.strip().split("\n"):
			answered |= {*person}
		q += len(answered)
	return q

def sol1(pzin):
	q = 0
	for group in pzin:
		answered = {*ascii_lowercase}
		for person in group.strip().split("\n"):
			answered &= {*person}
		q += len(answered)
	return q


def main():
	puzzle_in = get_input(YEAR, DAY).split("\n\n")

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
