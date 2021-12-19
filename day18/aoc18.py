from dataclasses import dataclass


@dataclass
class Number:

    def height(self):
        raise NotImplementedError

    def is_regular(self):
        raise NotImplementedError

    # returns true if exploded
    def explode_maybe(self):
        return False

    def explode(self):
        raise NotImplementedError

    def add_num_left(self, num):
        raise NotImplementedError

    def add_num_right(self, num):
        raise NotImplementedError

    # returns true if reduced
    def reduce(self):
        raise NotImplementedError

    def magnitude(self):
        raise NotImplementedError

    # debugging
    def as_str(self):
        raise NotImplementedError


@dataclass
class RegularNumber(Number):
    value: int

    def height(self):
        return 0

    def is_regular(self):
        return True

    def add_num_left(self, num):
        self.value += num

    def add_num_right(self, num):
        self.value += num

    def reduce(self):
        return False

    def magnitude(self):
        return self.value

    def as_str(self):
        return str(self.value)


@dataclass
class SnailfishNumber(Number):
    left: Number
    right: Number

    def height(self):
        return 1 + max(self.left.height(), self.right.height())

    def is_regular(self):
        return False

    def explode_maybe(self):
        if self.height() <= 4:
            return False

        left_height = self.left.height()
        if left_height == 4:
            left_val, right_val = self.left.explode()
            self.right.add_num_left(right_val)
            return True
        else:
            left_val, right_val = self.right.explode()
            self.left.add_num_right(left_val)
            return True

    # [[9,8],1]
    # [[[[[9,8],1],2],3],4]
    # [[[[0,9],2],3],4]
    # returns pair, num to add to left, num to add to right
    def explode(self):
        self_height = self.height()
        left_height = self.left.height()
        right_height = self.right.height()

        if self_height == 2 and left_height == 1:  # [[9,8],1]
            left_val = self.left.left.value
            right_val = self.left.right.value

            self.left = RegularNumber(0)
            self.right.add_num_left(right_val)
            return left_val, 0
        elif self_height == 2:  #[4,[3,2]]
            left_val = self.right.left.value
            right_val = self.right.right.value

            self.right = RegularNumber(0)
            self.left.add_num_right(left_val)
            return 0, right_val

        # recursion steps
        if left_height >= right_height:
            left_val, right_val = self.left.explode()

            if right_val != 0:
                self.right.add_num_left(right_val)
                right_val = 0

            return left_val, right_val

        else:
            left_val, right_val = self.right.explode()

            if left_val != 0:
                self.left.add_num_right(left_val)
                left_val = 0

            return left_val, right_val

    def add_num_left(self, num):
        temp = self.left
        while not temp.is_regular():
            temp = temp.left

        temp.add_num_left(num)

    def add_num_right(self, num):
        temp = self.right
        while not temp.is_regular():
            temp = temp.right

        temp.add_num_right(num)

    def reduce(self):
        if self.left.is_regular():
            val = self.left.value
            if val >= 10:
                self.left = SnailfishNumber(RegularNumber(val//2), RegularNumber((val+1)//2))
                return True

        has_reduced = self.left.reduce()
        if has_reduced:
            return True

        if self.right.is_regular():
            val = self.right.value
            if val >= 10:
                self.right = SnailfishNumber(RegularNumber(val//2), RegularNumber((val+1)//2))
                return True

        return self.right.reduce()

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def as_str(self):
        return f"[{self.left.as_str()},{self.right.as_str()}]"


def add(num1: SnailfishNumber, num2: SnailfishNumber):
    new_num = SnailfishNumber(num1, num2)

    has_exploded = True
    has_reduced = True

    while has_exploded or has_reduced:
        has_exploded = new_num.explode_maybe()
        while has_exploded:
            # print(new_num.as_str())
            has_exploded = new_num.explode_maybe()

        has_reduced = new_num.reduce()

    return new_num


# leetcode vibes here
def parse(str_input):
    stack = []

    for c in str_input:
        # print(c)
        if c == '[':
            pass
        elif c == ',':
            pass
        elif c == ']':
            # print(stack)
            value2 = stack.pop()
            value1 = stack.pop()
            stack.append(SnailfishNumber(value1, value2))
        else:
            stack.append(RegularNumber(int(c)))

    return stack[0]


def do_the_thing():
    with open("input.txt", 'r') as f:
        num1 = None

        for line in f:
            line = line.strip()

            if not num1:
                num1 = parse(line)
            else:
                num2 = parse(line)
                num1 = add(num1, num2)

        return num1


def part2():

    # stack 1: [9,9]
    # stack 2: [[9,9],[9,9]]
    # stack 3: [[[9,9],[9,9]],[[9,9],[9,9]]]
    # stack 4: [[[[9,9],[9,9]],[[9,9],[9,9]]],[[[9,9],[9,9]],[[9,9],[9,9]]]]
    # oh 2 different numbers
    # stack 4: [[[[9,9],[9,9]],[[9,9],[9,9]]],[[[9,9],[9,9]],[[9,9],[9,8]]]]

    # oh whoops its from the input....
    with open("input.txt", 'r') as f:
        inputs = list(map(lambda x: x.strip(), f.readlines()))

        # mutability sucks
        combos = [add(parse(inputs[a]), parse(inputs[b])).magnitude()
                  for a in range(len(inputs)) for b in range(len(inputs)) if a != b]

        ans = max(combos)
        print(ans)


if __name__ == "__main__":
    number = do_the_thing()
    print(number.as_str())
    print(number.magnitude())
    part2()

    # str_input1 = "[7,[6,[5,[4,[3,2]]]]]"
    # str_input2 = "[[[[[9,8],5],2],3],4]"
    # str_input1 = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"
    # str_input2 = "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"
    # str_input2 = "[1,1]"
    # str_input = "[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"
    # str_input = "[13,0]"
    # num1 = parse(str_input1)
    # num2 = parse(str_input2)
    # number = add(num1, num2)
    # print(number.as_str())

    # print(num1.magnitude())
    # number.explode_maybe()
    # print(number.as_str())
    # number.reduce()
    # print(number)
