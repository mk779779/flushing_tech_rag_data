import datasets
from rich import print

dataset = datasets.load_dataset("567-labs/bird-rag")["train"]

print("dataset", dataset[0])
