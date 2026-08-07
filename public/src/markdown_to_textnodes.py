from textnode import TextNode, TextType

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

    # NOTE: WE CANT TELL WHICH SEPARATOR WAS MATCHED
    def use_as_splitter(self, text: str) -> list[(bool, str)]:
        split_text = []
        built_text = ""
        Is_In_Sep = False

        i = 0
        while i < len(text):
            current = self.root
            for j in range(i, len(text)):
                char = text[j]
               
                if char not in current:
                    built_text += text[i]
                    break

                current = current[char]
                if self.end_symbol in current:
                    split_text.append((Is_In_Sep, built_text))
                    Is_In_Sep = not Is_In_Sep
                    built_text = ""
                    i = j + 1

            i += 1
        
        if len(built_text) > 0:
            split_text.append((Is_In_Sep, built_text))

        return split_text


regex_markdown = Trie()
regex_markdown.add("**")
regex_markdown.add("_")
regex_markdown.add("`")



def split_nodes_delimiter(
    old_nodes: list[TextNode], 
    delimiter: str, 
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))

        result = regex_markdown.use_as_splitter(node.text)

        for pair in result:
            is_in_sep = pair[0]
            actual_text = pair[1]

            if is_in_sep == False:
                new_nodes.append(TextNode(pair[1], TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(pair[1], text_type))


    
    return new_nodes