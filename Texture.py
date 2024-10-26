import os
from typing import Tuple

import numpy as np
import pygame as pg
from numpy.typing import NDArray
from pygame import Surface

__all__ = ['Texture']


class Texture:
    """
    Texture class to load and store textures

    Attributes:
    -----------
    _file: str
        The file path of the texture
    _texture: Surface
        The pygame surface of the texture
    _size: int
        The size of the texture
    _array: NDArray
        The numpy array of the texture

    Methods:
    --------
    size() -> int:
        Returns the size of the texture
    array() -> NDArray:
        Returns the numpy array of the texture
    get_size() -> Tuple[int, int]:
        Returns the size of the texture
    """
    _file: str
    _texture: Surface
    _size: int
    _array: NDArray

    def __init__(self, i):
        """
        Initialize the texture
        :param i: int: The index of the texture
        """
        file = f'img/texture_{i}'
        extensions = ['png', 'jpeg', 'jpg']
        for extension in extensions:
            if os.path.exists(f'{file}.{extension}'):
                self._file = f'{file}.{extension}'
                break
        else:
            raise FileNotFoundError(f'No texture found for {file}')
        self._texture = pg.image.load(self._file)
        self._size = min(self._texture.get_size()) - 1
        self._array = pg.surfarray.array3d(self._texture).astype(dtype=np.uint32)

    @property
    def size(self) -> int:
        """
        Returns the size of the texture
        :return: int: The size of the texture
        """
        return self._size

    @property
    def array(self) -> NDArray:
        """
        Returns the numpy array of the texture
        :return: NDArray: The numpy array of the texture
        """
        return self._array

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the texture
        :return: Tuple[int, int]: The size of the texture
        """
        return self._texture.get_size()
