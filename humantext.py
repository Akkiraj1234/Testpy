from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Sequence
import contextlib
import json
import random
import re


SPELLING_RATE = 0.18
GRAMMAR_RATE = 0.16
FILLER_RATE = 0.10
REPEAT_RATE = 0.03

HOST = "127.0.0.1"
PORT = 8000
CANDIDATE_COUNT = 5

VOCABULARY_TERMS = [
    "program",
    "computer",
    "system",
    "data",
    "input",
    "output",
    "memory",
    "cache",
    "language",
    "function",
    "value",
    "variable",
    "result",
    "example",
    "feature",
    "problem",
    "people",
    "person",
    "student",
    "teacher",
    "report",
    "email",
    "message",
    "service",
    "server",
    "client",
    "document",
    "content",
    "version",
    "working",
    "application",
    "project",
    "design",
    "library",
    "environment",
    "different",
    "important",
    "because",
    "necessary",
    "analysis",
    "performance",
    "support",
    "writing",
    "sentence",
    "response",
]

SPELLING_GROUPS = {
    "the": ["teh"],
    "because": ["becuse"],
    "language": ["langauge"],
    "computer": ["compueter"],
    "weird": ["wierd"],
    "receive": ["recieve"],
    "program": ["pgram", "progarm"],
    "function": ["funtion"],
    "important": ["impraont"],
    "value": ["vlaue"],
    "people": ["pepole"],
    "actually": ["actully"],
    "usually": ["usualy"],
    "library": ["libary"],
    "formatted": ["formated"],
    "initial": ["intial"],
    "environment": ["enviorment", "enviroment"],
    "different": ["diffrent"],
    "difference": ["differnce"],
    "separate": ["seperate"],
    "necessary": ["neccessary"],
    "address": ["adress"],
    "believe": ["beleive"],
    "would": ["woud"],
    "should": ["shold"],
    "performance": ["performence"],
    "response": ["responce"],
    "service": ["serivce"],
    "you": ["u"],
}

FILLER_PHRASES = [
    "actually",
    "basically",
    "you know",
    "kind of",
    "only",
]

REPEATING_PHRASES = [
    "very very",
    "really really",
    "the the",
]

GRAMMAR_PATTERNS = [
    ("works", "work"),
    ("provides", "provide"),
    ("returns", "return"),
    ("many people", "many peoples"),
    ("people use", "people are use"),
]

HINDI_GRAMMAR_PATTERNS = [
    ("people are using", "people is using"),
    ("it is working", "it working"),
    ("this function returns", "this funtion return"),
    ("this program works", "this pgram work"),
]

RAW_VOCABULARY = """
[terms]
{terms}

[spelling]
{spelling}

[fillers]
{fillers}

[repeat]
{repeat}

[grammar]
{grammar}

[hindi]
{hindi}
""".format(
    terms="\n".join(VOCABULARY_TERMS),
    spelling="\n".join(
        f"{wrong} -> {correct}"
        for correct, wrongs in SPELLING_GROUPS.items()
        for wrong in wrongs
    ),
    fillers="\n".join(FILLER_PHRASES),
    repeat="\n".join(REPEATING_PHRASES),
    grammar="\n".join(f"{left} => {right}" for left, right in GRAMMAR_PATTERNS),
    hindi="\n".join(f"{left} => {right}" for left, right in HINDI_GRAMMAR_PATTERNS),
)

TOKEN_RE = re.compile(r"\w+|[^\w\s]|\s+")
WORD_RE = re.compile(r"^[A-Za-z]+(?:[-'][A-Za-z]+)*$")
NUMBER_RE = re.compile(r"^\d+(?:[.,:/-]\d+)*$")
URL_RE = re.compile(r"^(https?://|www\.)", re.IGNORECASE)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PATH_RE = re.compile(r"^([A-Za-z]:\\|/|\.{1,2}/|~/)")
CODE_CHARS_RE = re.compile(r"[`{}[\]();<>=$]")
CAMEL_RE = re.compile(r"[a-z][A-Z]|[A-Z][a-z].*[A-Z]")
SENTENCE_SPLIT_RE = re.compile(r"([.!?]+(?:\s+|$))")
DOUBLE_WORD_RE = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)

