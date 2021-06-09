import yaml
import argparse
from rich import console
from rich.syntax import Syntax

from .udev import udev_to_file
from .raspberry_pi import raspberry_pi_to_file

console = console.Console()

def main():
	parser = argparse.ArgumentParser(description='Generate a robot init configuration from a yaml file.')
	parser.add_argument('config_file')
	args = parser.parse_args()

	with open(args.config_file, 'r') as fin:
		cfg = yaml.safe_load(fin)

	if "users" in cfg:
		console.print("[green]Setting up users")
		for u in cfg["users"]:
			if isinstance(u, str):
				console.print(f"- {u}")
			else:
				console.print(f'- {u["name"]}')

	if "udev" in cfg:
		print(cfg['udev'])
		udev_to_file(cfg)

	if "raspberry_pi" in cfg:
		print(cfg['raspberry_pi'])
		raspberry_pi_to_file(cfg)

	console.print(Syntax(yaml.dump(cfg), 'yaml'))

	with open("cloud_init_generated.yaml", "w") as fo:
		fo.write(yaml.dump(cfg))

if __name__ == "__main__":
	main()