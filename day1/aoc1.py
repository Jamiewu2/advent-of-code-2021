def do_the_thing():
    with open("input.txt", "r") as f:

        nums = list(map(int, f.readlines()))

        if len(nums) < 3:
            return 0


        count = 0
        for i in range(len(nums)-3):
            if nums[i] < nums[i+3]:
                count += 1

        return count

        #
        # window_size = 0
        # prev = 0
        # count = 0
        # for line in f:
        #     num = int(line)
        #
        #     if window_size < 3:
        #         prev += num
        #         window_size += 1
        #
        #     elif
        #
        #
        #     if prev and prev < num:
        #         count+=1
        #     prev = num
        #
        # print(count)


if __name__ == "__main__":
    answer = do_the_thing()
    print(answer)