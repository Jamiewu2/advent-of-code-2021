def convert(bool_val):
    if bool_val:
        return '1'
    else:
        return '0'


def do_the_thing():
    with open("input.txt", "r") as f:

        nums = list(f.readlines())

        gamma_vals = ""
        epsilon_vals = ""

        for i in range(len(nums[0])):
            if nums[0][i] == '\n':
                continue

            gamma_val = convert(sum(map(lambda x: int(x[i]), nums)) > len(nums)/2)
            gamma_vals += gamma_val
            epsilon_val = convert(sum(map(lambda x: int(x[i]), nums)) < len(nums)/2)
            epsilon_vals += epsilon_val

        g_val = int(gamma_vals, 2)
        e_val = int(epsilon_vals, 2)

        return g_val, e_val


def find_most_common_in_pos(nums, pos):
    gamma_val = convert(sum(map(lambda x: int(x[pos]), nums)) >= len(nums)/2)
    nums = list(filter(lambda x: x[pos] == gamma_val, nums))
    return nums


def find_least_common_in_pos(nums, pos):
    gamma_val = convert(sum(map(lambda x: int(x[pos]), nums)) < len(nums)/2)
    nums = list(filter(lambda x: x[pos] == gamma_val, nums))
    return nums


def do_the_thing_2():
    with open("input.txt", "r") as f:

        nums = list(map(lambda x: x.strip(), f.readlines()))

        tmp_ans = nums

        for i in range(len(nums[0])):
            if len(tmp_ans) == 1:
                break
            tmp_ans = find_most_common_in_pos(tmp_ans, i)

        oxygen_val = int(tmp_ans[0], 2)

        tmp_ans = nums

        for i in range(len(nums[0])):
            if len(tmp_ans) == 1:
                break
            tmp_ans = find_least_common_in_pos(tmp_ans, i)

        co2_val = int(tmp_ans[0], 2)

        return oxygen_val, co2_val


if __name__ == "__main__":
    a, b = do_the_thing_2()
    print(a*b)
