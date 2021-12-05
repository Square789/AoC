from aoc_input import get_input
import aoc_helpers as ah

import numpy as np
import re

DAY = 5
YEAR = 2021

class Line:
	def __init__(self, x0, y0, x1, y1) -> None:
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1

	def insert(self, array, diagonally=False):
		x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
		xdir = 1 if x0 < x1 else -1
		ydir = 1 if y0 < y1 else -1

		if x0 != x1 and y0 == y1: # Vertical line
			for x in range(x0, x1 + xdir, xdir):
				array[y0, x] += 1
			return

		elif x0 == x1 and y0 != y1: # Horizontal line
			for y in range(y0, y1 + ydir, ydir):
				array[y, x0] += 1
			return

		if not diagonally:
			return

		if abs(x0 - x1) != abs(y0 - y1):
			print(f"Line {x0}, {y0} -> {x1}, {y1} not diagonal!")
			return

		for i in range(abs(x0 - x1) + 1):
			array[y0 + (i * ydir), x0 + (i * xdir)] += 1


def sol0(field, puzzle_data):
	for line in puzzle_data:
		line.insert(field)
	return (field > 1).sum()

def sol1(field, puzzle_data):
	for line in puzzle_data:
		line.insert(field, True)
	return (field > 1).sum()

def get_data():
	puzzle_data = get_input(YEAR, DAY).strip().split("\n")
	return [
		Line(*map(int, re.match("^(\d+),(\d+) -> (\d+),(\d+)$", l).groups()))
		for l in puzzle_data
	]

def setup(puzzle_data):
	return np.zeros((
		max(max(line.y0, line.y1) for line in puzzle_data) + 1,
		max(max(line.x0, line.x1) for line in puzzle_data) + 1,
	))

def main():
	ah.print_solution2(get_data, setup, DAY, YEAR, sol0, sol1)

if __name__ == "__main__":
	main()
