# docker run -v $(pwd):/hyperconfig hyx python3 /hyperconfig/udev.py

from glob import glob
from pathlib import Path
from robo_init.util import literal_unicode

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

	def __init__(self, additional_rules=None):
		self.additional_rules = additional_rules or []

	custom_rules_folder = folders[0]

	def parse_rule(self, rule):
		return rule

	def to_cloud_init(self, result_yaml, prefix="robo_init"):
		if not self.additional_rules:
			return False

		entry = {
			"owner": "root:root",
			"content": literal_unicode("\n".join(self.additional_rules)),
			"path": str(self.custom_rules_folder / ("10-" + prefix + ".rules")),
			"permissions": "0644"
		}

		if "write_files" in result_yaml:
			result_yaml["write_files"].append(entry)
		else:
			result_yaml["write_files"] = [entry]
		return True

	def add_rules(self, rules):
		self.additional_rules = rules

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
					if len(ls) == 0 or ls[0] == '#':
						continue
					rules.append(ls)

		print('\n'.join(rules))

def udev_to_file(cfg):
	udev_entries = cfg.get("udev", [])

	for e in udev_entries:
		x = UDEV(e["rules"])
		x.to_cloud_init(cfg, e.get("name", "robo_init"))

	return cfg

if __name__ == "__main__":
	testrules = """
SUBSYSTEM=="block", ATTRS{idVendor}=="03f0", ACTION=="add", SYMLINK+="safety%n"
SUBSYSTEM=="block", ATTRS{idVendor}=="03f0", ACTION=="add", RUN+="/usr/local/bin/trigger.sh"
"""
	x = UDEV(testrules.splitlines())
	x.list_existing()
	result_yaml = {}
	x.to_cloud_init(result_yaml)
	print(result_yaml)