from aoc_input import get_input
import aoc_helpers as ah

DAY = 5
YEAR = 2020

def id_from_spec(spec):
	rl = 0
	ru = 127
	step = 64
	for c in spec[:7]:
		if c == "F":
			ru -= step
		else:
			rl += step
		step //= 2
	row = ru

	rl = 0
	ru = 7
	step = 4
	for c in spec[7:]:
		if c == "L":
			ru -= step
		else:
			rl += step
		step //= 2
	col = ru
	return row*8 + col

def sol0(pzin):
	ids = []
	for spec in pzin:
		ids.append(id_from_spec(spec))

	return max(ids)

def sol1(pzin):
	existing = {id_from_spec(spec) for spec in pzin}
	for i in range(128*8):
		if i not in existing and (i+1 in existing) and (i-1 in existing):
			return i

def main():
	puzzle_in = get_input(YEAR, DAY).splitlines()

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
