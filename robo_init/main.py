import os
import copy
import yaml
import argparse
from rich import console
from rich.syntax import Syntax
from pathlib import Path
from .udev import udev_to_file
from .raspberry_pi import raspberry_pi_to_file

console = console.Console()

def dump_to_folder(cfg, out_folder):
	os.makedirs(out_folder, exist_ok=True)

	cfg = copy.copy(cfg)

	if "network" in cfg:
		network = cfg["network"]
		with open(out_folder / "network-config", "w") as fo:
			fo.write("#cloud-config\n\n")
			fo.write(yaml.dump(cfg["network"]))
		del cfg["network"]

	delf = []
	for file in cfg.get("write_files", []):
		if file["path"].startswith("/boot"):
			p = file["path"]
			fn = p.split('/')[-1]
			with open(out_folder / fn, "w") as fo:
				fo.write(file["content"])
			delf.append(file)

	if delf:
		for x in delf:
			cfg["write_files"].remove(x)

	with open(out_folder / "user-data", "w") as fo:
		fo.write("#cloud-config\n\n")
		fo.write(yaml.dump(cfg))

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

	out_folder = Path("generated_boot_config")
	dump_to_folder(cfg, out_folder)


if __name__ == "__main__":
	main()