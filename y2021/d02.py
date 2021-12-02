from aoc_input import get_input
import aoc_helpers as ah

DAY = 2
YEAR = 2021


def sol0(pzin):
	x = y = 0
	for cmd, val in pzin:
		if cmd == "forward":
			x += val
		elif cmd == "down":
			y += val
		elif cmd == "up":
			y -= val

	return x * y


def sol1(pzin):
	x = y = aim = 0
	for cmd, val in pzin:
		if cmd == "forward":
			x += val
			y += aim * val
		elif cmd == "down":
			aim += val
		elif cmd == "up":
			aim -= val

	return x * y

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	puzzle_in = [(x[0], int(x[1])) for x in (l.split() for l in puzzle_in)]

	ah.print_solution(puzzle_in, DAY, YEAR, sol0, sol1)
