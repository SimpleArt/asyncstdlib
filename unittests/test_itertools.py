import itertools

import pytest

import asyncstdlib as a

from .utility import sync, asyncify


@sync
async def test_accumulate():
    async def reduction(x, y):
        return x + y

    for reducer in (reduction, lambda x, y: x + y):
        for itertype in (asyncify, list):
            assert await a.list(a.accumulate(itertype([0, 1]), reducer)) == list(
                itertools.accumulate([0, 1], lambda x, y: x + y)
            )
            assert await a.list(
                a.accumulate(itertype([0, 1, 2, 3, 4, 0, -5]), reducer)
            ) == list(itertools.accumulate([0, 1, 2, 3, 4, 0, -5], lambda x, y: x + y))
            assert await a.list(a.accumulate(itertype([12]), reducer)) == list(
                itertools.accumulate([12], lambda x, y: x + y)
            )
            assert await a.list(a.accumulate(itertype([1]), reducer, initial=23)) == [
                23,
                24,
            ]
            assert await a.list(a.accumulate(itertype([]), reducer, initial=42)) == [42]


@sync
async def test_accumulate_misuse():
    with pytest.raises(TypeError):
        assert await a.list(a.accumulate([]))
