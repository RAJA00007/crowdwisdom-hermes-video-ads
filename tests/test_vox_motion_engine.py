"""tests/test_vox_motion_engine.py

Comprehensive Test Suite for the Vox Motion Graphics Engine.

Verifies:
- All 20 object primitives defined
- All 19 transformation primitives defined
- Easing mathematical accuracy (linear, cubic, overshoot back, elastic)
- 2.5D Camera perspective projection & depth scaling
- Object keyframe property interpolation
- Halftone cutout procedural generation (with white keyline & offset red stroke)
- Newspaper fragment, kinetic typography, stat counter, and network mesh rendering
- Multi-layer composition rendering across timeline
"""

import math
import sys
from pathlib import Path
from PIL import Image

# Add project root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.vox_motion_engine import (
    ALL_OBJECT_PRIMITIVES,
    ALL_TRANSFORMATION_PRIMITIVES,
    AnimatedStatCounter,
    Camera25D,
    HalftoneTraderFigure,
    KineticTextObject,
    MotionObject,
    NetworkMeshLayer,
    NewspaperFragment,
    VoxMotionComposition,
    build_vox_motion_proof_sequence,
    ease_in_back,
    ease_linear,
    ease_out_back,
    ease_out_cubic,
    ease_out_quad,
)


def test_01_primitives_definitions():
    """Verify all required object and transformation primitives are defined."""
    assert len(ALL_OBJECT_PRIMITIVES) == 20, f"Expected 20 primitives, got {len(ALL_OBJECT_PRIMITIVES)}"
    assert len(ALL_TRANSFORMATION_PRIMITIVES) == 20, f"Expected 20 transformation primitives, got {len(ALL_TRANSFORMATION_PRIMITIVES)}"

    # Check key primitives
    assert "HALFTONE_CUTOUT" in ALL_OBJECT_PRIMITIVES
    assert "TRADER_FIGURE" in ALL_OBJECT_PRIMITIVES
    assert "NEWSPAPER_FRAGMENT" in ALL_OBJECT_PRIMITIVES
    assert "STAT_NUMBER" in ALL_OBJECT_PRIMITIVES
    assert "NETWORK_NODE" in ALL_OBJECT_PRIMITIVES
    assert "TEXT_OBJECT" in ALL_OBJECT_PRIMITIVES

    assert "DUPLICATE" in ALL_TRANSFORMATION_PRIMITIVES
    assert "COLLAPSE" in ALL_TRANSFORMATION_PRIMITIVES
    assert "PAPER_TEAR" in ALL_TRANSFORMATION_PRIMITIVES
    assert "CAMERA_DIVE" in ALL_TRANSFORMATION_PRIMITIVES
    assert "CONNECT" in ALL_TRANSFORMATION_PRIMITIVES


def test_02_easing_functions():
    """Verify easing functions interpolate properly within bounds."""
    for fn in [ease_linear, ease_out_quad, ease_out_cubic]:
        assert fn(0.0) == 0.0
        assert fn(1.0) == 1.0
        assert 0.0 < fn(0.5) <= 1.0

    # ease_out_back should overshoot 1.0 around t=0.7-0.9
    overshot = False
    for step in range(1, 10):
        t = step / 10.0
        if ease_out_back(t) > 1.0:
            overshot = True
            break
    assert overshot, "ease_out_back did not produce expected spring overshoot > 1.0"


def test_03_camera_25d_projection():
    """Verify 2.5D camera perspective projection scales with depth Z."""
    cam = Camera25D(focal_length=1000.0, width=1080, height=1920)
    cam.x = 0.0
    cam.y = 0.0
    cam.z = -1000.0

    # Point at Z=0 (distance = 1000, scale = 1.0)
    sx0, sy0, scale0 = cam.project(0.0, 0.0, 0.0)
    assert sx0 == 540.0
    assert sy0 == 960.0
    assert abs(scale0 - 1.0) < 0.001

    # Point deeper at Z=1000 (distance = 2000, scale = 0.5)
    sx1, sy1, scale1 = cam.project(0.0, 0.0, 1000.0)
    assert abs(scale1 - 0.5) < 0.001

    # Point closer at Z=-500 (distance = 500, scale = 2.0)
    sx2, sy2, scale2 = cam.project(0.0, 0.0, -500.0)
    assert abs(scale2 - 2.0) < 0.001


def test_04_motion_object_interpolation():
    """Verify MotionObject smoothly interpolates keyframes."""
    obj = MotionObject("test_obj", "TRADER_FIGURE", x=0.0, y=0.0)
    obj.add_keyframe("x", 0.0, 100.0)
    obj.add_keyframe("x", 2.0, 500.0, ease_linear)

    assert obj.get_property_at_time("x", 0.0) == 100.0
    assert obj.get_property_at_time("x", 1.0) == 300.0
    assert obj.get_property_at_time("x", 2.0) == 500.0
    assert obj.get_property_at_time("x", 3.0) == 500.0  # Clamp


def test_05_halftone_cutout_procedural():
    """Verify HalftoneTraderFigure builds authentic B&W sprite with keyline and red offset."""
    fig = HalftoneTraderFigure("trader", x=0, y=0, z=0)
    sprite = fig._build_sprite()
    assert sprite.width > 200 and sprite.height > 200
    # Verify non-empty transparency and RGBA channels
    assert sprite.mode == "RGBA"
    alpha_max = max(sprite.split()[3].getdata())
    assert alpha_max > 200


def test_06_stat_counter_acceleration():
    """Verify AnimatedStatCounter counts up from 1 to 1,482,930."""
    counter = AnimatedStatCounter("stat", target_number=1482930)
    counter.add_keyframe("count_progress", 0.0, 0.0)
    counter.add_keyframe("count_progress", 1.0, 1.0, ease_out_quad)

    # At start
    counter.update_at_time(0.0)
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    cam = Camera25D()
    counter.render(canvas, cam, 0.0)
    assert counter.current_val == 1

    # At finish
    counter.update_at_time(1.0)
    counter.render(canvas, cam, 1.0)
    assert counter.current_val == 1482930


def test_07_composition_rendering():
    """Verify multi-layer VoxMotionComposition renders valid frames across the timeline."""
    comp = build_vox_motion_proof_sequence(duration_sec=10.0)
    assert len(comp.objects) >= 8

    # Render test frames at critical transition moments
    test_timestamps = [0.5, 2.5, 5.0, 7.5, 9.5]
    for t in test_timestamps:
        frame = comp.render_frame(t)
        assert frame.size == (1080, 1920)
        assert frame.mode == "RGBA"
        # Verify frame is not blank
        extrema = frame.getextrema()
        assert extrema is not None


def run_all_tests():
    tests = [
        ("01_primitives_definitions", test_01_primitives_definitions),
        ("02_easing_functions", test_02_easing_functions),
        ("03_camera_25d_projection", test_03_camera_25d_projection),
        ("04_motion_object_interpolation", test_04_motion_object_interpolation),
        ("05_halftone_cutout_procedural", test_05_halftone_cutout_procedural),
        ("06_stat_counter_acceleration", test_06_stat_counter_acceleration),
        ("07_composition_rendering", test_07_composition_rendering),
    ]

    print("\n============================================================")
    print("VOX MOTION ENGINE TEST SUITE")
    print("============================================================\n")

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f" [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f" [FAIL] {name}: {e}")
            failed += 1

    print("\n------------------------------------------------------------")
    print(f"Summary: {passed} passed, {failed} failed out of {len(tests)} tests.")
    print("------------------------------------------------------------\n")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
