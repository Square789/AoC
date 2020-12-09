from aoc_input import get_input
import aoc_helpers as ah

from collections import deque

from itertools import combinations

DAY = 9
YEAR = 2020

def sol0(pzin):
	prev = deque()
	for _ in range(25):
		prev.append(pzin.pop(0))

	while pzin:
		cur = pzin.pop(0)
		for x, y in combinations(prev, 2):
			if x + y == cur:
				break
		else:
			return cur
		prev.append(cur)
		prev.popleft()

def sol1(pzin):
	NUM = 3199139634 # hardcoded
	data_len = len(pzin)

	for set_size in range(2, data_len + 1):
		for i in range(0, data_len - set_size + 1):
			cs = {*pzin[i:(i + set_size)]}
			if sum(cs) == NUM:
				return min(cs) + max(cs)
	return None

def main():
	puzzle_in = [
		int(i) for i in
		get_input(YEAR, DAY).strip().split("\n")
	]

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in.copy())
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
