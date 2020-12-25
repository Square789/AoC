from aoc_input import get_input
import aoc_helpers as ah

import time

DAY = 25
YEAR = 2020

def tf_subject_num(sn, loopsz):
	val = 1
	for _ in range(loopsz):
		val *= sn
		val %= 20201227
	return val

def bruteforce(pub):
	lsz = 1
	res = 1
	while res != pub:
		res *= 7
		res %= 20201227
		lsz += 1
	return lsz - 1
	
def sol0(pzin):
	card_pub = pzin[0]
	door_pub = pzin[1]

	cls = bruteforce(card_pub)
	dls = bruteforce(door_pub)

	return tf_subject_num(door_pub, cls)

def sol1(pzin):
	return "[Pay your deposit]"

def main():
	puzzle_in = [*map(int, get_input(YEAR, DAY).strip().split("\n"))]

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
