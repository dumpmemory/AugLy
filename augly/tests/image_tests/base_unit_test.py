#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import tempfile
import unittest
from typing import Any, Callable, Dict, List, Optional

import imagehash
from augly.tests import ImageAugConfig
from augly.utils import pathmgr, TEST_URI
from PIL import Image


def are_equal_images(a: Image.Image, b: Image.Image) -> bool:
    threshold = 0  # hamming distance of 0 is forgiving enough for phash
    a_hash = imagehash.phash(a)
    b_hash = imagehash.phash(b)
    return a.size == b.size and a_hash - b_hash == threshold


def are_equal_metadata(
    actual_meta: List[Dict[str, Any]],
    expected_meta: List[Dict[str, Any]],
    exclude_keys: Optional[List[str]],
) -> bool:
    if actual_meta == expected_meta:
        return True

    for actual_dict, expected_dict in zip(actual_meta, expected_meta):
        for (act_k, act_v), (exp_k, exp_v) in zip(
            sorted(actual_dict.items(), key=lambda kv: kv[0]),
            sorted(expected_dict.items(), key=lambda kv: kv[0]),
        ):
            if exclude_keys is not None and act_k in exclude_keys:
                continue

            if act_k != exp_k:
                return False

            if act_v == exp_v:
                continue

            # Bboxes are tuples but stored as lists in expected metadata
            if (
                isinstance(act_v, list)
                and all(isinstance(x, tuple) for x in zip(act_v, exp_v))
                and len(act_v) == len(exp_v)
                and all(list(x) == y for x, y in zip(act_v, exp_v))
            ):
                continue

            """
            Allow relative paths in expected metadata: just check that the end of the
            actual path matches the expected path
            """
            if not (
                isinstance(act_v, str)
                and isinstance(exp_v, str)
                and act_v[-len(exp_v) :] == exp_v
            ):
                return False

    return True


class BaseImageUnitTest(unittest.TestCase):
    ref_img_dir = os.path.join(TEST_URI, "image", "dfdc_expected_output")

    def test_import(self) -> None:
        try:
            from augly import image as imaugs
        except ImportError:
            self.fail("imaugs failed to import")
        self.assertTrue(dir(imaugs), "Image directory does not exist")

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.config = ImageAugConfig(input_file_index=0)

        img_path, img_file = cls.config.get_input_path()
        cls.local_img_path = pathmgr.get_local_path(img_path)
        cls.img = Image.open(cls.local_img_path)

    def evaluate_function(self, aug_function: Callable[..., Image.Image], **kwargs):
        ref = self.get_ref_image(aug_function.__name__)

        with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
            aug_function(self.local_img_path, output_path=tmpfile.name, **kwargs)
            file_dst = Image.open(tmpfile.name)

        pil_dst = aug_function(self.img, **kwargs)

        self.assertTrue(
            are_equal_images(pil_dst, ref), "Expected and outputted images do not match"
        )
        self.assertTrue(
            are_equal_images(file_dst, ref),
            "Expected and outputted images do not match",
        )

    def evaluate_class(
        self,
        transform_class: Callable[..., Image.Image],
        fname: str,
        metadata_exclude_keys: Optional[List[str]] = None,
        check_mode: bool = True,
    ):
        metadata = []
        bboxes, bbox_format = [(0.5, 0.5, 0.25, 0.75)], "yolo"
        ref = self.get_ref_image(fname)
        dst = transform_class(
            self.img, metadata=metadata, bboxes=bboxes, bbox_format=bbox_format
        )

        if check_mode:
            self.assertTrue(
                self.img.mode == dst.mode,
                "Expected and outputted image modes do not match",
            )

        self.assertTrue(
            are_equal_metadata(metadata, self.metadata[fname], metadata_exclude_keys),
            "Expected and outputted metadata do not match",
        )
        self.assertTrue(
            are_equal_images(dst, ref), "Expected and outputted images do not match"
        )

    def get_ref_image(self, fname: str) -> Image.Image:
        ref_img_name = f"test_{fname}.png"
        ref_local_path = pathmgr.get_local_path(
            os.path.join(self.ref_img_dir, ref_img_name)
        )
        return Image.open(ref_local_path)
