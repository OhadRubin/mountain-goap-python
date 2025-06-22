# // <copyright file="PermutationSelectorGeneratorTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from typing import Dict, Any, List, Optional

class PermutationSelectorGeneratorTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    def test_it_selects_from_a_collection(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection(collection)
        permutations = selector({}) # Empty state dict
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

    def test_it_selects_from_a_collection_in_state(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection_in_state("collection")
        permutations = selector({"collection": collection})
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

    def test_it_selects_from_an_integer_range(self):
        selector = PermutationSelectorGenerators.select_from_integer_range(1, 4)
        permutations = selector({}) # Empty state dict
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

