from aoc_input import get_input
import aoc_helpers as ah

DAY = 1
YEAR = 2021

def sol0(pzin):
	increases = 0
	for i, m in enumerate(pzin):
		if i > 0 and pzin[i] > pzin[i - 1]:
			increases += 1
	return increases

def sol1(pzin):
	increases = 0
	for i in range(len(pzin) - 2):
		prv = sum(pzin[i-1 : i+2])
		cur = sum(pzin[i : i+3])
		if i > 0 and cur > prv:
			increases += 1
	return increases

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	puzzle_in = [int(l) for l in puzzle_in]

	ah.print_solution(puzzle_in, DAY, YEAR, sol0, sol1)
