from aoc_input import get_input
import aoc_helpers as ah

import functools

DAY = 10
YEAR = 2020

def sol0(pzin):
	c_jol = 0
	steps1 = steps3 = 0
	while pzin:
		for stepattempt in range(1, 4):
			if c_jol + stepattempt in pzin:
				pzin.remove(c_jol + stepattempt)
				c_jol += stepattempt
				if stepattempt == 1:
					steps1 += 1
				elif stepattempt == 3:
					steps3 += 1
				break
		else:
			break
	return steps1 * steps3

@functools.lru_cache
def branch_from_current(adapters, c_jol):
	poss = 0
	for stepsize in range(1, 4):
		attempt = c_jol + stepsize
		if attempt in adapters:
			if attempt == max(adapters):
				return 1
			else:
				poss += branch_from_current(adapters, attempt)
	return poss

def sol1(pzin):
	pzin = frozenset(pzin)
	return branch_from_current(pzin, 0)

def main():
	puzzle_in = {
		int(i) for i in 
		get_input(YEAR, DAY).strip().split("\n")
	}
	puzzle_in.add(max(puzzle_in) + 3)

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in.copy())
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
