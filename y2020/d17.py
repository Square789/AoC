from aoc_input import get_input
import aoc_helpers as ah

import numpy as np

# Good chance this will fail for other inputs since the array bounds
# are somewhat botched.

DAY = 17
YEAR = 2020

STEPS = 6

class STATE:
	INACTIVE = 0
	ACTIVE = 1

def step3(array):
	new_array = array.copy()
	for z in range(array.shape[0]):
		for y in range(array.shape[1]):
			for x in range(array.shape[2]):
				actneightbors = (array[z-1:z+2, y-1:y+2, x-1:x+2] == STATE.ACTIVE).sum()
				if array[z, y, x] == STATE.ACTIVE:
					# -1 since cube itself is counted
					if not (2 <= actneightbors - 1 <= 3):
						new_array[z, y, x] = STATE.INACTIVE
				else:
					if actneightbors == 3:
						new_array[z, y, x] = STATE.ACTIVE
	return new_array

def step4(array):
	new_array = array.copy()
	for w in range(array.shape[0]):
		for z in range(array.shape[1]):
			for y in range(array.shape[2]):
				for x in range(array.shape[3]):
					actneightbors = (array[w-1:w+2, z-1:z+2, y-1:y+2, x-1:x+2] == STATE.ACTIVE).sum()
					if array[w, z, y, x] == STATE.ACTIVE:
						# -1 since cube itself is counted
						if not (2 <= actneightbors - 1 <= 3):
							new_array[w, z, y, x] = STATE.INACTIVE
					else:
						if actneightbors == 3:
							new_array[w, z, y, x] = STATE.ACTIVE
	return new_array

def sol0(pzin):
	arr = np.zeros(
		(3+2*STEPS, len(pzin)+2*STEPS, len(pzin[0])+2*STEPS),
		dtype=np.uint8
	)
	for y, ln in enumerate(pzin):
		for x, c in enumerate(ln):
			arr[1+STEPS, y + STEPS, x + STEPS] = STATE.ACTIVE if c == "#" else STATE.INACTIVE

	for _ in range(STEPS):
		arr = step3(arr)
	return (arr == STATE.ACTIVE).sum()

def sol1(pzin):
	arr = np.zeros(
		(3+2*STEPS, 3+2*STEPS, len(pzin)+2*STEPS, len(pzin[0])+2*STEPS),
		dtype=np.uint8
	)
	for y, ln in enumerate(pzin):
		for x, c in enumerate(ln):
			arr[1+STEPS, 1+STEPS, y + STEPS, x + STEPS] = STATE.ACTIVE if c == "#" else STATE.INACTIVE

	for _ in range(STEPS):
		arr = step4(arr)
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
