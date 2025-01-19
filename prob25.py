def get_col(matrix, col):
    return [row[col] for row in matrix]


def get_char_count(i, matrix, target_char):
    return len([char for char in get_col(matrix, i) if char == target_char]) - 1


def map_to_counts(matrix):
    return [get_char_count(i, matrix, "#") for i in range(5)]


def get_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        keys, locks = [], []
        for i in range(0, len(lines)//8 + 1):
            key_or_lock = lines[i*8: i*8 + 7]
            if all([char == "#" for char in key_or_lock[0]]):
                locks.append(map_to_counts(key_or_lock))
            else:
                keys.append(map_to_counts(key_or_lock))
    return keys, locks


def does_key_fit_lock(lock, key):
    return all([l + k <= 5 for l, k in zip(lock, key)])


def part1(keys, locks):
    lock_key_fits = 0
    for lock in locks:
        for key in keys:
            if does_key_fit_lock(key, lock):
                lock_key_fits += 1
    print(f"Solution to part 1 is {lock_key_fits}")


def main():
    keys, locks = get_input("test_files/prob25_full_input.txt")
    part1(keys, locks)


if __name__ == "__main__":
    main()
