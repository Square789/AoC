from aoc_input import get_input
import aoc_helpers as ah

import re


DAY = 3
YEAR = 2023


RE_NUMBER = re.compile(r"\d+")
NUMBERS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

def is_symbol(char):
	if char == '.':
		return False
	if char in NUMBERS:
		return False
	return True

def symbol_check(puzzle_data, line_idx, start, end):
	if line_idx > 0:
		for i in range(max(0, start - 1), min(len(puzzle_data[line_idx - 1]), end + 1)):
			if is_symbol(puzzle_data[line_idx - 1][i]):
				return True
	if start > 0:
		if is_symbol(puzzle_data[line_idx][start - 1]):
			return True
	if end < len(puzzle_data[line_idx]):
		if is_symbol(puzzle_data[line_idx][end]):
			return True
	if line_idx + 1 < len(puzzle_data):
		for i in range(max(0, start - 1), min(len(puzzle_data[line_idx + 1]), end + 1)):
			if is_symbol(puzzle_data[line_idx + 1][i]):
				return True
	return False

def sol0(setup_data, puzzle_data):
	res = 0
	for i, line in enumerate(puzzle_data):
		for match in RE_NUMBER.finditer(line):
			start, end = match.span(0)
			if symbol_check(puzzle_data, i, start, end):
				res += int(match.group(0))

	return res

def sol1(setup_data, puzzle_data):
	# god bless python's ability to use whatever as hash indices
	q = {}
	res = 0

	match_id = 0
	for y, line in enumerate(puzzle_data):
		for match in RE_NUMBER.finditer(line):
			start, end = match.span(0)
			part_id = int(match.group(0))
			for x in range(start, end):
				q[(y, x)] = (part_id, match_id)
			match_id += 1

	for y, line in enumerate(puzzle_data):
		for x, c in enumerate(line):
			if c != '*':
				continue

			seen_part_ids = {}
			for coord in (
				(y - 1, x - 1),
				(y - 1, x),
				(y - 1, x + 1),
				(y,     x - 1),
				(y,     x + 1),
				(y + 1, x - 1),
				(y + 1, x),
				(y + 1, x + 1),
			):
				if coord in q:
					part_id, m_id = q[coord]
					if m_id not in seen_part_ids:
						seen_part_ids[m_id] = part_id
			if len(seen_part_ids) == 2:
				a, b = seen_part_ids.values()
				res += a * b

	return res


def get_data():
	puzzle_data = get_input(YEAR, DAY).strip().split("\n")
	return puzzle_data

def setup(puzzle_data):
	return puzzle_data

def main():
	ah.print_solution2(get_data, setup, DAY, YEAR, sol0, sol1)

if __name__ == "__main__":
	main()
