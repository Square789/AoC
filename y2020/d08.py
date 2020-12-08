from aoc_input import get_input
import aoc_helpers as ah

DAY = 8
YEAR = 2020

def simulate(instructions):
	acc = 0
	instrcptr = 0
	run_already = [False for _ in instructions]
	while instrcptr < len(instructions):
		if run_already[instrcptr]:
			return (False, acc)
		run_already[instrcptr] = True
		instrc, arg = instructions[instrcptr]

		if instrc == "nop":
			pass
		elif instrc == "acc":
			acc += arg
		elif instrc == "jmp":
			instrcptr += arg - 1
		instrcptr += 1
	return (True, acc)

def sol0(pzin):
	return simulate(pzin)[1]

def sol1(pzin):
	for idx, instrc in enumerate(pzin):
		# Flip instruction if it's a nop or jmp
		if instrc[0] in ("nop", "jmp"):
			pzin[idx][0] = ("nop", "jmp")[instrc[0] == "nop"]
		else:
			continue
		res, acc = simulate(pzin)
		# Reset instruction to previous state
		pzin[idx][0] = ("nop", "jmp")[instrc[0] == "nop"]
		if res:
			return acc
	return None

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	puzzle_in = [ins.split() for ins in puzzle_in]
	puzzle_in = [[instrc, int(arg)] for instrc, arg in puzzle_in]

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
