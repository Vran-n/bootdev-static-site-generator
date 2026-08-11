import re
from textnode import TextNode, TextType

def in_tuple(x, x_tuple):
    found = False
    for a in x_tuple:
        if x in a:
            found = True
            break
    return found

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

    def use_as_splitter(self, text: str, sep:str) -> list[(bool, str)]:
        split_text = []
        built_text = ""
        Reached_End_Symbol = True

        i = 0
        while i < len(text):
            current = self.root

            char = text[i]
            if (char not in current 
                or char not in sep
            ): 
                built_text += char
                i += 1
                continue

            Reached_End_Symbol = False
            split_text.append((False, built_text))
            built_text = ""

            for j in range(i, len(text)):
                inner_char = text[j]

                if (inner_char not in current
                    or inner_char not in sep
                ): 
                    built_text += inner_char
                    continue

                current = current[inner_char]
                if self.end_symbol in current:
                    split_text.append((True, built_text))
                    Reached_End_Symbol = True
                    built_text = ""
                    i = j
                    break
            i += 1

        if Reached_End_Symbol is False:
            raise Exception("Incorrect Regex!")

        if len(built_text) > 0:
            split_text.append((False, built_text))

        return split_text

    def use_as_multi_splitter(self, text: str, *seps: str) -> list[(bool, str, str)]:
        split_text = []
        built_text = ""
        Reached_End_Symbol = True

        i, seps_i = 0, 0
        while i < len(text):
            current = self.root

            char = text[i]
            if (char not in current 
                or char not in seps[seps_i]
            ): 
                built_text += char
                i += 1
                continue

            Reached_End_Symbol = False
            split_text.append((False, built_text, None))
            built_text = ""
            temp_list = [True]

            for j in range(i, len(text)):
                inner_char = text[j]

                # check if the wrong character is next in the pattern
                if in_tuple(inner_char, seps) and inner_char not in seps[seps_i]:
                    break

                if (inner_char not in current
                    or inner_char not in seps[seps_i]
                ): 
                    built_text += inner_char
                    continue

                if inner_char in current and inner_char not in seps[seps_i]:
                    print(">>", inner_char, seps[seps_i])
                    break

                current = current[inner_char]
                if self.end_symbol in current:
                    temp_list.append(built_text)
                    current = self.root
                    built_text = ""
                    seps_i += 1

                if seps_i >= len(seps): 
                    Reached_End_Symbol = True
                    current = self.root
                    seps_i = 0
                    i = j
                    break
                    

            combined = tuple(temp_list)
            split_text.append(combined)
            i += 1

        if Reached_End_Symbol is False:
            #print("|||", text)
            raise Exception("Incorrect Regex!")

        if len(built_text) > 0:
            split_text.append((False, built_text, None))

        return split_text


    # another temp fix because it erros if "!" is matched with no seps
    def use_as_splitter_for_image(self, text: str) -> list[(bool, str, str)]:
        capture = ["[]", "()"]
        split_text = []
        built_text = ""
        Reached_End_Symbol = True

        i, cap_i = 0, 0
        while i < len(text):
            current = self.root

            char = text[i]
            if char not in current: 
                built_text += char
                i += 1
                continue
            # here if char in current

            if char == "!":
                try: 
                    if text[i+1] == " ": i += 1 ; continue
                except IndexError: break

            split_text.append((False, built_text, None))
            built_text = ""
            temp_list = [True]

            for j in range(i, len(text)):
                inner_char = text[j]

                if inner_char not in current: 
                    built_text += inner_char
                    continue
                
                if inner_char != "!" and Reached_End_Symbol is True:
                    Reached_End_Symbol = False

                if inner_char in capture[cap_i][1] and cap_i <= 1:
                    temp_list.append(built_text)
                    built_text = ""
                    cap_i += 1
                    
                current = current[inner_char]
                if self.end_symbol in current:
                    Reached_End_Symbol = True
                    current = self.root
                    i = j
                    cap_i = 0
                    break

            combined = tuple(temp_list)
            split_text.append(combined)
            i += 1

        if Reached_End_Symbol is False:
            raise Exception("Incorrect Regex!")

        if len(built_text) > 0:
            split_text.append((False, built_text, None))

        return split_text

regex_markdown = Trie()
regex_markdown.add("****")
regex_markdown.add("__")
regex_markdown.add("``")
# 
regex_markdown_image = Trie()
regex_markdown_image.add("![]()")

# shrimple solution to nearly identical regex
regex_markdown_link = Trie()
regex_markdown_link.add("[]")
regex_markdown_link.add("()")


def split_nodes_delimiter(
    old_nodes: list[TextNode], 
    delimiter: str, 
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        result = regex_markdown.use_as_splitter(node.text, delimiter)

        for pair in result:
            is_in_sep = pair[0]
            actual_text = pair[1]

            if is_in_sep == False:
                new_nodes.append(TextNode(actual_text, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(actual_text, text_type))
    return new_nodes

def split_nodes_link(
    old_nodes: list[TextNode], 
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        result = regex_markdown_link.use_as_multi_splitter(node.text, "[]", "()")
        
        for pair in result:
            is_in_sep = pair[0]
            actual_text = pair[1]
            url = pair[2]

            if is_in_sep == False:
                new_nodes.append(TextNode(actual_text, TextType.PLAIN_TEXT, url))
            else:
                new_nodes.append(TextNode(actual_text, TextType.LINK_TEXT, url))
    return new_nodes

def split_nodes_image(
    old_nodes: list[TextNode], 
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        result = regex_markdown_image.use_as_splitter_for_image(node.text)

        for pair in result:
            is_in_sep = pair[0]
            actual_text = pair[1]
            url = pair[2]

            if is_in_sep == False:
                new_nodes.append(TextNode(actual_text, TextType.PLAIN_TEXT, url))
            else:
                new_nodes.append(TextNode(actual_text, TextType.IMAGE, url))
    return new_nodes


def extract_markdown_links(text:str):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_images(text:str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches



def text_to_textnodes(text:str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    bold_result = split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)
    italic_result = split_nodes_delimiter(bold_result, "_", TextType.ITALIC_TEXT)
    code_result = split_nodes_delimiter(italic_result, "`*`", TextType.CODE_TEXT)
    image_result = split_nodes_image(code_result)
    link_result = split_nodes_link(image_result)
    return link_result