from statistics import mean, pstdev


def min_max_normalize(value: float, min_value: float, max_value: float) -> float:
    if max_value == min_value:
        return 0.0
    return (value - min_value) / (max_value - min_value)


def safe_z_score(value: float, values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    distribution_std = pstdev(values)
    if distribution_std == 0:
        return 0.0
    return (value - mean(values)) / distribution_std
