from aoc_input import get_input
import aoc_helpers as ah

import numpy as np

np.set_printoptions(linewidth=200, threshold=10000)

from time import sleep

DAY = 11
YEAR = 2020

class STATE:
	NONE = 0
	FREE = 1
	OCCUPIED = 2

def simulate(seats, occfunc, tol_free):
	change_occurred = True
	while change_occurred:
		print(".", end="", flush=True)
		change_occurred = False
		newseats = seats.copy()
		for y, line in enumerate(seats):
			for x, state in enumerate(line):
				if state == STATE.FREE and occfunc(seats, x, y) == 0:
					newseats[y, x] = STATE.OCCUPIED
					change_occurred = True
				elif state == STATE.OCCUPIED and occfunc(seats, x, y) >= tol_free:
					newseats[y, x] = STATE.FREE
					change_occurred = True
		seats = newseats
	print()

	return (seats == STATE.OCCUPIED).sum()

def adj_occ(seats, x, y):
	dxl = dyl = dxu = dyu = 1
	if x == 0:
		dxl = 0
	elif x == seats.shape[1] - 1:
		dxu = 0
	if y == 0:
		dyl = 0
	elif y == seats.shape[0] - 1:
		dyu = 0
	tmp = seats[y, x]
	seats[y, x] = 4
	res = (seats[y-dyl:y+dyu+1, x-dxl:x+dxu+1] == STATE.OCCUPIED).sum()
	seats[y, x] = tmp
	return res

def sol0(seats):
	return simulate(seats, adj_occ, 4)

def star_occ(seats, x, y):  # Prime spaghetto
	occ = 0
	cy = y
	while cy > 0:  # N
		cy -= 1
		if seats[cy, x] == STATE.NONE: continue
		if seats[cy, x] == STATE.OCCUPIED: occ += 1
		break
	cy = y
	cx = x
	while cy > 0 and cx < seats.shape[1] - 1:  # NE
		cy -= 1
		cx += 1
		if seats[cy, cx] == STATE.NONE: continue
		if seats[cy, cx] == STATE.OCCUPIED: occ += 1
		break
	cx = x
	while cx < seats.shape[1] - 1:  # E
		cx += 1
		if seats[y, cx] == STATE.NONE: continue
		if seats[y, cx] == STATE.OCCUPIED: occ += 1
		break
	cy = y
	cx = x
	while cy < seats.shape[0] - 1 and cx < seats.shape[1] - 1:  # SE
		cy += 1
		cx += 1
		if seats[cy, cx] == STATE.NONE: continue
		if seats[cy, cx] == STATE.OCCUPIED: occ += 1
		break
	cy = y
	while cy < seats.shape[0] - 1:  # S
		cy += 1
		if seats[cy, x] == STATE.NONE: continue
		if seats[cy, x] == STATE.OCCUPIED: occ += 1
		break
	cy = y
	cx = x
	while cy < seats.shape[0] - 1 and cx > 0:  # SW
		cy += 1
		cx -= 1
		if seats[cy, cx] == STATE.NONE: continue
		if seats[cy, cx] == STATE.OCCUPIED: occ += 1
		break
	cx = x
	while cx > 0:  # W
		cx -= 1
		if seats[y, cx] == STATE.NONE: continue
		if seats[y, cx] == STATE.OCCUPIED: occ += 1
		break
	cy = y
	cx = x
	while cy > 0 and cx > 0:  # NW
		cy -= 1
		cx -= 1
		if seats[cy, cx] == STATE.NONE: continue
		if seats[cy, cx] == STATE.OCCUPIED: occ += 1
		break
	return occ

def sol1(seats):
	return simulate(seats, star_occ, 5)

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	seats = np.zeros((len(puzzle_in), len(puzzle_in[0])), dtype=np.uint8)
	for y, (npline, lsline) in enumerate(zip(seats, puzzle_in)):
		for x, char in enumerate(lsline):
			if char == "L":
				seats[y, x] = STATE.FREE
			elif char == "#":
				seats[y, x] = STATE.OCCUPIED

	for i, f in enumerate((sol0, sol1)):
		res = f(seats)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
