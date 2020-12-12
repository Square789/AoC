from aoc_input import get_input
import aoc_helpers as ah

DAY = 12
YEAR = 2020

def sol0(pzin):
	rot = 90
	x = y = 0
	for instrc in pzin:
		cmd = instrc[0]
		arg = int(instrc[1:])
		if cmd == "N":
			y -= arg
		elif cmd == "S":
			y += arg
		elif cmd == "E":
			x += arg
		elif cmd == "W":
			x -= arg
		elif cmd == "L":
			rot = (rot - arg) % 360
		elif cmd == "R":
			rot = (rot + arg) % 360
		elif cmd == "F":
			if rot == 0:
				y -= arg
			elif rot == 90:
				x += arg
			elif rot == 180:
				y += arg
			elif rot == 270:
				x -= arg
			else:
				raise NotImplementedError()
	return abs(x) + abs(y)

def sol1(pzin):
	x = y = 0
	wx = 10
	wy = -1
	for instrc in pzin:
		print(x, y, "|", wx, wy)
		cmd = instrc[0]
		arg = int(instrc[1:])
		if cmd == "N":
			wy -= arg
		elif cmd == "S":
			wy += arg
		elif cmd == "E":
			wx += arg
		elif cmd == "W":
			wx -= arg
		elif cmd == "R":
			if not (arg / 90).is_integer(): raise NotImplementedError()
			for _ in range(arg // 90):
				wx, wy = -wy, wx
		elif cmd == "L":
			if not (arg / 90).is_integer(): raise NotImplementedError()
			for _ in range(arg // 90):
				wx, wy = wy, -wx
		elif cmd == "F":
			x += arg * wx
			y += arg * wy
	return abs(x) + abs(y)

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
