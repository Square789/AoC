import re

from schema import Schema, Or, Optional, Regex

from aoc_input import get_input
import aoc_helpers as ah

DAY = 4
YEAR = 2020

def v_height(h):
	res, *_ = re.findall(r"(\d+)((?:cm|in))", h)
	if not res:
		return false
	n, unit = int(res[0]), res[1]
	if unit == "cm":
		return n in range(150, 194)
	elif unit == "in":
		return n in range(59, 77)
	return False

FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
VSCHEM = Schema({
	"byr": lambda x: int(x) in range(1920, 2003),
	"iyr": lambda x: int(x) in range(2010, 2021),
	"eyr": lambda x: int(x) in range(2020, 2031),
	"hgt": v_height,
	"hcl": Regex("^#[0-9a-f]{6}$"),
	"ecl": Or("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
	"pid": Regex("^[0-9]{9}$"),
	Optional("cid"): (lambda x: True),
})

def sol0(pzin):
	valid = 0
	for pairs in pzin:
		cfields = {pair[0] for pair in pairs}
		missing = FIELDS - cfields
		if missing == {"cid"} or not missing:
			valid += 1
	return valid

def sol1(pzin):
	valid = 0
	for pairs in pzin:
		passp = {pair[0]: pair[1] for pair in pairs}
		if VSCHEM.is_valid(passp):
			valid += 1
	return valid

def main():
	puzzle_in = get_input(YEAR, DAY)
	puzzle_in = [
		[w.split(":") for w in l.strip().split()]
		for l in puzzle_in.split("\n\n")
	]
	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
