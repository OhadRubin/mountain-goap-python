import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "rpg.utils", Path(__file__).resolve().parent.parent / "rpg" / "utils.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Vector2 = module.Vector2
RpgUtils = module.RpgUtils


def test_vector_equality_and_move():
    v1 = Vector2(0, 0)
    v2 = Vector2(1, 0)
    assert RpgUtils.in_distance(v1, v2, 1)
    v3 = RpgUtils.move_towards_other_position(v1, v2)
    assert v3 == Vector2(1, 0)
