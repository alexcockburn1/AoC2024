from collections import defaultdict


def get_input(filename):
    with open(filename, "r") as f:
        rules = defaultdict(list)
        updates = []
        for line in f.readlines():
            if "|" in line:
                a, b = line.split("|")
                a, b = int(a), int(b)
                rules[a].append(b)
                # rules[b].append(a)
            if "," in line:
                updates.append([int(num) for num in line.split(",")])
    return rules, updates


def validate_update(rules, update):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if update[i] in rules[update[j]]:
                # print(f"{update} failed to satisfy rule {update[j]} < {update[i]}")
                return i, j, False
    # print(f"{update} is valid!")
    return None, None, True


def part1(rules, updates):
    middle_total = 0
    for update in updates:
        _, _, is_valid = validate_update(rules, update)
        if is_valid:
            middle_total += update[len(update)//2]
    return middle_total


def fix_update(rules, update):
    i, j, is_valid = validate_update(rules, update)
    if not is_valid:
        update[i], update[j] = update[j], update[i]
        return fix_update(rules, update)
    return update


def part2(rules, updates):
    middle_total = 0
    for update in updates:
        _, _, is_valid = validate_update(rules, update)
        if not is_valid:
            fix_update(rules, update)
            middle_total += update[len(update) // 2]
    return middle_total


def main():
    rules, updates = get_input("test_files/prob5_full_input.txt")
    # print(rules)
    # print(updates)
    # print(f"Part 1 solution is {part1(rules, updates)}")
    print(f"Part 2 solution is {part2(rules, updates)}")


if __name__ == "__main__":
    main()
