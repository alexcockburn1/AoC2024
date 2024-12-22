import math
from collections import Counter


def get_input(filename):
    with open(filename, "r") as f:
        return [int(line) for line in f.readlines()]


def mix(secret_number, value):
    return secret_number ^ value


def prune(secret_number):
    return secret_number % 16777216


def evolve(secret):
    secret = prune(mix(secret, secret*64))
    secret = prune(mix(secret, int(math.floor(secret/32))))
    secret = prune(mix(secret, secret*2048))
    return secret


def part1(seeds):
    total = 0
    for seed in seeds:
        secret = seed
        for _ in range(2000):
            secret = evolve(secret)
        total += secret
        # print(seed, secret)
    print(f"Solution to part 1 is {total}")


def get_changes_dict(length, price_list):
    differences = [a - b for a, b in zip(price_list[1:], price_list)]
    differences_counter = Counter()
    for i in range(len(differences) - length + 1):
        key = tuple(differences[i:i + length])
        if key not in differences_counter:
            differences_counter[key] = price_list[i + length]
    return differences_counter


def part2(seeds):
    prices_lists = []
    for seed in seeds:
        prices_list = []
        secret = seed
        for _ in range(2001):
            prices_list.append(secret % 10)
            secret = evolve(secret)
        prices_lists.append(prices_list)
    changes_counters = []
    for prices_list in prices_lists:
        changes_counter = get_changes_dict(4, prices_list)
        changes_counters.append(changes_counter)
    overall_differences_counter = sum(changes_counters, start=Counter())
    max_sales = max(overall_differences_counter.items(), key=lambda kv: kv[1])
    print(f"Solution to part 2 is {max_sales[1]}")


def main():
    secrets = get_input("test_files/prob22_full_input.txt")
    part1(secrets)
    part2(secrets)


if __name__ == "__main__":
    main()
