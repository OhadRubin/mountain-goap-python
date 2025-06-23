from typing import get_origin
from goap.types import StateDictionary

def test_state_dictionary_alias():
    assert get_origin(StateDictionary) is dict
