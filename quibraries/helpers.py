"""Module that includes helpers that for querying."""
# pylint: skip-file

from typing import Dict, List, Tuple, Union


def extract(*keys):
    class From:
        def of(self, container: Union[Dict, List, Tuple]):
            class Promise(list):  # workaround to allow monkeypatch to builtin list type
                def then(self, f) -> List:
                    pass

            def then(f):
                try:
                    return [f(value) for value in values]
                except (ValueError, TypeError):
                    return [f(key, value) for key, value in zip(keys, values)]

            values = Promise()
            values.extend([container.pop(k) for k in keys if k in container])  # type: ignore
            values.then = then  # type: ignore
            return values

    return From()
