from collections import Counter


def get_input(filename):
    with open(filename, "r") as f:
        return [int(char) for char in f.read().strip().split(" ")]


def update_stone(stone):
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        midpoint = int(len(stone_str)/2)
        return [int(stone_str[:midpoint]), int(stone_str[midpoint:])]
    return [stone*2024]


def part1(stones, blinks):
    for blink in range(blinks):
        print(f"{blink=}")
        updated_stones = []
        for stone in stones:
            updated_stones += update_stone(stone)
        stones = updated_stones
        print(f"Number of stones={len(stones)}")
    return stones


def part2(stones, blinks):
    stone_counter = Counter(stones)
    for blink in range(blinks):
        updated_counter = Counter()
        for stone, count in stone_counter.items():
            for new_stone in update_stone(stone):
                updated_counter[new_stone] += count
        stone_counter = updated_counter
    return sum(stone_counter.values())


def main():
    puzzle_input = get_input("test_files/prob11_full_input.txt")
    print(f"Solution to part1 is {part2(puzzle_input, 75)}")


if __name__ == "__main__":
    main()
