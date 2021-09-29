import json

# Load data
with open("./data/10884668-results.json", "r") as f:
    results_09182020 = json.load(f)
f.close()

with open("./data/13316507-results.json", "r") as f:
    results_09282021 = json.load(f)
f.close()

if __name__ == "__main__":
    # make magic
    pass