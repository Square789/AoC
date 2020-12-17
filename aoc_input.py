import json
from pathlib import Path

class UnexpectedResponseError(RuntimeError):
	pass

def get_input(year, day):
	thisdir = Path(__file__).parent / f"y{year}"

	with open(Path(thisdir, "input.json"), "r") as f:
		data = {int(k): v for k, v in json.load(f).items()}

	if day not in data:
		import requests

		with open(Path(thisdir, "cookie.txt"), "r") as f:
			SESSCOOKIE = f.read().strip()

		resp = requests.get(
			f"https://adventofcode.com/{year}/day/{day}/input",
			cookies = {
				"session": SESSCOOKIE,
			}
		)

		if resp.status_code != 200:
			raise UnexpectedResponseError(f"Expected 200, got {resp.status_code}")

		data[day] = resp.content.decode("utf-8")

		with open(Path(thisdir, "input.json"), "w") as f:
			json.dump(data, f, indent = 4)

	return data[day]

if __name__ == "__main__":
	print(get_input(2020, 1))
