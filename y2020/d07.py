from aoc_input import get_input
import aoc_helpers as ah

import re
from time import time

DAY = 7
YEAR = 2020

SEARCHED_BAG = "shiny gold"

BAG_EXP = re.compile(r"^(.*?) bags contain (.*)\.$")
CAN_CONTAIN_EXP = re.compile("(\d+) (.*?) bag[s]?")

class Bag:
	def __init__(self, color, holdable):
		self.color = color
		self.holdable = holdable
		self.holdable_names = {i[1] for i in holdable}
		self.parents = []


def build_bag_graph(pzin):
	bags = {}
	for line in pzin:
		bagcol, holdspec = BAG_EXP.match(line).groups()
		can_hold = CAN_CONTAIN_EXP.findall(holdspec)
		bags[bagcol] = Bag(
			bagcol,
			set((int(i), col) for i, col in can_hold),
		)

	# Add each node's parents to it.
	for color, bagspec in bags.items():
		for name in bagspec.holdable_names:
			bags[name].parents.append(bagspec)

	return bags

def rec_visit(bagspec, targets, can_hold_searched):
	if any(target in bagspec.holdable_names for target in (targets | can_hold_searched)):
		# print(f"{bagspec.color} can hold a container or the searched bag directly.")
		can_hold_searched.add(bagspec.color)
		for parent in bagspec.parents:
			rec_visit(parent, targets, can_hold_searched)

def rec_count(bag_graph, bag_col):
	acc = 0
	for count, color in bag_graph[bag_col].holdable:
		acc += count
		acc += count * rec_count(bag_graph, color)
	return acc

def sol0(bag_graph):
	can_hold_searched = set()

	targets = {SEARCHED_BAG}

	for bagspec in bag_graph.values():
		rec_visit(bagspec, targets, can_hold_searched)
	return len(can_hold_searched)

def sol1(bag_graph):
	return rec_count(bag_graph, SEARCHED_BAG)

def main():
	puzzle_in = build_bag_graph(get_input(YEAR, DAY).strip().split("\n"))

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
