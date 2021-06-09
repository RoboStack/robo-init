from glob import glob
from pathlib import Path
from collections import OrderedDict

from rich.console import Console

console = Console()

class RaspberryPiConfig:

	folder = Path("/boot/firmware")
	verbose = True

	def _parse_file(self, file, config_dict):
		if self.verbose:
			console.print(f"[yellow]Reading [/yellow]{self.folder / file}")
		with open(self.folder / file, 'r') as fin:
			lines = fin.readlines()
			for l in lines:
				x = l.strip()
				if len(x) == 0:
					continue
				elif x[0] == '#':
					console.print(f"[grey]{x}")
				elif x.startswith('include '):
					self._parse_file(x.split(' ')[1], config_dict)
				elif '=' in x:
					l, r = x.split('=', 1)

					if '#' in r:
						r, comment = r.split('#')
						console.print(f"[grey]# {comment}")
						r = r.strip()

					if r.endswith('.txt') and (self.folder / r).exists():
						console.print(f"[yellow]Reading [/yellow]{self.folder / r}")
						with open(self.folder / r, 'r') as fi:
							rval = fi.read()
						config_dict.append((l, rval))
					else:
						config_dict.append((l, r))

					if self.verbose:
						console.print(f"[green]{config_dict[-1][0]}=[bold]{config_dict[-1][1]}")



	def list_existing(self):
		entry_point = self.folder / "config.txt"

		config_options = []
		self._parse_file('config.txt', config_options)

		for k, v in config_options:
			print(f"{k}={v}")

if __name__ == "__main__":
	x = RaspberryPiConfig()
	x.folder = Path(__file__).parent.parent / "test/rpi/config_a"
	x.list_existing()