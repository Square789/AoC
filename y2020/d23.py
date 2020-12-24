from aoc_input import get_input
import aoc_helpers as ah

from tqdm import tqdm

DAY = 23
YEAR = 2020

def simulate(playfield, moves):
	cup_amt = len(playfield)
	maxcup = max(playfield)
	mincup = min(playfield)
	picked_up = [None] * 3

	cur_cup_idx = 0
	cur_cup = playfield[0]
	for _ in tqdm(range(moves)):
		for offset in range(3):
			picked_up[offset] = playfield[(cur_cup_idx + 1 + offset) % cup_amt]
		dest_cup = cur_cup
		while True:
			dest_cup -= 1
			if dest_cup < mincup:
				dest_cup = maxcup
			if dest_cup not in picked_up:
				break
		dest_cup_idx = playfield.index(dest_cup)
		# Shift back all cups between cur_cup_idx + 4..dest_cup_idx
		shift_ring_start = ((cur_cup_idx + 4) % cup_amt)
		ringlength = (dest_cup_idx - shift_ring_start + 1) % cup_amt
		for offset in range(ringlength):
			playfield[(shift_ring_start + offset - 3) % cup_amt] = \
				playfield[(shift_ring_start + offset) % cup_amt]
		dest_cup_idx = (dest_cup_idx - 3) % cup_amt
		for offset in range(3):
			playfield[(dest_cup_idx + 1 + offset) % cup_amt] = picked_up[offset]
		cur_cup_idx = (cur_cup_idx + 1) % cup_amt
		cur_cup = playfield[cur_cup_idx]

def sol0(pzin):
	playfield = [*map(int, pzin)]
	simulate(playfield, 100)

	r = ""
	cup_1_idx = playfield.index(1)
	for offset in range(8):
		r += str(playfield[(cup_1_idx + 1 + offset) % len(playfield)])

	return r

def sol1(pzin):
	playfield = [*map(int, pzin)]
	mic = max(playfield)
	more_cups = [None] * (1_000_000 - len(playfield))
	for idx, i in enumerate(range(mic + 1, len(more_cups) + mic + 1)):
		more_cups[idx] = i
	playfield += more_cups

	raise NotImplementedError()

	simulate(playfield, 10_000_000)

	# This is gonna run for a literal month, C gets it down to 3 hours. [d23.c]

def main():
	puzzle_in = get_input(YEAR, DAY).strip()

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
