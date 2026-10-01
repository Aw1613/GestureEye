"""
Unit tests for SentenceBuilder (Agent 3 - Contract E)
"""

import pytest
from app.sentence.builder import SentenceBuilder


def test_builder_word_buffer_order():
    """Verify words are maintained in the correct sequential order."""
    builder = SentenceBuilder()
    builder.add_word("hello")
    builder.add_word("thank_you")
    builder.add_word("water")

    assert builder.get_words() == ["hello", "thank_you", "water"]


def test_builder_accepts_contract_d_dict():
    """Verify add_word accepts a Contract D stable sign event dictionary."""
    builder = SentenceBuilder()
    event = {
        "word": "water",
        "confidence": 0.88,
        "start_time": 100.0,
        "end_time": 102.0
    }
    result = builder.add_word(event)
    assert builder.get_words() == ["water"]
    assert result["words"] == ["water"]
    assert "water" in result["text"].lower()


def test_builder_consecutive_duplicate_suppression():
    """Consecutive identical words are not duplicated in the buffer."""
    builder = SentenceBuilder(suppress_consecutive_duplicates=True)
    builder.add_word("hello")
    builder.add_word("hello")
    builder.add_word("water")
    builder.add_word("water")

    assert builder.get_words() == ["hello", "water"]


def test_builder_single_word_expansion():
    """Single sign produces natural standalone phrase."""
    builder = SentenceBuilder()

    builder.add_word("water")
    assert builder.get_sentence() == "I need water, please."

    builder.clear()
    builder.add_word("bathroom")
    assert builder.get_sentence() == "I need the bathroom."

    builder.clear()
    builder.add_word("help")
    assert builder.get_sentence() == "Please help me!"


def test_builder_idiom_sentence_smoothing():
    """Known sign combinations smooth into fluent sentences."""
    builder = SentenceBuilder()

    builder.add_word("hello")
    builder.add_word("thank_you")
    builder.add_word("water")
    result = builder.build_sentence()

    assert result["text"] == "Hello, thank you for the water."
    assert result["words"] == ["hello", "thank_you", "water"]


def test_builder_question_sentence_smoothing():
    """Question sign combinations end with a question mark."""
    builder = SentenceBuilder()

    builder.add_word("where")
    builder.add_word("bathroom")
    assert builder.get_sentence() == "Where is the bathroom?"

    builder.clear()
    builder.add_word("what")
    builder.add_word("name")
    assert builder.get_sentence() == "What is your name?"


def test_builder_remove_last_word():
    """remove_last_word pops the last word and updates the smoothed sentence."""
    builder = SentenceBuilder()
    builder.add_word("hello")
    builder.add_word("water")

    removed = builder.remove_last_word()
    assert removed == "water"
    assert builder.get_words() == ["hello"]
    assert builder.get_sentence() == "Hello."


def test_builder_finalize_sentence():
    """finalize_sentence returns the completed Contract E object and clears the buffer."""
    builder = SentenceBuilder()
    builder.add_word("i_am")
    builder.add_word("fine")

    final = builder.finalize_sentence()
    assert final["text"] == "I am fine."
    assert final["words"] == ["i_am", "fine"]

    # Buffer should now be empty for the next sentence
    assert builder.get_words() == []
    assert builder.get_sentence() == ""
