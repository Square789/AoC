from aoc_input import get_input
import aoc_helpers as ah

from collections import Counter

DAY = 3
YEAR = 2021

def sol0(pzin):
	gamma = ""
	epsilon = ""
	for bit_col in zip(*pzin):
		c = Counter(bit_col)
		if c["0"] > c["1"]:
			gamma += "0"
			epsilon += "1"
		else:
			gamma += "1"
			epsilon += "0"
	return int(gamma, 2) * int(epsilon, 2)

def sol1(pzin):
	oxy_indices = set(range(len(pzin)))
	co2_indices = set(range(len(pzin)))
	for i, bit_col in enumerate(zip(*pzin)):
		for considered_indices, get_keep_val_func in (
			(oxy_indices, lambda c: "0" if c["0"] > c["1"] else "1"),
			(co2_indices, lambda c: "0" if c["0"] <= c["1"] else "1"),
		):
			if len(considered_indices) <= 1:
				continue
			keep = get_keep_val_func(Counter(
				bit for i, bit in enumerate(bit_col) if i in considered_indices
			))
			for i, bit in enumerate(bit_col):
				if i in considered_indices and bit != keep:
					considered_indices.remove(i)

	if len(oxy_indices) != 1 or len(co2_indices) != 1:
		raise ValueError("Epic fail")

	return ah.prod(
		int(pzin[next(iter(set_))], 2)
		for set_ in (oxy_indices, co2_indices)
	)

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")

	ah.print_solution(puzzle_in, DAY, YEAR, sol0, sol1)
