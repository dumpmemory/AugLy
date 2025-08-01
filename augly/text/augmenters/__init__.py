#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe

from augly.text.augmenters.base64 import Base64
from augly.text.augmenters.baseline import BaselineAugmenter
from augly.text.augmenters.bidirectional import BidirectionalAugmenter
from augly.text.augmenters.case import CaseAugmenter
from augly.text.augmenters.contraction import ContractionAugmenter
from augly.text.augmenters.encode_text_context import EncodeText
from augly.text.augmenters.encode_text_strategy import EncodeTextAugmentation
from augly.text.augmenters.fun_fonts import FunFontsAugmenter
from augly.text.augmenters.insert_text import InsertTextAugmenter
from augly.text.augmenters.insertion import InsertionAugmenter
from augly.text.augmenters.leetspeak import LeetSpeak
from augly.text.augmenters.letter_replacement import LetterReplacementAugmenter
from augly.text.augmenters.text_replacement import TextReplacementAugmenter
from augly.text.augmenters.typo import TypoAugmenter
from augly.text.augmenters.upside_down import UpsideDownAugmenter
from augly.text.augmenters.word_replacement import WordReplacementAugmenter
from augly.text.augmenters.words_augmenter import WordsAugmenter

__all__ = [
    "Base64",
    "BaselineAugmenter",
    "BidirectionalAugmenter",
    "CaseAugmenter",
    "ContractionAugmenter",
    "EncodeText",
    "EncodeTextAugmentation",
    "FunFontsAugmenter",
    "InsertTextAugmenter",
    "InsertionAugmenter",
    "LeetSpeak",
    "LetterReplacementAugmenter",
    "WordsAugmenter",
    "TextReplacementAugmenter",
    "TypoAugmenter",
    "UpsideDownAugmenter",
    "WordReplacementAugmenter",
]
