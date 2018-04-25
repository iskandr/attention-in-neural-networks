substitutions = {
    "'’‘": " <SINGLE-QUOTE> ",
    '"«»': " <DOUBLE-QUOTE> ",
    "/": " <SLASH> ",
    "\\": " <BACK-SLASH> ",
    "”": " <RIGHT-QUOTE> ",
    "“": " <LEFT-QUOTE> ",
    "-": " <HYPHEN> ",
    "[": " <LEFT-BRACKET> ",
    "]": " <RIGHT-BRACKET> ",
    "?": " <QUESTION> ",
    "!": " <EXCLAMATION> ",
    ",": " <COMMA> ",
    ":": " <COLON> ",
    ";": " <SEMI-COLON> ",
    "+": "<PLUS> ",
    "(": " <LEFT-PAREN> ",
    ")": " <RIGHT-PAREN> ",
    "&": " <AND>",
}

deletions = {"¿", "¡"}


def normalize(s):
    s = s.lower().replace(".", "").replace("\n", "")
    while "--" in s:
        s = s.replace("--", "-")
    for (ks, v) in substitutions.items():
        for k in ks:
            if k in s:
                s = s.replace(k, v)
    for k in deletions:
        if k in s:
            s = s.replace(k, "")
    s = "<SOS> " + s.strip() + " <EOS>"
    while "  " in s:
        s = s.replace("  ", " ")
    return s


def tokenize(s):
    s = normalize(s)
    tokens = []
    for word in s.split(" "):
        if len(word) == 0:
            continue
        elif word.isdigit():
            tokens.append("<NUMBER>")
        else:
            tokens.append(word)
    return tokens


def denormalize_string(s):
    for (ks, v) in substitutions.items():
        if v in s:
            s = s.replace(v, ks[0])
    return s


def detokenize(tokens):
    tokens = [token for token in tokens if token not in ["<EOS>", "<SOS>"]]
    s = " ".join(tokens)
    return denormalize_string(s)
