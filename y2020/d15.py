from aoc_input import get_input
import aoc_helpers as ah

from collections import defaultdict, deque

DAY = 15
YEAR = 2020

def nthnum(n, startingnumbers):
	turn = 0
	lastoccs = defaultdict(lambda: deque(maxlen=2))
	lastspk = None
	for sn in startingnumbers:
		lastoccs[sn].append(turn)
		lastspk = sn
		turn += 1
	for _ in range(n - len(startingnumbers)):
		if len(lastoccs[lastspk]) < 2:  # First time spoken
			_spoken = 0
		else:
			_spoken = lastoccs[lastspk][1] - lastoccs[lastspk][0]
		lastoccs[_spoken].append(turn)
		lastspk = _spoken
		turn += 1
	return lastspk

def sol0(pzin):
	return nthnum(2020, pzin)

def sol1(pzin):
	return nthnum(30000000, pzin) # lol

def main():
	puzzle_in = [int(i) for i in get_input(YEAR, DAY).split(",")]

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
