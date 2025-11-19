from typing import Optional, List, Dict, Any


class NaviLanguageError(Exception):
    """
    Base class for custom errors related to Na'vi language, child class of Exeption
    """

    def __init__(
        self, message: str, word: Optional[str] = None, position: Optional[int] = None
    ):
        self.message = message
        self.word = word
        self.position = position
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        parts = [self.message]
        if self.word:
            parts.append(f"Word: '{self.word}'")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)

    def __str__(self) -> str:
        return self._format_message()


class NaviTokenizerError(NaviLanguageError):

    def __init__(
        self,
        message: str,
        text: Optional[str] = None,
        word: Optional[str] = None,
        position: Optional[int] = None,
    ):
        self.text = text
        super().__init__(message, word, position)

    def _format_message(self) -> str:
        parts = [self.message]
        if self.text:
            parts.append(f"Text: '{self.text}'")
        if self.word:
            parts.append(f"Word: '{self.word}'")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)


class InvalidInputError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        text: Optional[str] = None,
        input_type: Optional[type] = None,
    ):
        self.input_type = input_type
        super().__init__(message, text)

    def _format_message(self) -> str:
        parts = [f"Invalid input: {self.message}"]
        if self.text is not None:
            parts.append(f"Got: '{self.text}'")
        if self.input_type:
            parts.append(f"Type: {self.input_type.__name__}")
        return " | ".join(parts)


class InvalidNaviTextError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        text: Optional[str] = None,
        word: Optional[str] = None,
        invalid_chars: Optional[List[str]] = None,
    ):
        self.invalid_chars = invalid_chars or []
        super().__init__(message, text, word)

    def _format_message(self) -> str:
        parts = [f"Invalid Na'vi text: {self.message}"]
        if self.word:
            parts.append(f"Word: '{self.word}'")
        if self.invalid_chars:
            parts.append(f"Invalid characters: {self.invalid_chars}")
        return " | ".join(parts)


class TokenizationError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        text: Optional[str] = None,
        word: Optional[str] = None,
        position: Optional[int] = None,
        token_type: Optional[str] = None,
    ):
        self.token_type = token_type
        super().__init__(message, text, word, position)

    def _format_message(self) -> str:
        parts = [f"Tokenization failed: {self.message}"]
        if self.word:
            parts.append(f"At word: '{self.word}'")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        if self.token_type:
            parts.append(f"Token type: {self.token_type}")
        return " | ".join(parts)


class CaseConflictError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        word: str,
        found_cases: List[str],
        position: Optional[int] = None,
    ):
        self.found_cases = found_cases
        super().__init__(message, word=word, position=position)

    def _format_message(self) -> str:
        parts = [f"Case conflict: {self.message}"]
        parts.append(f"Word: '{self.word}'")
        parts.append(f"Found cases: {', '.join(self.found_cases)}")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)


class InfixError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        verb: str,
        infixes: Optional[List[str]] = None,
        position: Optional[int] = None,
    ):
        self.verb = verb
        self.infixes = infixes or []
        super().__init__(message, word=verb, position=position)

    def _format_message(self) -> str:
        parts = [f"Infix error: {self.message}"]
        parts.append(f"Verb: '{self.verb}'")
        if self.infixes:
            parts.append(f"Infixes: {self.infixes}")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)


class WordClassificationError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        word: str,
        possible_types: List[str],
        position: Optional[int] = None,
    ):
        self.possible_types = possible_types
        super().__init__(message, word=word, position=position)

    def _format_message(self) -> str:
        parts = [f"Classification error: {self.message}"]
        parts.append(f"Word: '{self.word}'")
        parts.append(f"Possible types: {', '.join(self.possible_types)}")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)


class GrammarValidationError(NaviTokenizerError):

    def __init__(
        self,
        message: str,
        rule_violated: str,
        context: Optional[Dict[str, Any]] = None,
        position: Optional[int] = None,
    ):
        self.rule_violated = rule_violated
        self.context = context or {}
        super().__init__(message, position=position)

    def _format_message(self) -> str:
        parts = [f"Grammar violation: {self.message}"]
        parts.append(f"Rule: {self.rule_violated}")
        if self.context:
            context_str = ", ".join(f"{k}: {v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")
        if self.position is not None:
            parts.append(f"Position: {self.position}")
        return " | ".join(parts)


class MorphologicalAnalysisError(NaviLanguageError):

    def __init__(
        self,
        message: str,
        word: str,
        analysis_type: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.analysis_type = analysis_type
        self.details = details or {}
        super().__init__(message, word)

    def _format_message(self) -> str:
        parts = [f"Morphological analysis failed: {self.message}"]
        parts.append(f"Word: '{self.word}'")
        parts.append(f"Analysis type: {self.analysis_type}")
        if self.details:
            details_str = ", ".join(f"{k}: {v}" for k, v in self.details.items())
            parts.append(f"Details: {details_str}")
        return " | ".join(parts)


class SyntaxAnalysisError(NaviLanguageError):

    def __init__(
        self,
        message: str,
        sentence: str,
        expected_pattern: Optional[str] = None,
        found_pattern: Optional[str] = None,
    ):
        self.sentence = sentence
        self.expected_pattern = expected_pattern
        self.found_pattern = found_pattern
        super().__init__(message)

    def _format_message(self) -> str:
        parts = [f"Syntax analysis failed: {self.message}"]
        parts.append(f"Sentence: '{self.sentence}'")
        if self.expected_pattern:
            parts.append(f"Expected: {self.expected_pattern}")
        if self.found_pattern:
            parts.append(f"Found: {self.found_pattern}")
        return " | ".join(parts)
