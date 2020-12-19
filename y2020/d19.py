from aoc_input import get_input
import aoc_helpers as ah

import re

RE_TERM = re.compile("\"(.)\"")

DAY = 19
YEAR = 2020

def rec_build_re(src, rules, patched8_11=False):
	if patched8_11 and src in (8, 11):
		if src == 8:
			res = "(?:" + rec_build_re(42, rules, patched8_11) + ")+"
		else:
			res = ("(?:" + "|".join(
				"(?:" + rec_build_re(42, rules, patched8_11) + f"){{{i}}}(?:" +
				rec_build_re(31, rules, patched8_11) + f"){{{i}}}"
				for i in range(1, 10)  # MEEEGA CHEAP
			) + ")")
	elif isinstance(rules[src], str):
		res = rules[src]
	else:
		res = ("(?:" + "|".join(
				''.join(
					rec_build_re(elem, rules, patched8_11)
					for elem in alt
				) for alt in rules[src]
			) + ")")
	return res

def sol0(rules, data):
	UNHOLY_RE = re.compile("^" + rec_build_re(0, rules) + "$")
	acc = 0
	for line in data:
		if UNHOLY_RE.match(line):
			acc += 1
	return acc

def sol1(rules, data):
	UNHOLY_RE = re.compile("^" + rec_build_re(0, rules, True) + "$")
	acc = 0
	for line in data:
		if UNHOLY_RE.match(line):
			acc += 1
	return acc

def main():
	txtrules, data = get_input(YEAR, DAY).strip().split("\n\n")
	txtrules = txtrules.strip().split("\n")
	data = data.strip().split("\n")
	rules = {}
	for rawline in txtrules:
		colp, colb = map(str.strip, rawline.split(":"))
		id_ = int(colp)
		if "\"" in colb:
			rules[id_] = RE_TERM.findall(colb)[0][0]
		else:
			alternatives = [*map(str.strip, colb.split("|"))]
			rules[id_] = tuple(
				tuple(map(int, alt.strip().split())) for alt in alternatives
			)

	for i, f in enumerate((sol0, sol1)):
		res = f(rules, data)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
