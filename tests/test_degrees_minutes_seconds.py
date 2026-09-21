from __future__ import annotations

import numpy as np
import pytest

from units import DegreesMinutesSeconds


def make_sexagesimal(
    degrees: list[float],
    minutes: list[float],
    seconds: list[float],
    is_negative: list[bool] | None = None,
) -> DegreesMinutesSeconds:
    return DegreesMinutesSeconds(
        degrees=np.array(degrees),
        minutes=np.array(minutes),
        seconds=np.array(seconds),
        is_negative=np.array([False] * len(degrees) if is_negative is None else is_negative, dtype=np.bool_),
    )


def test_keeps_canonical_components() -> None:
    sexagesimal: DegreesMinutesSeconds = make_sexagesimal([35.0, 0.0], [40.0, 59.0], [30.36, 59.999])
    assert np.array_equal(sexagesimal.degrees, np.array([35.0, 0.0]))
    assert np.array_equal(sexagesimal.minutes, np.array([40.0, 59.0]))
    assert np.array_equal(sexagesimal.seconds, np.array([30.36, 59.999]))
    assert len(sexagesimal) == 2


def test_accepts_integer_arrays() -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds(
        degrees=np.array([10]),
        minutes=np.array([30]),
        seconds=np.array([36]),
        is_negative=np.array([False]),
    )
    assert len(sexagesimal) == 1


def test_accepts_empty_arrays() -> None:
    assert len(make_sexagesimal([], [], [])) == 0


def test_is_immutable() -> None:
    sexagesimal: DegreesMinutesSeconds = make_sexagesimal([1.0], [0.0], [0.0])
    with pytest.raises(AttributeError):
        setattr(sexagesimal, "degrees", np.array([2.0]))


def test_keeps_sign() -> None:
    sexagesimal: DegreesMinutesSeconds = make_sexagesimal([1.0, 2.0], [0.0, 0.0], [0.0, 0.0], [True, False])
    assert np.array_equal(sexagesimal.is_negative, np.array([True, False]))


def test_rejects_non_boolean_sign() -> None:
    with pytest.raises(TypeError, match="boolean"):
        _ = DegreesMinutesSeconds(
            degrees=np.array([1.0]),
            minutes=np.array([0.0]),
            seconds=np.array([0.0]),
            is_negative=np.array([1]),
        )


def test_rejects_sign_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="same shape"):
        _ = make_sexagesimal([1.0], [0.0], [0.0], [True, False])


def test_rejects_non_1d_arrays() -> None:
    with pytest.raises(ValueError, match="1D"):
        _ = DegreesMinutesSeconds(
            degrees=np.array([[1.0]]),
            minutes=np.array([[0.0]]),
            seconds=np.array([[0.0]]),
            is_negative=np.array([[False]]),
        )


@pytest.mark.parametrize(
    ("degrees", "minutes", "seconds"),
    [
        ([1.0, 2.0], [30.0], [0.0]),
        ([1.0], [30.0, 15.0], [0.0]),
        ([1.0], [30.0], [0.0, 1.0]),
    ],
)
def test_rejects_shape_mismatch(degrees: list[float], minutes: list[float], seconds: list[float]) -> None:
    with pytest.raises(ValueError, match="same shape"):
        _ = make_sexagesimal(degrees, minutes, seconds)


@pytest.mark.parametrize(
    ("degrees", "minutes", "seconds"),
    [
        ([-35.0], [0.0], [0.0]),
        ([35.0], [-1.0], [0.0]),
        ([35.0], [0.0], [-0.5]),
        ([1.0, -1.0], [0.0, 0.0], [0.0, 0.0]),
    ],
)
def test_rejects_negative(degrees: list[float], minutes: list[float], seconds: list[float]) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        _ = make_sexagesimal(degrees, minutes, seconds)


@pytest.mark.parametrize(
    ("degrees", "minutes"),
    [
        ([35.5], [0.0]),
        ([35.0], [40.5]),
    ],
)
def test_rejects_fractional_degrees_or_minutes(degrees: list[float], minutes: list[float]) -> None:
    with pytest.raises(ValueError, match="whole numbers"):
        _ = make_sexagesimal(degrees, minutes, [0.0])


@pytest.mark.parametrize(
    ("minutes", "seconds"),
    [
        ([60.0], [0.0]),
        ([0.0], [60.0]),
        ([75.0], [0.0]),
        ([0.0], [3600.0]),
    ],
)
def test_rejects_out_of_range(minutes: list[float], seconds: list[float]) -> None:
    with pytest.raises(ValueError, match="less than 60"):
        _ = make_sexagesimal([1.0], minutes, seconds)


