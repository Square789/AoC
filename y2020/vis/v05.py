
# Sorry, all out of meatballs, but the spaghetti in here is good nonetheless

import curses
import itertools
import random
import re
from time import sleep
import threading

RE_VALID_SEATSPEC = re.compile("^[FB]{7}[LR]{3}$")

BOX_URD = 0x251C
BOX_UDL = 0x2524
BOX_UD = 0x2502
BOX_UR = 0x2514

TOTAL_SIZE = (132, 20)

PLANE_FRAME = ((0, 0), (132, 14))
ACTIVE_FRAME = ((0, 13), (66, 5))
RESULT_FRAME = ((66, 13), (66, 5))
STATUS_FRAME = ((0, 18), (100, 2))

SPEC_SCROLLER_OFFSETX = 15
ACTIVE_INFO_NUM_FIELD = 16
ACTIVE_POST_NUM_FIELD = 24
ACTIVE_INFO_KEY_OFFSETX = 32
ACTIVE_INFO_VALUE_OFFSETX = 42
RESULT_VALUE_OFFSETX = 16
ACTIVE_INFO_VALUE_MAXLN = ACTIVE_FRAME[1][0] - ACTIVE_INFO_VALUE_OFFSETX - 3
RESULT_VALUE_MAXLN = RESULT_FRAME[1][0] - RESULT_VALUE_OFFSETX - 3
STATUS_MAXLN = STATUS_FRAME[1][0] - 4

COLOR_LIGHT_GREEN = 0xA
COLOR_LIGHT_AQUA = 0xB
COLOR_LIGHT_YELLOW = 0xE
COLOR_WHITE = 0x7
COLOR_GRAY = 0x8
COLOR_FULLWHITE = 0xF

VISUALIZE_BIN_SEARCH_FIRST = 16

class StatusThread(threading.Thread):
	ANIM_LENGTH = 7

	def __init__(self, status_win):
		super().__init__()
		self.status_win = status_win
		self._stlen = 0
		self.draw_anim = False
		self.stop_flag = threading.Event()
		self.animcycler = itertools.cycle(
			(" ▙█", " █▟", " █▙", " █▛", " █▜", " ▛█", " ▜█", " ▟█")
		)

	def set_status(self, status, draw_anim=True):
		self.draw_anim = draw_anim
		self._stlen = min(len(status), STATUS_MAXLN - self.ANIM_LENGTH)
		self.status_win.addstr(0, 2, f"{status: <{STATUS_MAXLN}}")
		self.status_win.refresh()

	def join(self):
		self.stop_flag.set()
		super().join()

	def run(self):
		while not self.stop_flag.is_set():
			if self.draw_anim:
				self.status_win.addstr(0, 2 + self._stlen, next(self.animcycler))
				self.status_win.refresh()
			sleep(.14)


def new_border_and_win(ws):
	"""
	Returns two curses windows, one serving as the border, the other as the
	inside from these *_FRAME tuples above.
	"""
	return (
		curses.newwin(ws[1][1], ws[1][0], ws[0][1], ws[0][0]),
		curses.newwin(ws[1][1] - 2, ws[1][0] - 2, ws[0][1] + 1, ws[0][0] + 1),
	)

def new_win(tup):
	"""
	Returns a curses window made from the (x,y),(w,h) tuples above
	"""
	return curses.newwin(tup[1][1], tup[1][0], tup[0][1], tup[0][0])

