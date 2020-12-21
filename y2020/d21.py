from aoc_input import get_input
import aoc_helpers as ah

from functools import reduce
from pprint import pprint
import re

RE_ALLERGENS = re.compile(r"\(contains (.*)\)")

DAY = 21
YEAR = 2020

def build_ing_all_map(pzin):
	ing_all_map = {}
	ingredients = set()
	for ingrs, allergs in pzin:
		for ingr in ingrs:
			ingredients.add(ingr)
			if ingr in ing_all_map:
				ing_all_map[ingr] |= allergs
			else:
				ing_all_map[ingr] = allergs.copy()

	for ingrs, allergs in pzin:
		for ingredient in ingredients:
			if ingredient not in ingrs:
				ing_all_map[ingredient] -= allergs

	could_reduce = True
	used_for_reduction_already = set()
	while could_reduce:
		could_reduce = False
		for ing, allset in ing_all_map.items():
			if len(allset) == 1 and ing not in used_for_reduction_already:
				could_reduce = True
				used_for_reduction_already.add(ing)
				for ing2, allset2 in ing_all_map.items():
					if ing == ing2:
						continue
					ing_all_map[ing2] = allset2 - allset
				break

	pprint(ing_all_map)

	return ing_all_map

def sol0(pzin):
	ing_all_map = build_ing_all_map(pzin)

	non_allergens = {ing for ing, allset in ing_all_map.items() if not allset}

	count = 0
	for ings, allergs in pzin:
		for non_allergen in non_allergens:
			count += ings.count(non_allergen)

	pprint(ing_all_map)

	return count



def sol1(pzin):
	ing_all_map = build_ing_all_map(pzin)

	return ",".join(e[0] for e in sorted(
		[(k, [*v][0]) for k, v in ing_all_map.items() if v],
		key=lambda x: x[1])
	) # Look Ma, no readability!

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")
	data = [
		(
			[*map(str.strip, line.split("(")[0].split())],
			{*map(str.strip, RE_ALLERGENS.search(line)[1].split(","))}
		) for line in puzzle_in
	]

	for i, f in enumerate((sol0, sol1)):
		res = f(data)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
