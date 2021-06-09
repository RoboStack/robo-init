# docker run -v $(pwd):/hyperconfig hyx python3 /hyperconfig/udev.py

from glob import glob
from pathlib import Path

class UDEV():
	"""
	It allows you to identify devices based on their properties, like vendor ID
	and device ID, dynamically. udev runs in userspace (as opposed to devfs which
	was executed in kernel space).
	"""
	folders = [Path(p) for p in [
		"/etc/udev/udev.conf",
		"/lib/udev/rules.d",
		"/run/udev/rules.d"
	]]

	def parse_rule(self, rule):
		return rule

	def list_existing(self):
		elems = []
		for f in self.folders:
			if f.exists():
				elems.extend(glob(str(f / "*.rules")))
		ordered_rule_files = sorted(elems)

		rules = []

		for rf in ordered_rule_files:
			with open(rf, "r") as rf_in:
				lines = rf_in.readlines()
				for l in lines:
					ls = l.strip()
					if ls[0] == '#':
						continue
					rules.append(ls)

		print(rules)

if __name__ == "__main__":
	x = UDEV()
	x.list_existing()