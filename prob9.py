def get_input(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def get_checksum(ordered_block_list):
    return sum([i*int(char) for i, char in enumerate(ordered_block_list) if char != "."])


def expand(puzzle_input):
    result = []
    for i, num in enumerate(puzzle_input):
        if i % 2 == 0:
            result += [int(i/2)]*int(num)
        else:
            result += ["."]*int(num)
    return result


def part1(puzzle_input):
    file_block_list = expand(puzzle_input)
    adding_index = 0
    removing_index = len(file_block_list) - 1
    while adding_index < removing_index:
        if file_block_list[adding_index] != ".":
            adding_index += 1
        else:
            removing_index_val = file_block_list[removing_index]
            if removing_index_val != ".":
                file_block_list[adding_index] = removing_index_val
                file_block_list[removing_index] = "."
            removing_index -= 1
    checksum = get_checksum(file_block_list)
    return checksum


def parse_blocks(puzzle_input):
    block_list = []
    for i, num in enumerate(puzzle_input):
        num = int(num)
        if num > 0:
            if i % 2 == 0:
                block_list.append((int(i/2), num))
            else:
                if len(block_list) > 0 and block_list[len(block_list) - 1][0] == ".":
                    final_block_list_elem = block_list[len(block_list) - 1]
                    block_list[len(block_list) - 1] = (final_block_list_elem[0], final_block_list_elem[1] + num)
                else:
                    block_list.append((".", num))
    return block_list


def get_checksum_block_list(block_list):
    total = 0
    current_index = 0
    for block in block_list:
        identity, size = block
        if identity != ".":
            total += identity*sum(range(current_index, current_index + size))
        current_index = current_index + size
    return total


def stringify_blocklist(block_list):
    expanded_block_list = []
    for block_identity, block_size in block_list:
        expanded_block_list += str(block_identity) * block_size
    return expanded_block_list


def part2(puzzle_input):
    block_list = parse_blocks(puzzle_input)
    print("".join(stringify_blocklist(block_list)))
    moving_index = len(block_list) - 1
    while moving_index > 0:
        # previous_stringified_block_list = "".join(stringify_blocklist(block_list))
        moving_identity, moving_block_size = block_list[moving_index]
        for i in range(0, moving_index):
            candidate_identity, candidate_space = block_list[i]
            if candidate_identity == "." and candidate_space >= moving_block_size:
                block_list[moving_index] = (".", moving_block_size)
                if candidate_space > moving_block_size:
                    block_list = block_list[:i] + [(moving_identity, moving_block_size), (".", candidate_space - moving_block_size)] + block_list[i+1:]
                    moving_index += 1
                else:
                    block_list[i] = (moving_identity, moving_block_size)
                break
        moving_index -= 1
        moving_identity, _ = block_list[moving_index]
        while moving_identity == ".":
            moving_index -= 1
            moving_identity, _ = block_list[moving_index]
        # print("".join(stringify_blocklist(block_list)))
        # if len("".join(stringify_blocklist(block_list))) != len(previous_stringified_block_list):
        #     print("A bad thing happend")

    return get_checksum_block_list(block_list)



def main():
    puzzle_input = get_input("test_files/prob9_full_input.txt")
    # print(f"Solution to part 1 is: {part1(puzzle_input)}")
    # 010101010101010101012
    print(f"Solution to part 2 is: {part2(puzzle_input)}")


if __name__ == "__main__":
    main()
