import json

from naming import output_name
from reader import parse_csv
from summarize import summarize


def run(inputs):
    outputs = {}
    index = {}
    for filename in sorted(inputs):
        if not filename.endswith(".csv"):
            continue
        name = output_name(filename)
        if name in outputs:
            raise ValueError(f"two inputs would both write {name}")
        outputs[name] = json.dumps(summarize(*parse_csv(inputs[filename])), sort_keys=True)
        index[filename] = name
    outputs["index.json"] = json.dumps(index, sort_keys=True)
    return outputs
