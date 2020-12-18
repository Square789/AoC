from aoc_input import get_input
import aoc_helpers as ah

from collections import deque

import re

DAY = 18
YEAR = 2020

RE_VALUE = re.compile(r"(\d+)")

# shoutouts to uni for the stuff below

# Expression     => Term, Multiplication* ;
# Addition       => "+" + Unary ;
# Term           => Unary + Addition* ;
# Multiplication => "*" + Term ;
# Unary          => Value | Brackets ;
# Brackets       => "(" + Expression + ")" ;

class UnOp:
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return f"{self.__class__.__name__}<{self.val!r}>"

class Value(UnOp):
	def eval(self):
		return self.val

class Brackets(UnOp):
	def eval(self):
		return self.val.eval()

class BinOp:
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __repr__(self):
		return f"{self.__class__.__name__}<{self.lhs!r}, {self.rhs!r}>"

class Add(BinOp):
	def eval(self):
		return (self.lhs.eval() + self.rhs.eval())

class Mul(BinOp):
	def eval(self):
		return (self.lhs.eval() * self.rhs.eval())

class Parser:
	def __init__(self, input_):
		self.inln = len(input_)
		self.input_ = input_
		self.pos = 0

	def curchar(self):
		return self.input_[self.pos] if self.pos < self.inln else "\x00"

	def parse_expr(self):
		self.consume_ws()
		res = self.parse_term()
		while True:
			self.consume_ws()
			new = self.parse_multiplication()
			if new is not None:
				res = Mul(res, new)
				continue
			break
		return res

	def parse_term(self):
		self.consume_ws()
		res = self.parse_unary()
		while True:
			self.consume_ws()
			new = self.parse_addition()
			if new is not None:
				res = Add(res, new)
				continue
			break
		return res

	def parse_unary(self):
		self.consume_ws()
		res = self.parse_value()
		if res is not None:
			return res

		res = self.parse_brackets()
		if res is not None:
			return res

		raise ValueError("Unable to find Unary")

	def parse_value(self):
		match = RE_VALUE.match(self.input_[self.pos:])
		if match:
			self.pos += len(match[0])
			return Value(int(match[1]))
		return None

	def parse_brackets(self):
		if self.curchar() != "(":
			return None
		self.pos += 1
		res = self.parse_expr()
		self.consume_ws()
		if res is None or self.curchar() != ")":
			raise ValueError("Bracket failure")
		self.pos += 1
		return Brackets(res)

	def parse_addition(self):
		if self.curchar() != "+":
			return None
		self.pos += 1
		return self.parse_unary()

	def parse_multiplication(self):
		if self.curchar() != "*":
			return None
		self.pos += 1
		return self.parse_term()

	def consume_ws(self):
		while self.curchar() in (" ", ):
			self.pos += 1

	def parse(self):
		return self.parse_expr()

class LinearEvaluator():
	"""
	Cheap evaluator that goes through the expression from left to right,
	calling its parsing method recursively when enocuntering brackets.
	"""
	def __init__(self, input_):
		input_ = "(" + input_ + ")"
		self.inln = len(input_)
		self.input_ = input_
		self.pos = 1

	def curchar(self):
		return self.input_[self.pos] if self.pos < self.inln else "\x00"

	def consume_ws(self):
		while self.curchar() in (" ", ):
			self.pos += 1

	def get_next_token(self):
		self.consume_ws()
		cc = self.curchar()
		if cc in ("(", ")", "+", "*"):
			self.pos += 1
			return cc
		match = RE_VALUE.match(self.input_[self.pos:])
		if match is None:
			raise ValueError("Unknown token")
		self.pos += len(match[0])
		return int(match[0])

	def eval(self):
		return self.bracket_eval()

	def bracket_eval(self):
		res = 0
		op = "__add__"
		while True:
			nexttoken = self.get_next_token() # Expecting value
			if nexttoken == "(":
				res = getattr(res, op)(self.bracket_eval())
			elif isinstance(nexttoken, int):
				res = getattr(res, op)(nexttoken)
			else:
				raise ValueError(f"Unexpected token {nexttoken!r}")
			nexttoken = self.get_next_token() # Expecting op or ")"
			if nexttoken == ")":
				return res
			elif nexttoken == "+":
				op = "__add__"
			elif nexttoken == "*":
				op = "__mul__"
			else:
				raise ValueError(f"Unexpected token {nexttoken!r}")

def sol0(pzin):
	res = 0
	for line in pzin:
		res += LinearEvaluator(line).eval()
	return res

def sol1(pzin):
	res = 0
	for line in pzin:
		res += Parser(line).parse().eval()
	return res

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n")

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in)
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
