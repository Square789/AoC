from aoc_input import get_input
import aoc_helpers as ah

from collections import deque

DAY = 22
YEAR = 2020

def sol0(pzin):
	p0 = deque()
	p1 = deque()

	p0deck, p1deck = pzin

	for card in p0deck:
		p0.append(int(card))
	for card in p1deck:
		p1.append(int(card))

	while p0 and p1:
		played = (p0.popleft(), p1.popleft())
		if played[0] > played[1]: # Crab gets advantage cause crabs are pretty cool
			p0.append(played[0])
			p0.append(played[1])
		else:
			p1.append(played[1])
			p1.append(played[0])

	winner = p0 if p0 else p1

	res = 0
	cur_card_value = len(winner)
	for card in winner:
		res += card * cur_card_value
		cur_card_value -= 1

	return res

def get_game_hash(p0, p1):
	return hash(hash(tuple(p0)) + hash(tuple(p1)))

def sol1(pzin):
	p0deck, p1deck = pzin
	seen_states = set()

	p0 = deque()
	p1 = deque()

	for card in p0deck:
		p0.append(int(card))
	for card in p1deck:
		p1.append(int(card))

	while p0 and p1:
		game_hash = get_game_hash(p0, p1)
		if game_hash in seen_states:
			break
		seen_states.add(game_hash)

		played = (p0.popleft(), p1.popleft())
		if played[0] <= len(p0) and played[1] <= len(p1):
			winner = sol1(([*p0][:played[0]], [*p1][:played[1]]))[0]
		else:
			winner = 0 if played[0] > played[1] else 1

		if winner == 0:
			p0.append(played[0])
			p0.append(played[1])
		else:
			p1.append(played[1])
			p1.append(played[0])

	if p0:
		winner = p0
		winnerid = 0
	else:
		winner = p1
		winnerid = 1

	res = 0
	cur_card_value = len(winner)
	for card in winner:
		res += card * cur_card_value
		cur_card_value -= 1

	return (winnerid, res)

def main():
	puzzle_in = get_input(YEAR, DAY).strip().split("\n\n")
	puzzle_in = tuple(
		(*map(int, half.split("\n")[1:]),) for half in puzzle_in
	)

	for i, f in enumerate((sol0, sol1)):
		res = f(puzzle_in) if i == 0 else f(puzzle_in)[1]
		if res is None:
			continue
		print(
			f"===[AoC 2020, {DAY}.{i} result:]===\n{res}\n"
			f"{'='*len(str(DAY))}============================"
		)
