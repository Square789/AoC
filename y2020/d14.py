from aoc_input import get_input
import aoc_helpers as ah

import re

from itertools import product

RE_MEM = re.compile(r"^mem\[(\d+)\] = (\d+)$")
RE_MSK = re.compile(r"^mask = ([X01]{36})$")

DAY = 14
YEAR = 2020

def sol0(pzin):
	mem = {}
	mask = None
	for instrc in pzin:
		match = RE_MEM.match(instrc)
		if match:
			val = int(match[2])
			tgt = int(match[1])
			for i, c in enumerate(reversed(mask)):
				if c == "1":
					val |= (1 << i)
				elif c == "0":
					val -= (1 << i)*(1 & (val >> i))
			mem[tgt] = val
			continue
		match = RE_MSK.match(instrc)
		if match:
			mask = match[1]
			continue
		raise ValueError()
	return sum(mem.values())

def sol1(pzin):
	mem = {}
	mask = None
	for instrc in pzin:
		match = RE_MEM.match(instrc)
		if match:
			val = int(match[2])
			tgt = "".join(
				"{}" if mb == "X" else ("1" if mb == "1" else ab)
				for mb, ab in zip(mask, bin(int(match[1]))[2:].zfill(36))
			)
			for prd in product((0, 1), repeat = mask.count("X")):
				mem[int(tgt.format(*prd), 2)] = val
			continue
		match = RE_MSK.match(instrc)
		if match:
			mask = match[1]
			continue
		raise ValueError()
	return sum(mem.values())


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
