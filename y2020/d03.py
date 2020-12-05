from aoc_input import get_input

def prod(it):
	res = 1
	for el in it:
		res *= el
	return res

DAY = 3
YEAR = 2020

def sol0(puzzle_in):
	field_width = len(puzzle_in[0])
	field_height = len(puzzle_in)
	x = y = 0
	trees = 0
	while y < field_height-1:
		x += 3
		y += 1
		if puzzle_in[y][x % field_width] == "#":
			trees += 1
	return trees

def sol1(puzzle_in):
	field_width = len(puzzle_in[0])
	field_height = len(puzzle_in)
	trees = []
	for sx, sy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
		x = y = 0
		ctrees = 0
		while y < field_height-1:
			x += sx
			y += sy
			if puzzle_in[y][x % field_width] == "#":
				ctrees += 1
		trees.append(ctrees)
	return prod(trees)

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