PROTECTED_WORDS = {
    "api",
    "http",
    "https",
    "json",
    "html",
    "css",
    "javascript",
    "python",
    "linux",
    "windows",
}

VOWELS = "aeiou"
KEYBOARD_NEIGHBORS = {
    "a": "sqwz",
    "b": "vghn",
    "c": "xdfv",
    "d": "serfcx",
    "e": "wsdr",
    "f": "drtgvc",
    "g": "ftyhbv",
    "h": "gyujnb",
    "i": "ujko",
    "k": "ijlo",
    "l": "kop",
    "m": "njk",
    "n": "bhjm",
    "o": "iklp",
    "p": "ol",
    "r": "edft",
    "s": "awedxz",
    "t": "rfgy",
    "u": "yhji",
    "v": "cfgb",
    "w": "qase",
    "x": "zsdc",
    "y": "tghu",
    "z": "asx",
}

WRITER_PROFILES: dict[str, dict[str, Any]] = {
    "indian_esl": {
        "spelling_scale": 0.90,
        "grammar_scale": 1.10,
        "filler_scale": 1.00,
        "repeat_scale": 0.70,
        "fillers": ["actually", "kind of", "only"],
        "grammar_bias": "hindi",
    },
    "fast_typer": {
        "spelling_scale": 1.15,
        "grammar_scale": 0.45,
        "filler_scale": 0.30,
        "repeat_scale": 0.35,
        "fillers": ["basically"],
        "grammar_bias": "light",
    },
    "student": {
        "spelling_scale": 0.85,
        "grammar_scale": 0.85,
        "filler_scale": 0.75,
        "repeat_scale": 0.40,
        "fillers": ["actually", "basically"],
        "grammar_bias": "mixed",
    },
    "casual_chat": {
        "spelling_scale": 0.70,
        "grammar_scale": 0.55,
        "filler_scale": 1.10,
        "repeat_scale": 0.55,
        "fillers": ["you know", "kind of", "basically"],
        "grammar_bias": "light",
    },
}


@dataclass
class MutationBudget:
    spelling: int
    grammar: int
    fillers: int
    repeat: int
    sentence_pressure: float = 1.0


@dataclass
class MutationStats:
    persona: str
    spelling_errors: int = 0
    grammar_errors: int = 0
    filler_count: int = 0
    repeat_count: int = 0
    changed_words: int = 0
    known_typos: int = 0
    keyboard_typos: int = 0
    helper_removals: int = 0
    text: str = ""
    quality_score: int = 0
    humanity_score: int = 0
    damage_score: int = 0
    debug_notes: list[str] = field(default_factory=list)


def log(message: str) -> None:
    stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[humantext {stamp}] {message}", flush=True)


def loadVocabulary() -> str:
    return RAW_VOCABULARY


def parseVocabularyFile(raw_text: str) -> dict[str, object]:
    section = "terms"
    parsed: dict[str, object] = {
        "terms": [],
        "misspellings": {},
        "fillers": [],
        "repeaters": [],
        "grammar_patterns": [],
        "hindi_patterns": [],
    }

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue

        if section == "spelling" and "->" in line:
            wrong, correct = (part.strip().lower() for part in line.split("->", 1))
            misspellings = parsed["misspellings"]
            assert isinstance(misspellings, dict)
            misspellings.setdefault(correct, [])
            if wrong not in misspellings[correct]:
                misspellings[correct].append(wrong)
            continue

        if section in {"grammar", "hindi"} and "=>" in line:
            left, right = (part.strip() for part in line.split("=>", 1))
            key = "grammar_patterns" if section == "grammar" else "hindi_patterns"
            patterns = parsed[key]
            assert isinstance(patterns, list)
            patterns.append((left, right))
            continue

        if section == "fillers":
            fillers = parsed["fillers"]
            assert isinstance(fillers, list)
            fillers.append(line.lower())
            continue

        if section == "repeat":
            repeaters = parsed["repeaters"]
            assert isinstance(repeaters, list)
            repeaters.append(line.lower())
            continue

        terms = parsed["terms"]
        assert isinstance(terms, list)
        terms.append(line.lower())

    return parsed


