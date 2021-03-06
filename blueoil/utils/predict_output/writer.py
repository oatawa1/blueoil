# -*- coding: utf-8 -*-
# Copyright 2019 The Blueoil Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import logging
import os

from blueoil.io import file_io
from blueoil.utils.predict_output.output import ImageFromJson
from blueoil.utils.predict_output.output import JsonOutput

logger = logging.getLogger(__name__)


class OutputWriter():
    def __init__(self, task, classes, image_size, data_format):
        self.json_output = JsonOutput(task, classes, image_size, data_format)
        self.image_from_json = ImageFromJson(task, classes, image_size)

    def write(self, dest, outputs, raw_images, image_files, step, save_material=True):
        """Save predict output to disk.
           numpy array, JSON, and images if you want.

        Args:
            dest (str): path to save file
            outputs (np.ndarray): save ndarray
            raw_images (np.ndarray): image ndarray
            image_files (list[str]): list of file names.
            step (int): value of training step
            save_material (bool, optional): save materials or not. Defaults to True.
        """
        save_npy(dest, outputs, step)

        json = self.json_output(outputs, raw_images, image_files)
        save_json(dest, json, step)

        if save_material:
            materials = self.image_from_json(json, raw_images, image_files)
            save_materials(dest, materials, step)


def save_npy(dest, outputs, step):
    """Save numpy array to disk.

    Args:
        dest (str): path to save file
        outputs (np.ndarray): save ndarray
        step (int): value of training step

    Raises:
        PermissionError: If dest dir has no permission to write.
        ValueError: If type of step is not int.
    """
    if type(step) is not int:
        raise ValueError("step must be integer.")

    filepath = os.path.join(dest, "npy", "{}.npy".format(step))
    file_io.makedirs(os.path.dirname(filepath))

    file_io.save_npy(filepath, outputs)

    logger.info("save npy: {}".format(filepath))


def save_json(dest, json, step):
    """Save JSON to disk.

    Args:
        dest (str): path to save file
        json (str): dumped json string
        step (int): value of training step

    Raises:
        PermissionError: If dest dir has no permission to write.
        ValueError: If type of step is not int.
    """
    if type(step) is not int:
        raise ValueError("step must be integer.")

    filepath = os.path.join(dest, "json", "{}.json".format(step))
    file_io.makedirs(os.path.dirname(filepath))

    with file_io.File(filepath, mode="w") as f:
        f.write(json)

    logger.info("save json: {}".format(filepath))


def save_materials(dest, materials, step):
    """Save materials to disk.

    Args:
        dest (str): path to save file
        materials (list[(str, PIL.Image)]): image data, str in tuple is filename.
        step (int): value of training step

    Raises:
        PermissionError: If dest dir has no permission to write.
        ValueError: If type of step is not int.
    """
    if type(step) is not int:
        raise ValueError("step must be integer.")

    for filename, content in materials:
        filepath = os.path.join(dest, "images", "{}".format(step), filename)
        file_io.makedirs(os.path.dirname(filepath))

        file_io.save_image(filepath, content)

        logger.info("save image: {}".format(filepath))
