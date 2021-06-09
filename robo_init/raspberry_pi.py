from glob import glob
from pathlib import Path
from collections import OrderedDict

from rich.console import Console

from robo_init.util import literal_unicode

console = Console()

class RaspberryPiConfig:

	folder = Path("/boot/firmware")
	verbose = True

	additional_commands = []

	def __init__(self, additional_commands=None):
		if additional_commands:
			self.additional_commands = additional_commands

	def add_commands(self, rules):
		self.additional_commands = rules

	def to_cloud_init(self, result_yaml):
		if not self.additional_commands:
			return False

		entry = {
			"owner": "root:root",
			"content": literal_unicode("\n".join(self.additional_commands)),
			"path": str(self.folder / "usercfg.txt"),
			"permissions": "0644"
		}

		if "write_files" in result_yaml:
			result_yaml["write_files"].append(entry)
		else:
			result_yaml["write_files"] = [entry]
		return True

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

def raspberry_pi_to_file(cfg):
	rpi_entries = cfg.get("raspberry_pi", {}).get("config", [])

	x = RaspberryPiConfig(rpi_entries)
	x.to_cloud_init(cfg)

	del cfg["raspberry_pi"]

	return cfg


if __name__ == "__main__":
	x = RaspberryPiConfig()
	x.folder = Path(__file__).parent.parent / "test/rpi/config_a"
	x.list_existing()