VOCABULARY = parseVocabularyFile(loadVocabulary())
MISSPELLINGS: Dict[str, List[str]] = VOCABULARY["misspellings"]  # type: ignore[assignment]
FILLERS: List[str] = VOCABULARY["fillers"]  # type: ignore[assignment]
REPEATERS: List[str] = VOCABULARY["repeaters"]  # type: ignore[assignment]
GRAMMAR_RULES: List[tuple[str, str]] = VOCABULARY["grammar_patterns"]  # type: ignore[assignment]
HINDI_RULES: List[tuple[str, str]] = VOCABULARY["hindi_patterns"]  # type: ignore[assignment]

COMPILED_GRAMMAR_RULES = [
    (re.compile(rf"\b{re.escape(left)}\b", re.IGNORECASE), right)
    for left, right in GRAMMAR_RULES
]
COMPILED_HINDI_RULES = [
    (re.compile(rf"\b{re.escape(left)}\b", re.IGNORECASE), right)
    for left, right in HINDI_RULES
]
LONG_SENTENCE_GRAMMAR_FALLBACKS = [
    (re.compile(r"\bi have ([a-z]+ed)\b", re.IGNORECASE), r"i \1"),
    (re.compile(r"\bwe will go\b", re.IGNORECASE), "we will going"),
    (re.compile(r"\bit will work\b", re.IGNORECASE), "it will working"),
    (re.compile(r"\bthey are going\b", re.IGNORECASE), "they is going"),
]
KNOWN_WRONG_FORMS = {
    wrong
    for wrongs in MISSPELLINGS.values()
    for wrong in wrongs
}


def _tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text)


def _join_tokens(tokens: Sequence[str]) -> str:
    return "".join(tokens)


def _compress_spaces(text: str) -> str:
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([,.;!?])", r"\1", text)
    return text.strip()


def _is_word(token: str) -> bool:
    return bool(WORD_RE.match(token))


def _match_case(source: str, target: str) -> str:
    if source.isupper():
        return target.upper()
    if source.istitle():
        return target.title()
    return target


def _looks_protected(token: str) -> bool:
    lower = token.lower()
    if not token:
        return True
    if NUMBER_RE.match(token):
        return True
    if URL_RE.match(token) or EMAIL_RE.match(token) or PATH_RE.match(token):
        return True
    if CODE_CHARS_RE.search(token):
        return True
    if "_" in token or "." in token or "/" in token or "\\" in token:
        return True
    if CAMEL_RE.search(token):
        return True
    if token[0].isupper() and lower not in {"i"}:
        return True
    return lower in PROTECTED_WORDS


def _word_indexes(tokens: Sequence[str]) -> List[int]:
    return [index for index, token in enumerate(tokens) if _is_word(token)]


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[A-Za-z]+\b", text))


def _sentence_word_lengths(text: str) -> list[int]:
    lengths: list[int] = []
    for chunk in re.split(r"[.!?]+", text):
        words = re.findall(r"\b[A-Za-z]+\b", chunk)
        if words:
            lengths.append(len(words))
    return lengths or [_word_count(text)]


def _mutation_budget(text: str, profile: dict[str, Any]) -> MutationBudget:
    words = max(1, _word_count(text))
    sentence_lengths = _sentence_word_lengths(text)
    longest_sentence = max(sentence_lengths)
    average_sentence = sum(sentence_lengths) / len(sentence_lengths)
    sentence_pressure = 1.0
    if longest_sentence >= 10:
        sentence_pressure += 0.20
    if longest_sentence >= 16:
        sentence_pressure += 0.20
    if average_sentence >= 12:
        sentence_pressure += 0.10

    spelling = max(1, min(4, round(words * 0.04 * profile["spelling_scale"])))
    grammar = min(2, round(words * 0.02 * profile["grammar_scale"]))
    if words >= 12 and grammar == 0 and profile["grammar_scale"] >= 0.70:
        grammar = 1
    if longest_sentence >= 12:
        grammar = max(grammar, 1)
    if longest_sentence >= 22:
        grammar = max(grammar, 2)
    fillers = min(1, round(words * 0.01 * profile["filler_scale"]))
    if words >= 30 and fillers == 0 and profile["filler_scale"] >= 0.70:
        fillers = 1
    repeat = 1 if words >= 18 and profile["repeat_scale"] >= 0.35 else 0

    if longest_sentence <= 5:
        grammar = 0
        fillers = 0
        repeat = 0
    if words <= 4:
        spelling = 0
        if re.search(r"\byou\b", text, flags=re.IGNORECASE):
            spelling = 1

    return MutationBudget(
        spelling=spelling,
        grammar=max(0, grammar),
        fillers=max(0, fillers),
        repeat=repeat,
        sentence_pressure=sentence_pressure,
    )


