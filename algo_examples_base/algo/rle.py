def run_length_encode(text):
    if not text:
        return ""
    encoded = ""
    i = 0
    n = len(text)
    while i < n:
        count = 1
        while i + 1 < n and text[i] == text[i + 1]:
            count += 1
            i += 1
        encoded += str(count) + text[i]
        i += 1
    return encoded

if __name__ == "__main__":
    text = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW"
    print("Encoded:", run_length_encode(text))
