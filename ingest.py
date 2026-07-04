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


if __name__ == "__main__":
    print(list_root_files("pallets", "flask"))
    print(is_license_source("LICENSE.txt"))
    print(is_license_source("README.md"))
    print(is_license_source("gitignore"))
