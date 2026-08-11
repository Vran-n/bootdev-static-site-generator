from blocks import markdown_to_blocks, block_to_block_type

class Trie:
    def __init__(self) -> None:
        self.root: dict[str, Any] = {}
        self.end_symbol = "&"
    
    def add(self, word: str) -> None:
        current = self.root
        for char in word:
            if char not in current:
                current[char] = {}
            current = current[char]

        current[self.end_symbol] = True

    # this one actually works as intended
    def find_header(self, text:str):
        matches = set()
        current = self.root

        for i in range(len(text)):
            char = text[i]
            if char not in current:
                break

            current = current[char]
            if self.end_symbol in current:
                matches.add(text[0 : i + 1])
                break
        return matches

    def get(self):
        return self.root

title_regex = Trie()
title_regex.add("# ")



def extract_title(markdown:str):
    blocks = markdown_to_blocks(markdown)
    title = ""

    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype != blocktype.HEADING: continue

        results = title_regex.find_header(block)
        if len(results) != 0:
            header = sorted(results)[0]
            title = block.lstrip("# ")
            break

    if len(title) == 0:
        raise Exception("Title not found!")

    return title