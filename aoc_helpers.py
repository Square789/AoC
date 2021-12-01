
def prod(it):
	res = 1
	for el in it:
		res *= el
	return res


def print_solution(puzzle_in, day, year, *sols):
	for i, f in enumerate(sols):
		if (res := f(puzzle_in)) is None:
			continue
		print(
			f"===[AoC {year}, {day}.{i} result:]===\n{res}\n"
			f"{'='*len(str(day))}============================"
		)