@pytest.mark.parametrize(
    ("components", "expected"),
    [
        (([35.0], [40.0], [30.36]), ([35.0], [40.0], [30.36])),
        (([0.0], [0.0], [90.0]), ([0.0], [1.0], [30.0])),
        (([0.0], [75.0], [0.0]), ([1.0], [15.0], [0.0])),
        (([0.0], [59.0], [60.0]), ([1.0], [0.0], [0.0])),
        (([35.5], [0.0], [0.0]), ([35.0], [30.0], [0.0])),
        (([0.0], [1.5], [0.0]), ([0.0], [1.0], [30.0])),
        (([1.5], [75.0], [90.0]), ([2.0], [46.0], [30.0])),
        (([0.0], [0.0], [7322.5]), ([2.0], [2.0], [2.5])),
    ],
)
def test_normalized_carries_components(
    components: tuple[list[float], list[float], list[float]],
    expected: tuple[list[float], list[float], list[float]],
) -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds.normalized(
        degrees=np.array(components[0]),
        minutes=np.array(components[1]),
        seconds=np.array(components[2]),
    )
    assert np.allclose(sexagesimal.degrees, np.array(expected[0]))
    assert np.allclose(sexagesimal.minutes, np.array(expected[1]))
    assert np.allclose(sexagesimal.seconds, np.array(expected[2]))


def test_normalized_is_elementwise() -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds.normalized(
        degrees=np.array([0.0, 10.0]),
        minutes=np.array([120.0, 0.0]),
        seconds=np.array([0.0, 61.0]),
    )
    assert np.allclose(sexagesimal.degrees, np.array([2.0, 10.0]))
    assert np.allclose(sexagesimal.minutes, np.array([0.0, 1.0]))
    assert np.allclose(sexagesimal.seconds, np.array([0.0, 1.0]))


def test_normalized_accepts_integer_arrays() -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds.normalized(
        degrees=np.array([0]),
        minutes=np.array([61]),
        seconds=np.array([61]),
    )
    assert np.array_equal(sexagesimal.degrees, np.array([1]))
    assert np.array_equal(sexagesimal.minutes, np.array([2]))
    assert np.array_equal(sexagesimal.seconds, np.array([1]))


def test_normalized_defaults_to_non_negative() -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds.normalized(
        degrees=np.array([1.0, 2.0]),
        minutes=np.array([0.0, 0.0]),
        seconds=np.array([0.0, 0.0]),
    )
    assert np.array_equal(sexagesimal.is_negative, np.array([False, False]))


def test_normalized_keeps_given_sign() -> None:
    sexagesimal: DegreesMinutesSeconds = DegreesMinutesSeconds.normalized(
        degrees=np.array([0.0]),
        minutes=np.array([90.0]),
        seconds=np.array([0.0]),
        is_negative=np.array([True]),
    )
    assert np.allclose(sexagesimal.degrees, np.array([1.0]))
    assert np.allclose(sexagesimal.minutes, np.array([30.0]))
    assert np.array_equal(sexagesimal.is_negative, np.array([True]))


def test_normalized_rejects_sign_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="same shape"):
        _ = DegreesMinutesSeconds.normalized(
            degrees=np.array([1.0]),
            minutes=np.array([0.0]),
            seconds=np.array([0.0]),
            is_negative=np.array([True, False]),
        )


@pytest.mark.parametrize(
    ("is_negative", "expected"),
    [
        ([False, False], [3723.5, 0.0]),
        ([True, True], [-3723.5, -0.0]),
        ([False, True], [3723.5, -0.0]),
    ],
)
def test_total_seconds(is_negative: list[bool], expected: list[float]) -> None:
    sexagesimal: DegreesMinutesSeconds = make_sexagesimal([1.0, 0.0], [2.0, 0.0], [3.5, 0.0], is_negative)
    assert np.allclose(sexagesimal.total_seconds, np.array(expected))


def test_equality_compares_signed_value() -> None:
    assert make_sexagesimal([1.0], [30.0], [0.0]) == DegreesMinutesSeconds.normalized(
        degrees=np.array([1.5]),
        minutes=np.array([0.0]),
        seconds=np.array([0.0]),
    )
    assert make_sexagesimal([1.0, 2.0], [0.0, 0.0], [0.0, 0.0]) == make_sexagesimal([1.0, 2.0], [0.0, 0.0], [0.0, 0.0])


def test_equality_treats_signed_zero_as_equal() -> None:
    assert make_sexagesimal([0.0], [0.0], [0.0], [True]) == make_sexagesimal([0.0], [0.0], [0.0], [False])


def test_inequality_on_different_sign() -> None:
    assert make_sexagesimal([1.0], [0.0], [0.0], [True]) != make_sexagesimal([1.0], [0.0], [0.0], [False])


def test_inequality_on_different_shapes() -> None:
    assert make_sexagesimal([1.0], [0.0], [0.0]) != make_sexagesimal([1.0, 1.0], [0.0, 0.0], [0.0, 0.0])


def test_inequality_with_other_types() -> None:
    assert make_sexagesimal([1.0], [0.0], [0.0]) != 1.0


def test_normalized_rejects_negative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        _ = DegreesMinutesSeconds.normalized(
            degrees=np.array([1.0]),
            minutes=np.array([-1.0]),
            seconds=np.array([0.0]),
        )


def test_normalized_rejects_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="same shape"):
        _ = DegreesMinutesSeconds.normalized(
            degrees=np.array([1.0, 2.0]),
            minutes=np.array([0.0]),
            seconds=np.array([0.0]),
        )


def test_normalized_rejects_non_1d_arrays() -> None:
    with pytest.raises(ValueError, match="1D"):
        _ = DegreesMinutesSeconds.normalized(
            degrees=np.array([[1.0]]),
            minutes=np.array([[0.0]]),
            seconds=np.array([[0.0]]),
            is_negative=np.array([[False]]),
        )
