import subprocess, sys, re

args = sys.argv[1:]
user = args[0]
passw = args[1]
cli_output = subprocess.check_output("git config -f .gitmodules -l | awk '{split($0, a, /=/); split(a[1], b, /\./); print a[1], a[2]}'", shell=True)
cli_output = cli_output.decode("utf-8").split("\n")
submodules = {}
for line in cli_output:
    key_value = line.split(" ")
    if len(key_value) > 1:
        keys = key_value[0].split(".")
        value = key_value[1]
        if (len(keys) > 2 and keys[0] == 'submodule'):
            if (keys[1] not in submodules.keys()):
                submodules[keys[1]] = {}
            submodules[keys[1]][keys[2]] = value

for i in submodules:
    path = submodules[i]['path']
    url = submodules[i]['url']
    matches = re.findall("git@(.+)\.git", url)
    if (len(matches) > 0):
        match = "/".join(matches[0].split(":"))
        repo_url = f"https://{user}:{passw}@{match}"
        subprocess.check_output(f"rm -rf {path}", shell=True)
        subprocess.check_output(f"git clone --depth 1 {repo_url} {path}", shell=True)
        