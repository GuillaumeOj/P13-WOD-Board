def to_camel_case(string: str) -> str:
    words = []

    for i, word in enumerate(string.split("_")):
        if i == 0:
            words.append(word)
            continue
        words.append(word.capitalize())

    return "".join(words)
