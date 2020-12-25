from aoc_input import get_input
import aoc_helpers as ah

import re

DAY = 24
YEAR = 2020

RE_STEPS = re.compile("e|w|nw|ne|sw|se")

STEPS = {
	"e":  (( 1,  1),  0),
	"w":  ((-1, -1),  0),
	"nw": ((-1,  0), -1),
	"ne": (( 0,  1), -1),
	"sw": ((-1,  0),  1),
	"se": (( 0,  1),  1),
}

def sol0(pzin):
	black_tiles = set()
	for line in pzin:
		x = y = 0
		for move in RE_STEPS.findall(line):
			x += STEPS[move][0][y & 1]
			y += STEPS[move][1]
		coords = (x, y)
		if coords in black_tiles:
			black_tiles.remove(coords)
		else:
			black_tiles.add(coords)

	return (len(black_tiles), black_tiles)

def get_black_neighbors(tile_config, coords):
	x, y = coords
	return sum(
		(x + step[0][y & 1], y + step[1]) in tile_config
		for step in STEPS.values()
	)

def sol1(pzin):
	tile_config = sol0(pzin)[1]
	for _ in range(100):
		border_estimate = (
			(min(x for x, y in tile_config) - 1, min(y for x, y in tile_config) - 1),
			(max(x for x, y in tile_config) + 1, max(y for x, y in tile_config) + 1),
		)
		next_config = set()
		for y in range(border_estimate[0][1], border_estimate[1][1] + 1):
			for x in range(border_estimate[0][0], border_estimate[1][0] + 1):
				coords = (x, y)
				bn = get_black_neighbors(tile_config, coords)
				if (
					((coords in tile_config) and (1 <= bn <= 2)) or
					((coords not in tile_config) and bn == 2)
				):
					next_config.add(coords)
		tile_config = next_config
	return len(tile_config)

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		res = res[0] if i == 0 else res
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
