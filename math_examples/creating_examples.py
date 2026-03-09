from random import randint
from collections import Counter

async def generate_examples_and_keyboards(factor, kb_class):
    examples = []
    keyboard_with_answers = []
    counter = Counter()

    while len(examples) < 10:
        num = randint(1, 9)
        ans = factor * num
        for example in examples:
            if example[1] == num:
                counter[num] += 1
        if counter[num] < 2 and not examples: 
            examples.append([factor, num, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))
        elif counter[num] < 2 and examples and examples[-1][1] != num: 
            examples.append([factor, num, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))

    return examples, keyboard_with_answers

async def generate_examples_and_kb_full_table(kb_class):
    examples = []
    keyboard_with_answers = []
    counter = Counter()

    while len(examples) < 10:
        num1, num2 = randint(2, 9), randint(1, 9)
        ans = num1 * num2
        for example in examples:
            if example[0] in [num1, num2] and example[1] in [num1, num2]:
                counter[(num1, num2)] += 1
        if counter[(num1, num2)] < 2 and not examples: 
            examples.append([num1, num2, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))
        elif counter[(num1, num2)] < 2 and examples and (
        (example[0] not in [num1, num2] or example[1] not in [num1, num2])): 
            examples.append([num1, num2, ans])
            keyboard_with_answers.append(kb_class.generate_multiplicate_answers(ans))

    return examples, keyboard_with_answers