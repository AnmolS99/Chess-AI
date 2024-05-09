@staticmethod
def compare_outputs(file1, file2):
    with open(file1, 'r') as f:
        set1 = set(line.strip() for line in f)
    with open(file2, 'r') as f:
        set2 = set(line.strip() for line in f)
    return {file1: set1 - set2, file2: set2 - set1}

print(compare_outputs('./output/my_program_output.txt', './output/stockfish_output.txt'))