def _weighted_typo_probability(word: str, profile: dict[str, Any], budget: MutationBudget) -> float:
    weight = SPELLING_RATE * profile["spelling_scale"] * budget.sentence_pressure
    if word in VOCABULARY_TERMS:
        weight += 0.08
    if len(word) >= 8:
        weight += 0.04
    if len(word) >= 10:
        weight += 0.06
    if len(word) <= 4:
        weight -= 0.05
    return max(0.06, min(0.45, weight))


def keyboardSpellingMistake(word: str, rng: random.Random) -> str:
    if len(word) < 7:
        return word

    preferred_positions = []
    for pos in (1, 2, len(word) - 3, len(word) - 2):
        if 0 < pos < len(word) - 1:
            preferred_positions.append(pos)

    if not preferred_positions:
        return word

    position = rng.choice(preferred_positions)
    neighbor_pool = KEYBOARD_NEIGHBORS.get(word[position], "")
    if not neighbor_pool:
        return word

    chars = list(word)
    chars[position] = rng.choice(neighbor_pool)
    return "".join(chars)


def _human_typo(word: str, rng: random.Random) -> tuple[str, bool]:
    if len(word) < 4:
        return word, False

    if word in MISSPELLINGS:
        return rng.choice(MISSPELLINGS[word]), False

    if "ie" in word and rng.random() < 0.35:
        return word.replace("ie", "ei", 1), False
    if "ei" in word and rng.random() < 0.35:
        return word.replace("ei", "ie", 1), False

    if len(word) >= 8 and rng.random() < 0.55:
        keyboard_typo = keyboardSpellingMistake(word, rng)
        if keyboard_typo != word:
            return keyboard_typo, True

    repeated_index = next((i for i in range(1, len(word)) if word[i] == word[i - 1]), None)
    if repeated_index is not None and rng.random() < 0.30:
        return word[:repeated_index] + word[repeated_index + 1 :], False

    vowel_indexes = [i for i, char in enumerate(word[1:-1], start=1) if char in VOWELS]
    if vowel_indexes and len(word) >= 7 and rng.random() < 0.25:
        index = rng.choice(vowel_indexes)
        return word[:index] + word[index + 1 :], False

    middle = max(1, min(len(word) - 2, len(word) // 2))
    if rng.random() < 0.45:
        chars = list(word)
        chars[middle], chars[middle + 1] = chars[middle + 1], chars[middle]
        return "".join(chars), False

    neighbor_pool = KEYBOARD_NEIGHBORS.get(word[middle], "")
    if neighbor_pool:
        chars = list(word)
        chars[middle] = rng.choice(neighbor_pool)
        return "".join(chars), True

    return word, False


def spellingMutator(
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> str:
    rng = rng or random.Random()
    tokens = _tokenize(text)

    for index in _word_indexes(tokens):
        if stats.spelling_errors >= budget.spelling:
            break

        token = tokens[index]
        lower = token.lower()
        if _looks_protected(token) or lower in KNOWN_WRONG_FORMS:
            continue

        probability = _weighted_typo_probability(lower, profile, budget)
        if rng.random() >= probability:
            continue

        if lower == "you" and budget.grammar == 0 and rng.random() < 0.45:
            mutated, used_keyboard = "u", False
        else:
            mutated, used_keyboard = _human_typo(lower, rng)
        if mutated == lower or mutated.count(" ") > 0:
            continue

        tokens[index] = _match_case(token, mutated)
        stats.spelling_errors += 1
        stats.changed_words += 1
        if used_keyboard:
            stats.keyboard_typos += 1
        if mutated in KNOWN_WRONG_FORMS:
            stats.known_typos += 1

    return _compress_spaces(_join_tokens(tokens))


def _apply_phrase_rules(
    text: str,
    rules: Sequence[tuple[re.Pattern[str], str]],
    budget_left: int,
    sentence_pressure: float,
    stats: MutationStats,
    rng: random.Random,
) -> str:
    mutated = text

    for pattern, replacement in rules:
        if stats.grammar_errors >= budget_left:
            break
        if not pattern.search(mutated):
            continue
        if rng.random() < min(0.88, 0.56 + ((sentence_pressure - 1.0) * 0.55)):
            mutated = pattern.sub(replacement, mutated, count=1)
            stats.grammar_errors += 1
            stats.changed_words += 1

    return mutated


def grammarMutator(
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> str:
    rng = rng or random.Random()
    if budget.grammar <= 0 or budget.sentence_pressure <= 1.0 and _word_count(text) <= 7:
        return text

    grammar_rules = COMPILED_GRAMMAR_RULES
    if profile["grammar_bias"] == "hindi":
        grammar_rules = COMPILED_HINDI_RULES + COMPILED_GRAMMAR_RULES
    elif profile["grammar_bias"] == "mixed":
        grammar_rules = COMPILED_GRAMMAR_RULES + COMPILED_HINDI_RULES[:2]

    mutated = _apply_phrase_rules(text, grammar_rules, budget.grammar, budget.sentence_pressure, stats, rng)

    if stats.grammar_errors < budget.grammar and budget.sentence_pressure > 1.10:
        for pattern, replacement in LONG_SENTENCE_GRAMMAR_FALLBACKS:
            candidate = pattern.sub(replacement, mutated, count=1)
            if candidate != mutated:
                mutated = candidate
                stats.grammar_errors += 1
                stats.changed_words += 1
                break

    if stats.grammar_errors < budget.grammar and profile["grammar_bias"] != "light" and rng.random() < 0.35:
        candidate = re.sub(r"\bthe\b\s+", "", mutated, count=1, flags=re.IGNORECASE)
        if candidate != mutated:
            mutated = candidate
            stats.grammar_errors += 1
            stats.helper_removals += 1
            stats.changed_words += 1

    return _compress_spaces(mutated)


def hindiMutator(
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> str:
    rng = rng or random.Random()
    if budget.grammar <= 0 or profile["grammar_bias"] not in {"hindi", "mixed"}:
        return text

    if stats.grammar_errors >= budget.grammar:
        return text

    mutated = text
    for pattern, replacement in COMPILED_HINDI_RULES:
        if stats.grammar_errors >= budget.grammar:
            break
        if pattern.search(mutated) and rng.random() < 0.45:
            mutated = pattern.sub(replacement, mutated, count=1)
            stats.grammar_errors += 1
            stats.changed_words += 1

    return _compress_spaces(mutated)


def fillerMutator(
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> str:
    rng = rng or random.Random()
    if budget.fillers <= 0:
        return text

    parts = SENTENCE_SPLIT_RE.split(text)
    if len(parts) == 1:
        return text

    allowed_fillers = profile["fillers"] or FILLERS
    rebuilt: List[str] = []

    for i in range(0, len(parts), 2):
        sentence = parts[i]
        suffix = parts[i + 1] if i + 1 < len(parts) else ""
        if not sentence.strip():
            rebuilt.append(sentence + suffix)
            continue

        updated = sentence
        if stats.filler_count < budget.fillers:
            filler = rng.choice(allowed_fillers)
            if filler == "only":
                updated = f"{sentence.rstrip()} only"
            else:
                updated = f"{filler}, {sentence.lstrip()}"
            stats.filler_count += 1

        rebuilt.append(updated + suffix)

    return _compress_spaces("".join(rebuilt))


def repeatMutator(
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> str:
    rng = rng or random.Random()
    if budget.repeat <= 0 or stats.repeat_count >= budget.repeat:
        return text

    patterns = [
        (re.compile(r"\bvery\b", re.IGNORECASE), "very very"),
        (re.compile(r"\breally\b", re.IGNORECASE), "really really"),
        (re.compile(r"\bthe\b", re.IGNORECASE), "the the"),
    ]

    for pattern, replacement in patterns:
        if pattern.search(text) and rng.random() < max(0.20, REPEAT_RATE * profile["repeat_scale"]):
            stats.repeat_count += 1
            stats.changed_words += 1
            return _compress_spaces(pattern.sub(replacement, text, count=1))

    return text


def _score_candidate(original: str, text: str, stats: MutationStats, budget: MutationBudget) -> MutationStats:
    word_count = max(1, _word_count(original))
    damage = (
        stats.spelling_errors * 13
        + stats.grammar_errors * 12
        + stats.filler_count * 6
        + stats.repeat_count * 10
        + stats.helper_removals * 5
    )
    stats.damage_score = max(0, min(100, damage))

    corruption_penalty = 0
    if DOUBLE_WORD_RE.search(text):
        corruption_penalty += 6
    if stats.changed_words > max(6, word_count // 3):
        corruption_penalty += 16
    if re.search(r"\b[a-z]{2,}\s+[a-z]{2,}\s+[a-z]{2,}\s+[a-z]{2,}\b", text) and stats.changed_words > 5:
        corruption_penalty += 8

    quality = 92
    quality -= stats.damage_score * 0.40
    quality -= corruption_penalty
    quality -= max(0, stats.repeat_count - budget.repeat) * 12
    stats.quality_score = max(0, min(100, round(quality)))

    humanity = 64
    humanity += stats.known_typos * 8
    humanity += min(16, stats.spelling_errors * 5)
    humanity += stats.filler_count * 5
    humanity += stats.grammar_errors * 6
    if stats.quality_score >= 75:
        humanity += 6
    if 25 <= stats.damage_score <= 60:
        humanity += 12
    else:
        humanity -= 10
    humanity -= corruption_penalty
    stats.humanity_score = max(0, min(100, round(humanity)))

    stats.text = text
    return stats


def qualityCheck(
    original: str,
    text: str,
    *,
    budget: MutationBudget,
    profile: dict[str, Any],
    stats: MutationStats,
    rng: random.Random | None = None,
) -> tuple[str, MutationStats]:
    rng = rng or random.Random()
    scored = _score_candidate(original, text, stats, budget)

    if scored.humanity_score >= 70 and scored.quality_score >= 60 and 25 <= scored.damage_score <= 60:
        return text, scored

    refined = text
    if stats.spelling_errors < budget.spelling and rng.random() < 0.65:
        refined = spellingMutator(refined, budget=budget, profile=profile, stats=stats, rng=rng)
    if stats.grammar_errors < budget.grammar and rng.random() < 0.55:
        refined = grammarMutator(refined, budget=budget, profile=profile, stats=stats, rng=rng)
    if stats.filler_count < budget.fillers and rng.random() < 0.40:
        refined = fillerMutator(refined, budget=budget, profile=profile, stats=stats, rng=rng)

    return refined, _score_candidate(original, refined, stats, budget)


def _choose_persona(rng: random.Random) -> str:
    personas = list(WRITER_PROFILES)
    weights = [0.34, 0.20, 0.24, 0.22]
    return rng.choices(personas, weights=weights, k=1)[0]


def _build_candidate(text: str, persona: str, seed: int) -> MutationStats:
    rng = random.Random(seed)
    profile = WRITER_PROFILES[persona]
    budget = _mutation_budget(text, profile)
    stats = MutationStats(persona=persona)

    mutated = text
    mutated = spellingMutator(mutated, budget=budget, profile=profile, stats=stats, rng=rng)
    mutated = grammarMutator(mutated, budget=budget, profile=profile, stats=stats, rng=rng)
    mutated = hindiMutator(mutated, budget=budget, profile=profile, stats=stats, rng=rng)
    mutated = fillerMutator(mutated, budget=budget, profile=profile, stats=stats, rng=rng)
    mutated = repeatMutator(mutated, budget=budget, profile=profile, stats=stats, rng=rng)
    mutated, stats = qualityCheck(
        text,
        mutated,
        budget=budget,
        profile=profile,
        stats=stats,
        rng=rng,
    )
    stats.text = mutated
    return stats


def _candidate_rank(stats: MutationStats) -> tuple[int, int, int]:
    penalty = 0
    if stats.humanity_score < 70:
        penalty += 70 - stats.humanity_score
    if stats.quality_score < 60:
        penalty += (60 - stats.quality_score) * 2
    if stats.damage_score < 25:
        penalty += 25 - stats.damage_score
    if stats.damage_score > 60:
        penalty += (stats.damage_score - 60) * 2
    return (penalty, -stats.humanity_score, -stats.quality_score)


def mutateText(text: str) -> dict[str, Any]:
    seed_rng = random.Random()
    persona = _choose_persona(seed_rng)
    log(f"selected persona={persona}")

    candidates = [
        _build_candidate(text, persona, seed_rng.randint(1, 10_000_000))
        for _ in range(CANDIDATE_COUNT)
    ]

    for index, candidate in enumerate(candidates, start=1):
        log(
            "candidate=%s humanity=%s quality=%s damage=%s spelling=%s grammar=%s filler=%s repeat=%s"
            % (
                index,
                candidate.humanity_score,
                candidate.quality_score,
                candidate.damage_score,
                candidate.spelling_errors,
                candidate.grammar_errors,
                candidate.filler_count,
                candidate.repeat_count,
            )
        )

    valid_candidates = [
        candidate
        for candidate in candidates
        if candidate.humanity_score > 70
        and candidate.quality_score > 60
        and 25 <= candidate.damage_score <= 60
    ]
    selected = min(valid_candidates or candidates, key=_candidate_rank)
    return {
        "persona": selected.persona,
        "spelling_errors": selected.spelling_errors,
        "grammar_errors": selected.grammar_errors,
        "filler_count": selected.filler_count,
        "repeat_count": selected.repeat_count,
        "quality_score": selected.quality_score,
        "humanity_score": selected.humanity_score,
        "damage_score": selected.damage_score,
        "text": selected.text,
    }


class HumanTextHandler(BaseHTTPRequestHandler):
    server_version = "HumanText/2.0"

    def do_POST(self) -> None:
        if self.path != "/mutate":
            self.send_error(404)
            return

        length_header = self.headers.get("Content-Length", "0")
        try:
            length = int(length_header)
        except ValueError:
            self.send_error(400)
            return

        if length <= 0:
            self.send_error(400, "request body is required")
            return

        try:
            log(f"processing request path={self.path} bytes={length}")
            payload = self.rfile.read(length)
            text = payload.decode("utf-8", errors="replace").strip()
            if not text:
                self.send_error(400, "text body is empty")
                return

            log(f"processing text chars={len(text)}")
            result = mutateText(text)
            body = json.dumps(result, ensure_ascii=True).encode("utf-8")
            log(
                "result ready persona=%s humanity=%s quality=%s damage=%s"
                % (
                    result["persona"],
                    result["humanity_score"],
                    result["quality_score"],
                    result["damage_score"],
                )
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except BrokenPipeError:
            log("client disconnected before response write completed")
        except Exception as exc:
            log(f"request failed error={exc.__class__.__name__}")
            with contextlib.suppress(BrokenPipeError):
                body = b'{"error":"internal server error"}'
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

    def do_GET(self) -> None:
        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return


class HumanTextServer(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> None:
    log(
        "loading vocabulary terms=%s misspellings=%s fillers=%s grammar_rules=%s"
        % (
            len(VOCABULARY_TERMS),
            len(MISSPELLINGS),
            len(FILLERS),
            len(GRAMMAR_RULES) + len(HINDI_RULES),
        )
    )

    try:
        server = HumanTextServer((HOST, PORT), HumanTextHandler)
    except OSError as exc:
        log(f"failed to bind port={PORT} error={exc.__class__.__name__}")
        raise

    log(f"server running in port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("shutdown requested from keyboard interrupt")
    finally:
        server.shutdown()
        server.server_close()
        log("server stopped cleanly")


if __name__ == "__main__":
    main()
