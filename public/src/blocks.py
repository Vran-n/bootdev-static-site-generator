import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
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

    def find_matches(self, text:str):
        matches = set()
        
        if text[0] not in self.root:
            return set()

        for i in range(len(text)):
            current = self.root
            
            for j in range(i, len(text)):
                char = text[j]
                if char not in current:
                    break

                current = current[char]
                if self.end_symbol in current:
                    matches.add(text[i : j + 1])
        return matches

    def get(self):
        return self.root

header_chars = Trie()
header_chars.add("# ")
header_chars.add("## ")
header_chars.add("### ")
header_chars.add("#### ")
header_chars.add("##### ")
header_chars.add("###### ")

multi_code_chars = Trie()
multi_code_chars.add("```\n")
multi_code_chars.add("```")

quote_chars = Trie()
quote_chars.add(">")

order_chars = Trie()
order_chars.add(". ")

unorder_chars = Trie()
unorder_chars.add("- ")

def markdown_to_blocks(text:str) -> list[str]:
    split_blocks = text.split("\n\n")
    no_excessive_blocks = []
    final_block = []

    for block in split_blocks:
        if len(block) == 0: continue
        no_excessive_blocks.append(block)

    for block in no_excessive_blocks:
        no_extra_newline = block.strip("\n")
        no_extra_whitespace = no_extra_newline.strip(" ")
        final_block.append(no_extra_whitespace)

    return final_block

def block_to_block_type(block:str) -> BlockType:
    header_result = header_chars.find_matches(block)

    multi_code_result = multi_code_chars.find_matches(block)
    last_backtics = block[-3:]
    last_backtics_result = multi_code_chars.find_matches(last_backtics)

    quote_results = []
    order_results = []
    unorder_results = []

    lines = block.split("\n")
    for line in lines:
        first_2 = line[:2]
        # temp fix using regex
        first_2_without_number = "".join(re.findall(r"\d(.*)", line))[:2]

        quote_result = quote_chars.find_matches(first_2)
        unorder_result = unorder_chars.find_matches(first_2)
        # temp fix because i'm a fucking dumbass
        try: order_result = order_chars.find_matches(first_2_without_number)
        except IndexError: order_result = set()

        if len(quote_result) == 0:
            quote_results = None
        if len(unorder_result) == 0:
            unorder_results = None
        if len(order_result) == 0:
            order_results = None

        if quote_results != None:
            quote_results.append(quote_result)

        if unorder_results != None:
            unorder_results.append(unorder_result)

        if order_results != None:
            order_results.append(order_result)

    
    if quote_results == None:
        quote_results = []
    if unorder_results == None:
        unorder_results = []
    if order_results == None:
        order_results = []
    elif order_results != None:
        lines = block.split("\n")
        for i in range(len(lines)):
            digit = re.findall(r"(\d)(?:.*)", lines[i])[0]
            i += 1
            if i != int(digit):
                order_results = []
                break

    match (
        len(header_result) != 0,
        len(multi_code_result) != 0 and len(last_backtics_result) != 0,
        len(quote_results) != 0,
        len(order_results) != 0,
        len(unorder_results) != 0
    ):
        case (True, _, _, _, _):
            return BlockType.HEADING
        case (_, True, _, _, _):
            return BlockType.CODE
        case (_, _, True, _, _):
            return BlockType.QUOTE
        case (_, _, _, True, _):
            return BlockType.ORDERED_LIST
        case (_, _, _, _, True):
            return BlockType.UNORDERED_LIST
        case (False, False, False, False, False):
            return BlockType.PARAGRAPH

        case _:
            raise Exception("what the fuck")