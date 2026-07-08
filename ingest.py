import json
import urllib.request

def list_root_files(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    request = urllib.request.Request(url,headers={"User-Agent": "liscense-compliance-auditor"})
    response = urllib.request.urlopen(request)
    body = response.read()
    data = json.loads(body)
    file_names=[]
    for item in data:
        if item["type"] == "file":
            file_names.append(item["name"])
    return file_names

def is_license_source(name):
    license_keywords = ["license", "licence","readme", "copying", "notice"]
    manifest_keywords = ["package.json", "cargo.toml", "pyproject.toml", "setup.py", "setup.cfg"]
    name_lower = name.lower()
    for keyword in license_keywords:
        if name_lower.startswith(keyword):
            return True
    for keyword in manifest_keywords:
        if name_lower == keyword:
            return True
    return False

def get_file(owner, repo, name):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{name}"
    request = urllib.request.Request(url, headers={"User-Agent": "liscense-compliance-auditor"})
    response = urllib.request.urlopen(request)
    body = response.read()
    text = body.decode()

    return text


def get_sources(owner, repo):
    sources = {}
    file_names = list_root_files(owner, repo)
    for name in file_names:
        if is_license_source(name):
            text = get_file(owner, repo, name)
            sources[name] = text
    return sources

if __name__ == "__main__":
    sources = get_sources("pallets", "flask")
    for name, text in sources.items():
        print(f"==={name}({len(text)} chars) ===")
        print(text[:200])
        print()