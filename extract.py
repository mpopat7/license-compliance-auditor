import json
import urllib.request
from ingest import get_sources

OLLAMA_HOST = "http://192.168.5.163:11434"

def call_llm(prompt: str, model: str = "qwen3:30b") -> str:
    payload = {"model": model, "prompt": prompt, "stream": False}
    body_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",data=body_bytes, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        response_data = json.loads(response_body)
        return response_data["response"]
    

def identify_license(sources: dict[str,str]) -> str:
     prompt = f"Identify the SPDX license for this project. \n\n"

     for name, text in sources.items():
         prompt+= f"=={name}==\n"
         prompt+= text[:4000]
         prompt+= "\n\n"
     prompt+= "Return only the SPDX license identifier, like MIT, BSD-3-Clause, Apache-2.0, or NOASSERTION."
     return call_llm(prompt)

def identify_license_with_citation(sources: dict[str,str]) -> str:
    prompt = f"Identify the SPDX license for this project using the source files below. \n\n"

    for name, text in sources.items():
        prompt+= f"=={name}==\n"
        prompt+= text[:4000]
        prompt+= "\n\n"
        prompt += """

Return your answer in exactly this format:

License: <SPDX identifier or NOASSERTION>

Citation: <filename> — <short quote from the file that supports your answer>

Prefer citations from LICENSE, COPYING, or NOTICE files when available.

If those are not clear, use manifest files like pyproject.toml, package.json, or Cargo.toml.

"""
    return call_llm(prompt)



if __name__ == "__main__":

    sources = get_sources("pallets", "flask")

    result = identify_license_with_citation(sources)

    print(result)