from aoc_input import get_input
import aoc_helpers as ah

DAY = 13
YEAR = 2020

def sol0(dep_t, buses):
	waiting = 0
	while True:
		for bus in buses:
			if bus is None:
				continue
			if (dep_t + waiting) % bus == 0:
				return waiting * bus
		waiting += 1

def sol1(_, buses):
	buses = buses.copy()
	while buses[0] is None: # Potential first Nones irrelevant I think
		buses.pop(0)
	offsets = [(bus, idx) for idx, bus in enumerate(buses) if bus is not None]
	cstep = offsets.pop(0)[0]
	timestep = 0
	while offsets:
		timestep += cstep
		slice = 0
		for bus, idx in offsets:
			if (timestep + idx) % bus == 0:
				slice += 1
				cstep *= bus
			else:
				break
		if slice:
			offsets = offsets[slice:]
	return timestep

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	puzzle_in = (
		int(puzzle_in[0]),
		[
			int(i) if i.isnumeric() else None
			for i in puzzle_in[1].split(",")
		]
	)

	for i, f in enumerate((sol0, sol1)):
		res = f(*puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
