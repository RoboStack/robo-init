from glob import glob
from pathlib import Path
from collections import OrderedDict

from rich.console import Console

console = Console()

class RaspberryPiConfig:

	folder = Path("/boot/config")
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
				if x[0] == '#':
					console.print(f"[grey]{x}")
				if x.startswith('include '):
					self._parse_file(x.split(' ')[1], config_dict)

				if '=' in x:
					l, r = x.split('=', 1)

					if '#' in r:
						r, comment = r.split('#')
						console.print(f"[grey]# {comment}")
						r = r.strip()

					if r.endswith('.txt') and (self.folder / r).exists():
						console.print(f"[yellow]Reading [/yellow]{self.folder / r}")
						with open(self.folder / r, 'r') as fi:
							rval = fi.read()
						config_dict[l] = rval
					else:
						config_dict[l] = r

					if self.verbose:
						console.print(f"[green]{l}=[bold]{config_dict[l]}")



	def list_existing(self):
		entry_point = self.folder / "config.txt"

		config_options = OrderedDict()
		self._parse_file('config.txt', config_options)

		for k, v in config_options.items():
			print(f"{k}={v}")

if __name__ == "__main__":
	x = RaspberryPiConfig()
	x.folder = Path(__file__).parent.parent / "test/rpi/config_a"
	x.list_existing()