from aoc_input import get_input
import aoc_helpers as ah

import numpy as np

DAY = 4
YEAR = 2021

class BingoBoard:
	def __init__(self, board) -> None:
		self._board = np.array(board)
		self._marked = np.zeros_like(self._board, dtype=bool)

		self._positions = {}
		for y, row in enumerate(self._board):
			for x, n in enumerate(row):
				if n in self._positions:
					raise ValueError(
						f"Duplicate number {n}! First appeared at {self._positions[n]}!"
					)
				self._positions[n] = (y, x)

	def mark(self, number) -> None:
		if number not in self._positions:
			return
		self._marked[self._positions[number]] = True

	def wins(self):
		return (
			any(row.all() for row in self._marked) or
			any(col.all() for col in self._marked.T)
		)

	def get_unmarked_sum(self):
		return (self._board[~self._marked]).sum()


def sol0(pzin):
	nums, boards = pzin
	boards = [BingoBoard(board) for board in boards]
	for number in nums:
		for board in boards:
			board.mark(number)
			if board.wins():
				return board.get_unmarked_sum() * number

def sol1(pzin):
	nums, boards = pzin
	boards = [BingoBoard(board) for board in boards]
	winners = set()
	# Mega scuffed indendation lol
	for number in nums:
		for i, board in enumerate(boards):
			if i in winners:
				continue
			board.mark(number)
			if board.wins():
				winners.add(i)
				if len(winners) == len(boards):
					return board.get_unmarked_sum() * number

	return -1

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n\n")
	puzzle_in = (
		[int(i) for i in puzzle_in[0].split(",")],
		[[[int(x) for x in row.split()] for row in board.split("\n")] for board in puzzle_in[1:]],
	)

	ah.print_solution(puzzle_in, DAY, YEAR, sol0, sol1)
