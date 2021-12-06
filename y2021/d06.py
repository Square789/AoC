from aoc_input import get_input
import aoc_helpers as ah

DAY = 6
YEAR = 2021

def simulate(fish, days):
	for _ in range(days):
		reproducing = fish[0]
		fish = fish[1:] + [reproducing]
		fish[6] += reproducing

	return sum(fish)

def sol0(setup_data, _):
	return simulate(setup_data, 80)

def sol1(setup_data, _):
	return simulate(setup_data, 256)

def get_data():
	return [int(x) for x in get_input(YEAR, DAY).strip().split(",")]

def setup(puzzle_data):
	fish = [0 for _ in range(9)]
	for i in puzzle_data:
		fish[i] += 1
	return fish

def main():
	ah.print_solution2(get_data, setup, DAY, YEAR, sol0, sol1)

if __name__ == "__main__":
	main()
