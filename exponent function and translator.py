def raise_to_power(base_num, pow_num):
    result = 1
    for index in range(pow_num):
        result = result * base_num
    return result
print(raise_to_power(3, 2))

number_grid = [

    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [0]
]
for row in number_grid:
    for col in row:
        print(col)

def translate(phrase):
    translation = ""
    for letter in phrase:
        if letter.lower() in "aeuio":
            if letter.isupper():
                translation = translation + "S"
            else:
                translation = translation + "s"
        else:
            translation = translation +letter
    return translation
print(translate(input("Enter a phrase: ")))
