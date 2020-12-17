from aoc_input import get_input
import aoc_helpers as ah

from itertools import product
import numpy as np

# Good chance this will fail for other inputs since the array bounds
# are somewhat botched and will wrap around in a really unclean manner.

DAY = 17
YEAR = 2020

STEPS = 6

class STATE:
	INACTIVE = 0
	ACTIVE = 1

def step(array):
	new_array = array.copy()
	for pos in product(*map(range, array.shape)):
		actneightbors = (
			array[tuple(slice(coord - 1, coord + 2) for coord in pos)] == STATE.ACTIVE
		).sum()
		if array[pos] == STATE.ACTIVE:
			if not (2 <= actneightbors - 1 <= 3):
				new_array[pos] = STATE.INACTIVE
		else:
			if actneightbors == 3:
				new_array[pos] = STATE.ACTIVE
	return new_array

def sol0(pzin):
	arr = np.zeros(
		(3 + 2*STEPS, len(pzin) + 2*STEPS, len(pzin[0]) + 2*STEPS),
		dtype=np.uint8
	)
	for y, ln in enumerate(pzin):
		for x, c in enumerate(ln):
			arr[1+STEPS, y + STEPS, x + STEPS] = STATE.ACTIVE if c == "#" else STATE.INACTIVE

	for _ in range(STEPS):
		arr = step(arr)
	return (arr == STATE.ACTIVE).sum()

def sol1(pzin):
	arr = np.zeros(
		(3 + 2*STEPS, 3 + 2*STEPS, len(pzin) + 2*STEPS, len(pzin[0]) + 2*STEPS),
		dtype=np.uint8
	)
	for y, ln in enumerate(pzin):
		for x, c in enumerate(ln):
			arr[1 + STEPS, 1 + STEPS, y + STEPS, x + STEPS] = \
				STATE.ACTIVE if c == "#" else STATE.INACTIVE

	for _ in range(STEPS):
		arr = step(arr)
	return (arr == STATE.ACTIVE).sum()

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
