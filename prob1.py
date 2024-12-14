from collections import Counter


def get_input(filename):
    with open(filename, "r") as f:
        list1, list2 = [], []
        for line in f.readlines():
            first, second = line.split("   ")
            list1.append(int(first)), list2.append(int(second))
        return list1, list2


def part1(list1, list2):
    list1 = sorted(list1)
    list2 = sorted(list2)
    return sum(abs(a - b) for a, b in zip(list1, list2))


def part2(list1, list2):
    list2_counter = Counter(list2)
    return sum([num*list2_counter[num] for num in list1])


def main():
    list1, list2 = get_input("test_files/prob1_full_input.txt")
    print(f"Part 1 solution: {part1(list1, list2)}")
    print(f"Part 2 solution: {part2(list1, list2)}")


if __name__ == "__main__":
    main()