class PlaneVisualization():
	def __init__(self, input_):
		self.seat_specs = input_.splitlines()
		for spec in self.seat_specs:
			if RE_VALID_SEATSPEC.match(spec) is None:
				raise ValueError(f"{spec!r} is not a valid seat specification.")

	def run(self):
		self.init_curses()
		my, mx = self.screen.getmaxyx()
		if (mx, my) < TOTAL_SIZE:
			self.screen.addstr("Terminal too small!")
			self.screen.refresh()
			sleep(1)
		else:
			self.setup_windows()
			self.visualize()
		self.stop_curses()

	def init_curses(self):
		self.screen = curses.initscr()
		curses.start_color()
		curses.init_pair(1, COLOR_GRAY,        curses.COLOR_BLACK) # Darkest non-black color on black bg
		curses.init_pair(2, COLOR_FULLWHITE,   curses.COLOR_BLACK) # Full white on black bg
		curses.init_pair(3, COLOR_WHITE,       COLOR_GRAY) # Full white on black bg
		curses.init_pair(4, COLOR_LIGHT_GREEN, curses.COLOR_BLACK) # Green on black bg
		curses.init_pair(5, COLOR_LIGHT_AQUA,  curses.COLOR_BLUE ) # aqua on black bg, used to highlight max
		curses.init_pair(6, COLOR_LIGHT_YELLOW,curses.COLOR_BLACK)
		curses.init_pair(7, curses.COLOR_RED,  curses.COLOR_BLACK)
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)

	def stop_curses(self):
		curses.curs_set(1)
		curses.nocbreak()
		curses.echo()
		curses.endwin()

	def setup_windows(self):
		## Frame creation
		plane_b,  self.plane_win  = new_border_and_win(PLANE_FRAME)
		active_b, self.active_win = new_border_and_win(ACTIVE_FRAME)
		result_b, self.result_win = new_border_and_win(RESULT_FRAME)
		self.status_win = new_win(STATUS_FRAME)

		## Borders
		plane_b.border()
		active_b.border(0, 0, 0, 0, BOX_URD, 0, BOX_URD, 0)
		result_b.border(0, 0, 0, 0, 0, BOX_UDL, 0, 0)
		self.status_win.addstr(0, 0, "│")
		self.status_win.addstr(1, 0, "└")
		self.status_win.addstr(1, 1, "─"*98)

		for win in (plane_b, active_b, result_b, self.status_win):
			win.refresh()

	@staticmethod
	def seat_to_screen_pos(row, col):
		"""
		Given a seat coordinate from 0, 0 (x, y) -> (row, col),
		returns actual screen coordinate corresponding to the seat in
		self.plane_win
		"""
		return (1 + row, 1 + col + (col > 2) + (col > 4))

	def vis_seat_search(self, seat_ids):
		"""
		Takes existing/occupied seat_ids as a set, returns the free seat or
		None if not locatable, as well as vizualizing the process.
		"""
		for seat_id in range(128*8):
			prev = seat_id - 1
			next_ = seat_id + 1

			# Draw C, N, P markers
			x, y = self.seat_to_screen_pos(seat_id >> 3, seat_id & 7)
			self.plane_win.addstr(y, x, "C", curses.color_pair(5))

			if prev >= 0:
				x, y = self.seat_to_screen_pos(prev >> 3, prev & 7)
				self.plane_win.addstr(y, x, "P", curses.color_pair(6))

			if next_ < 1024:
				x, y = self.seat_to_screen_pos(next_ >> 3, next_ & 7)
				self.plane_win.addstr(y, x, "N", curses.color_pair(6))

			self.plane_win.refresh()

			self.active_win.addstr(0, ACTIVE_INFO_NUM_FIELD, f"{seat_id: >5}")
			self.active_win.addstr(1, ACTIVE_INFO_NUM_FIELD, f"{prev: >5}")
			self.active_win.addstr(2, ACTIVE_INFO_NUM_FIELD, f"{next_: >5}")

			for i, seat_id_ in enumerate((seat_id, prev, next_)):
				if seat_id_ in seat_ids:
					self.active_win.addstr(
						i, ACTIVE_POST_NUM_FIELD, "Exists        ",
						curses.color_pair(7 if i == 0 else 4)
					)
				else:
					self.active_win.addstr(
						i, ACTIVE_POST_NUM_FIELD, "Does not exist",
						curses.color_pair(4 if i == 0 else 7)
					)

			self.active_win.refresh()

			if seat_id not in seat_ids and (prev in seat_ids) and (next_ in seat_ids):
				for unvisited_seat in range(seat_id + 2, 128*8):
					ux, uy = self.seat_to_screen_pos(unvisited_seat >> 3, unvisited_seat & 7)
					self.plane_win.addstr(uy, ux, "[" if unvisited_seat in seat_ids else " ", curses.color_pair(0))
				self.plane_win.refresh()
				return seat_id

			# Reset P marker
			if prev >= 0:
				x, y = self.seat_to_screen_pos(prev >> 3, prev & 7)
				self.plane_win.addstr(y, x, "[" if prev in seat_ids else " ", curses.color_pair(0))

			sleep(1.01 - (seat_id/1024)**.005)

		return None

	def vis_binsearch(self, iter, spec, _pos_remember, cmax):
		"""
		Visualize binary search by drawing rectangles all over the screen.
		iter: How often this method was called already in the simulation run
		spec: Seatspec as defined by the regular expression at the top.
		_pos_remember: List that should contain the direct screen coordinates
		for seats already processed so they aren't overdrawn again when the
		search rect gets smaller.
		cmax: Screen coordinates of the max seat or None.
		This function sucks, but works
		"""
		#Draw initial binsearch rect
		delay = .25 - ((iter/VISUALIZE_BIN_SEARCH_FIRST)**.2)*.24
		for i in range(8):
			self.plane_win.chgat(
				self.seat_to_screen_pos(-1, i)[1],
				1, 128, curses.color_pair(3)
			)
		self.plane_win.refresh()
		if iter == 0:
			sleep(5)

		# Binsearch rows
		row_min = 0
		row_max = 127
		step = 64
		for i, c in enumerate(spec[:7]):
			if c == "F":
				row_max -= step
			else:
				row_min += step
			for j in range(10):
				self.plane_win.chgat(
					1 + j,
					1 + (row_max + 1 if c == "F" else row_min - step),
					step,
					curses.color_pair(1),
				)
			for x, y in _pos_remember:
				self.plane_win.chgat(y, x, 1, curses.color_pair(2))
			if cmax is not None:
				self.plane_win.chgat(cmax[1], cmax[0], 1, curses.color_pair(5))
			self.active_win.chgat(1, SPEC_SCROLLER_OFFSETX + 2 + i, 1, curses.color_pair(4))
			self.plane_win.refresh()
			self.active_win.refresh()
			step //= 2
			sleep(delay)
		row = row_min

		# Binsearch columns
		col_min = 0
		col_max = 7
		step = 4
		for i, c in enumerate(spec[7:]):
			if c == "L":
				col_max -= step
			else:
				col_min += step
			offset = col_max + 1 if c == "L" else col_min - step
			for j in range(step):
				tx, ty = self.seat_to_screen_pos(row, offset + j)
				self.plane_win.chgat(ty, tx, 1, curses.color_pair(1))
			for x, y in _pos_remember:
				self.plane_win.chgat(y, x, 1, curses.color_pair(2))
			if cmax is not None:
				self.plane_win.chgat(cmax[1], cmax[0], 1, curses.color_pair(5))
			self.active_win.chgat(1, SPEC_SCROLLER_OFFSETX + 2 + 7 + i, 1, curses.color_pair(4))
			self.plane_win.refresh()
			self.active_win.refresh()
			step //= 2
			sleep(delay)
		col = col_min
		_pos_remember.append(self.seat_to_screen_pos(row, col))

	def visualize(self):
		## Text for Part 1
		self.active_win.addstr(0, 1, f"{0: ^{SPEC_SCROLLER_OFFSETX - 2}}")
		self.active_win.addstr(0, SPEC_SCROLLER_OFFSETX, "|            |")
		self.active_win.addstr(1, 1, "Current seat: >            <")
		self.active_win.addstr(2, 1, f"{len(self.seat_specs): ^{SPEC_SCROLLER_OFFSETX - 2}}")
		self.active_win.addstr(2, SPEC_SCROLLER_OFFSETX, "|            |")
		self.active_win.addstr(0, ACTIVE_INFO_KEY_OFFSETX, "Row:")
		self.active_win.addstr(1, ACTIVE_INFO_KEY_OFFSETX, "Column:")
		self.active_win.addstr(2, ACTIVE_INFO_KEY_OFFSETX, "Id:")
		self.result_win.addstr(1, 1, "Current max:")

		## Seats
		self.plane_win.attron(curses.color_pair(1))
		for line in range(8):
			self.plane_win.addstr(
				self.seat_to_screen_pos(-1, line)[1],
				1, "["*128, curses.color_pair(1)
			)
		self.plane_win.refresh()
		self.plane_win.attron(curses.color_pair(0))

		status_thread = StatusThread(self.status_win)
		status_thread.start()

		# Begin
		# Part 1
		SPEC_AMT = len(self.seat_specs)
		# Holds position of the first VISUALIZE_BIN_SEARCH_FIRST seats so they
		# are properly redrawn during binary search.
		seat_ids = set()
		_pos_remember = []
		cmax = cmax_pos = row = col = seat_id = None

		self.active_win.addstr(0, ACTIVE_INFO_VALUE_OFFSETX, str(row))
		self.active_win.addstr(1, ACTIVE_INFO_VALUE_OFFSETX, str(col))
		self.active_win.addstr(2, ACTIVE_INFO_VALUE_OFFSETX, str(seat_id))
		self.result_win.addstr(1, RESULT_VALUE_OFFSETX, str(cmax))
		self.active_win.refresh()
		self.result_win.refresh()

		status_thread.set_status("Part 1: Finding maximum seat id")
		for i, spec in enumerate(self.seat_specs):
			# Draw Seat Specs into the scroller
			if i != 0:
				self.active_win.addstr(
					0, SPEC_SCROLLER_OFFSETX + 2,
					self.seat_specs[i - 1], curses.color_pair(1)
				)
			self.active_win.addstr(1, SPEC_SCROLLER_OFFSETX + 2, spec)
			if i != SPEC_AMT - 1:
				self.active_win.addstr(
					2, SPEC_SCROLLER_OFFSETX + 2,
					self.seat_specs[i + 1], curses.color_pair(1)
				)
			else:
				self.active_win.addstr(2, SPEC_SCROLLER_OFFSETX + 2, "          ")
			# Draw current index
			self.active_win.addstr(0, 1, f"{i: ^{SPEC_SCROLLER_OFFSETX - 2}}")
			self.active_win.refresh()

			# Visualize binary subdivision for first few specs
			if i < VISUALIZE_BIN_SEARCH_FIRST:
				self.vis_binsearch(i, spec, _pos_remember, cmax_pos)

			# Mega cheap, get seat_id, row and col
			seat_id = int(spec.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2)
			row, col = seat_id >> 3, seat_id & 7

			seat_ids.add(seat_id)

			# Color current seat in brighter color
			tx, ty = self.seat_to_screen_pos(row, col)
			self.plane_win.chgat(ty, tx, 1, curses.color_pair(2))
			self.plane_win.refresh()

			# New maximum id?
			if cmax is None or seat_id > cmax:
				cmax = seat_id
				# Decolor old maximum seat
				if cmax_pos is not None:
					self.plane_win.chgat(cmax_pos[1], cmax_pos[0], 1, curses.color_pair(2))
				cmax_pos = self.seat_to_screen_pos(row, col)
				self.plane_win.chgat(cmax_pos[1], cmax_pos[0], 1, curses.color_pair(5))
				self.result_win.addstr(1, 1, f"Current max: {cmax: <{RESULT_VALUE_MAXLN}}")
				self.result_win.refresh()
				self.plane_win.refresh()

			self.active_win.addstr(0, ACTIVE_INFO_VALUE_OFFSETX, f"{row: <{ACTIVE_INFO_VALUE_MAXLN}}")
			self.active_win.addstr(1, ACTIVE_INFO_VALUE_OFFSETX, f"{col: <{ACTIVE_INFO_VALUE_MAXLN}}")
			self.active_win.addstr(2, ACTIVE_INFO_VALUE_OFFSETX, f"{seat_id: <{ACTIVE_INFO_VALUE_MAXLN}}")
			self.active_win.refresh()

			sleep(.008)

		status_thread.set_status("Maximum found!", False)

		# Blink max repeatedly
		for _ in range(5):
			self.result_win.addstr(
				1, 1, f"Current max: {cmax: <{RESULT_VALUE_MAXLN}}", curses.color_pair(4))
			self.result_win.refresh()
			sleep(.4)
			self.result_win.addstr(
				1, 1, f"Current max: {' ': <{RESULT_VALUE_MAXLN}}",)
			self.result_win.refresh()
			sleep(.3)

		# Purge info windows
		self.result_win.clear()
		self.active_win.clear()
		self.result_win.refresh()
		self.active_win.refresh()

		status_thread.set_status("Removing seats")
		BACKDRAG = 8
		# Thanos snap seats
		for x in range(128 + BACKDRAG):
			for y in range(8):
				for t in range(BACKDRAG):
					tx, ty = self.seat_to_screen_pos(x - t, y)
					if 0 < tx < 129 and random.randint(1, BACKDRAG * 10 - 10) < t * 10 + 1:
						self.plane_win.addstr(ty, tx, " ")
			self.plane_win.refresh()
			sleep(.006 + x/6000)

		status_thread.set_status("Drawing existing seats")
		# Part 2
		# Add new text fields to lower windows
		self.active_win.addstr(0, 1, "Current seat  [     ]: ")
		self.active_win.addstr(1, 1, "Previous seat [     ]: ")
		self.active_win.addstr(2, 1, "Next seat     [     ]: ")
		self.result_win.addstr(1, 1, "Your seat: ?")

		self.active_win.refresh()
		self.result_win.refresh()

		# Draw all existing seats
		for i, seat_id in enumerate(seat_ids):
			row, col = seat_id >> 3, seat_id & 7
			x, y = self.seat_to_screen_pos(row, col)
			self.plane_win.addstr(y, x, "[", curses.color_pair(2))
			self.plane_win.refresh()
			sleep(.001)

		status_thread.set_status("Part 2: Searching for own seat")
		own_seat = self.vis_seat_search(seat_ids)

		if own_seat is None:
			status_thread.set_status("Failed to find seat!", False)
		else:
			# Blink seat number repeatedly
			status_thread.set_status("Seat found!", False)
			for _ in range(5):
				self.result_win.addstr(
					1, 1, f"Your seat: {own_seat: <{RESULT_VALUE_MAXLN}}", curses.color_pair(4))
				self.result_win.refresh()
				sleep(.4)
				self.result_win.addstr(
					1, 1, f"Your seat: {' ': <{RESULT_VALUE_MAXLN}}",)
				self.result_win.refresh()
				sleep(.3)

		sleep(1)

		status_thread.join()

def main(pz_in):
	pv = PlaneVisualization(pz_in)
	try:
		pv.run()
	except Exception as e:
		PlaneVisualization.stop_curses(None)
		raise e from None

if __name__ == "__main__":
	# In order to run this file with your own puzzle input, you'll need to add an open
	# statement here and pass the input to main as a simple string.
	main(None)
