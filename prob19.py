import functools


def get_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        patterns = [pattern.strip() for pattern in lines[0].split(", ")]
        designs = [line.strip() for line in lines[2:]]
    return patterns, designs


@functools.cache
def is_possible(design):
    # print(f"{design=}")
    if design == "":
        return True
    for pattern in patterns:
        if design[:len(pattern)] == pattern:
            if is_possible(design[len(pattern):]):
                return True
    return False


@functools.cache
def count_ways(design):
    if design == "":
        return 1
    count = 0
    for pattern in patterns:
        if design[:len(pattern)] == pattern:
            pattern_count = count_ways(design[len(pattern):])
            count += pattern_count
    return count


def part1():
    total = 0
    for i, design in enumerate(designs):
        # print(i)
        if is_possible(design):
            total += 1
    return total


def part2():
    total = 0
    for i, design in enumerate(designs):
        # print(i)
        total += count_ways(design)
    return total


def main():
    count_possible_patterns = part1()
    print(f"Solution to part 1 is {count_possible_patterns}")
    ways_count = part2()
    print(f"Solution to part 2 is {ways_count}")
    # is_possible(designs[4])


if __name__ == "__main__":
    patterns, designs = get_input("test_files/prob19_full_input.txt")
    main()
