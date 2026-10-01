"""
Sentence Builder & Smoothing Module (Agent 3 - Milestone M3)
Maintains the accepted word buffer and converts recognized sign sequences
into human-readable sentences following Contract E.
"""

from typing import List, Dict, Any, Union, Optional


class SentenceBuilder:
    """
    Maintains an ordered buffer of accepted words and provides
    heuristic sentence smoothing conforming to Contract E:
    {
        "words": ["hello", "thank_you", "water"],
        "text": "Hello, thank you for the water."
    }
    """

    # Idiomatic phrase mapping for common sign combinations
    IDIOM_RULES = {
        ("hello", "thank_you", "water"): "Hello, thank you for the water.",
        ("hello", "thank_you", "food"): "Hello, thank you for the food.",
        ("hello", "thank_you", "help"): "Hello, thank you for the help.",
        ("hello", "how"): "Hello, how are you?",
        ("hello", "how", "fine"): "Hello, how are you? I am fine.",
        ("hello", "name"): "Hello, what is your name?",
        ("thank_you", "water"): "Thank you for the water.",
        ("thank_you", "food"): "Thank you for the food.",
        ("thank_you", "help"): "Thank you for the help.",
        ("please", "help"): "Please help me.",
        ("please", "water"): "Please, may I have water?",
        ("please", "food"): "Please, may I have food?",
        ("where", "bathroom"): "Where is the bathroom?",
        ("where", "water"): "Where is the water?",
        ("where", "food"): "Where is the food?",
        ("what", "name"): "What is your name?",
        ("who", "name"): "Who are you?",
        ("how", "fine"): "How are you? I am fine.",
        ("i_am", "fine"): "I am fine.",
        ("i_am", "good"): "I am good.",
        ("i_am", "bad"): "I am not feeling well.",
        ("i_am", "sorry"): "I am sorry.",
        ("i_am", "name"): "My name is here.",
        ("water", "please"): "Water, please.",
        ("food", "please"): "Food, please.",
        ("help", "please"): "Help, please!",
        ("bathroom", "where"): "Where is the bathroom?",
    }

    # Single-sign contextual phrases
    SINGLE_WORD_EXPANSIONS = {
        "hello": "Hello.",
        "thank_you": "Thank you.",
        "yes": "Yes.",
        "no": "No.",
        "please": "Please.",
        "sorry": "I am sorry.",
        "help": "Please help me!",
        "water": "I need water, please.",
        "food": "I need food, please.",
        "bathroom": "I need the bathroom.",
        "good": "Good.",
        "bad": "Bad.",
        "fine": "I am fine.",
        "name": "What is your name?",
        "what": "What?",
        "where": "Where?",
        "when": "When?",
        "who": "Who?",
        "how": "How are you?",
        "i_am": "I am here.",
    }

    QUESTION_WORDS = {"what", "where", "when", "who", "how"}
    GREETINGS = {"hello", "please", "sorry"}

    def __init__(self, suppress_consecutive_duplicates: bool = True):
        """
        Args:
            suppress_consecutive_duplicates: If True, ignores immediate consecutive
                                             duplicate words added to the buffer.
        """
        self.suppress_consecutive_duplicates = suppress_consecutive_duplicates
        self.words: List[str] = []

    def add_word(self, word_item: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add an accepted sign to the word buffer. Accepts either a string label
        or a Contract D stable sign event dict {"word": "...", "confidence": ...}.

        Returns:
            Contract E sentence object:
            {
                "words": [...],
                "text": "..."
            }
        """
        if isinstance(word_item, dict):
            word = word_item.get("word")
        elif isinstance(word_item, str):
            word = word_item
        else:
            return self.build_sentence()

        if not word or not isinstance(word, str):
            return self.build_sentence()

        clean_word = word.strip().lower()

        # Duplicate suppression check
        if self.suppress_consecutive_duplicates and self.words:
            if self.words[-1] == clean_word:
                return self.build_sentence()

        self.words.append(clean_word)
        return self.build_sentence()

    def remove_last_word(self) -> Optional[str]:
        """Remove the most recently added word from the buffer (backspace)."""
        if self.words:
            return self.words.pop()
        return None

    def clear(self):
        """Clear all words in the buffer."""
        self.words.clear()

    def reset(self):
        """Alias for clear."""
        self.clear()

    def get_words(self) -> List[str]:
        """Return a copy of the ordered word buffer."""
        return list(self.words)

    def smooth_sentence(self, words: Optional[List[str]] = None) -> str:
        """
        Transform a list of raw sign labels into a grammatically smoothed English sentence.
        """
        token_list = self.words if words is None else words
        if not token_list:
            return ""

        words_tuple = tuple(token_list)

        # 1. Exact phrase lookup
        if words_tuple in self.IDIOM_RULES:
            return self.IDIOM_RULES[words_tuple]

        # 2. Single-word expansion
        if len(token_list) == 1 and token_list[0] in self.SINGLE_WORD_EXPANSIONS:
            return self.SINGLE_WORD_EXPANSIONS[token_list[0]]

        # 3. Heuristic multi-word assembly
        cleaned_tokens: List[str] = []
        is_question = False

        for i, token in enumerate(token_list):
            if token in self.QUESTION_WORDS:
                is_question = True

            if token == "i_am":
                cleaned_tokens.append("I am")
            elif token == "thank_you":
                cleaned_tokens.append("thank you")
            else:
                cleaned_tokens.append(token.replace("_", " "))

        # Build sentence with appropriate formatting
        if not cleaned_tokens:
            return ""

        # Handle greetings at start (e.g., "Hello, ...")
        first_token = token_list[0]
        if first_token in self.GREETINGS and len(cleaned_tokens) > 1:
            lead = cleaned_tokens[0].capitalize()
            rest = " ".join(cleaned_tokens[1:])
            # If rest contains "thank you", format naturally
            if rest.startswith("thank you"):
                sentence = f"{lead}, {rest}"
            else:
                sentence = f"{lead}, {rest}"
        else:
            sentence = " ".join(cleaned_tokens)
            # Capitalize first letter
            sentence = sentence[0].upper() + sentence[1:]

        # Capitalize standalone "i"
        words_split = sentence.split(" ")
        formatted_words = []
        for w in words_split:
            if w == "i":
                formatted_words.append("I")
            elif w.lower() == "i_am":
                formatted_words.append("I am")
            else:
                formatted_words.append(w)
        sentence = " ".join(formatted_words)

        # Append final punctuation if missing
        if not sentence.endswith((".", "?", "!")):
            if is_question:
                sentence += "?"
            else:
                sentence += "."

        return sentence

    def get_sentence(self) -> str:
        """Get the current smoothed sentence string."""
        return self.smooth_sentence()

    def build_sentence(self) -> Dict[str, Any]:
        """
        Construct Contract E object:
        {
            "words": ["hello", "thank_you", "water"],
            "text": "Hello, thank you for the water."
        }
        """
        return {
            "words": list(self.words),
            "text": self.get_sentence()
        }

    def finalize_sentence(self) -> Dict[str, Any]:
        """
        Finalize and return the current sentence, then clear the buffer
        for the next utterance.
        """
        result = self.build_sentence()
        self.clear()
        return result
