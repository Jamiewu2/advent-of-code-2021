def do_the_thing():
    depth = 0
    pos = 0

    with open("input.txt", "r") as f:
        for line in f:
            a, b = line.split(' ')
            if a == "down":
                depth += int(b)
            elif a == "up":
                depth -= int(b)
            elif a == "forward":
                pos += int(b)

    return depth, pos


def do_the_thing_2():
    depth = 0
    pos = 0
    aim = 0

    with open("input.txt", "r") as f:
        for line in f:
            a, b = line.split(' ')
            if a == "down":
                aim += int(b)
            elif a == "up":
                aim -= int(b)
            elif a == "forward":
                pos += int(b)
                depth += aim * int(b)

    return depth, pos

if __name__ == "__main__":
    depth, pos = do_the_thing_2()
    print(depth * pos)