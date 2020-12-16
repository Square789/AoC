from aoc_input import get_input
import aoc_helpers as ah

import re
try:
	from tabulate import tabulate
except ImportError:
	tabulate = lambda *_: print("The tabulate module seems to be missing")

RE_TICKET = re.compile(r"^(.*): (\d+)-(\d+) or (\d+)-(\d+)$")

DAY = 16
YEAR = 2020

def fancify_candidates(rules, res):
	print(tabulate(
		[
			[name, *["X" if idx in value else "" for idx in range(len(rules))]]
			for name, value in res.items()
		],
		headers = ["Name"] + [*map(str, range(len(rules)))]
	))

def rulematch(rule, value):
	return value in rule[0] or value in rule[1]

def sol0(rules, _, tickets):
	err_rate = 0
	valid_tickets = []
	for ticket in tickets:
		for field in ticket:
			if not any(rulematch(rule, field) for rule in rules.values()):
				err_rate += field
				break
		else:
			valid_tickets.append(ticket)
	return (err_rate, valid_tickets)

def sol1(rules, own_ticket, tickets):
	tickets = sol0(rules, None, tickets)[1]
	res = {rulename: set() for rulename in rules.keys()}
	for idx, value_row in enumerate(zip(*tickets)):
		for rulename, rule in rules.items():
			if all(rulematch(rule, value) for value in value_row):
				res[rulename].add(idx)

	used_for_elimination_already = set()
	while not all(len(candidates) == 1 for candidates in res.values()):
		for key, candidates in res.items():
			if len(candidates) == 1 and key not in used_for_elimination_already:
				used_for_elimination_already.add(key)
				for other_key, other_cands in res.items():
					if key == other_key:
						continue
					res[other_key] = other_cands - candidates
				break
		else:
			raise ValueError("Can't reliably resolve")

	mul = 1
	for key, value in res.items():
		if key.startswith("departure"):
			mul *= own_ticket[[*value][0]]
	return mul

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n\n")
	ticket_rules = [
		RE_TICKET.match(line)
		for line in puzzle_in[0].split("\n")
	]
	ticket_rules = {
		match[1]: (
			range(int(match[2]), int(match[3])+1),
			range(int(match[4]), int(match[5])+1),
		)
		for match in ticket_rules
	}
	own_ticket = [int(i) for i in puzzle_in[1].split("\n")[1].split(",")]
	other_tickets = [
		[int(i) for i in line.split(",")]
		for line in puzzle_in[2].split("\n")[1:]
	]

	for i, f in enumerate((sol0, sol1)):
		res = f(ticket_rules, own_ticket, other_tickets)
		if res is None:
			continue
		if i == 0:
			res = res[0]
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
