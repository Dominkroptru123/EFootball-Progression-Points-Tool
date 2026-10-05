import math

POSITIONS = { "GK": 0, "CB": 1, "LB": 2, "RB": 3, "DMF": 4, "CMF": 5, "LMF": 6, "RMF": 7, "AMF": 8, "LWF": 9, "RWF": 10, "SS": 11, "CF": 12 }

WEAK_FOOT_ACCURACY = { "Low": 0, "Medium": 1, "High": 2, "Very High": 3 }

WEIGHTS = [ 186, 136, 49, 49, 61, 37, 12, 12, 37, 49, 49, 62, 99, 0, 14, 61, 61, 61, 98, 98, 98, 171, 159, 159, 173, 210, 13, 27, 86, 86, 122, 171, 171, 171, 196, 159, 159, 210, 123, 0, 14, 61, 61, 37, 98, 110, 122, 122, 159, 159, 123, 62, 0, 0, 37, 37, 24, 49, 73, 61, 73, 86, 86, 86, 37, 27, 41, 61, 61, 122, 208, 135, 135, 196, 73, 73, 99, 37, 40, 68, 147, 147, 122, 159, 196, 196, 159, 98, 98, 74, 12, 0, 27, 24, 24, 37, 73, 86, 86, 184, 159, 159, 284, 358, 0, 14, 24, 24, 12, 12, 24, 24, 12, 12, 12, 12, 12, 0, 14, 24, 24, 12, 12, 24, 24, 12, 12, 12, 12, 12, 0, 55, 24, 24, 61, 24, 12, 12, 24, 24, 24, 25, 62, 13, 286, 147, 147, 220, 86, 49, 49, 24, 12, 12, 0, 0, 0, 191, 86, 86, 122, 86, 24, 24, 24, 12, 12, 12, 12, 0, 82, 37, 37, 98, 37, 12, 12, 12, 12, 12, 12, 12, 53, 27, 24, 24, 49, 73, 24, 24, 73, 61, 61, 99, 123, 13, 136, 220, 220, 61, 61, 196, 196, 98, 220, 220, 86, 99, 40, 150, 184, 184, 61, 86, 159, 159, 86, 159, 159, 99, 123, 80, 204, 98, 98, 122, 49, 24, 24, 24, 37, 37, 37, 86, 0, 0, 24, 24, 12, 24, 61, 61, 24, 73, 73, 74, 86, 133, 109, 37, 37, 37, 12, 12, 12, 12, 24, 24, 37, 62, 279, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 173, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 173, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 196, 196, 196, 196, 147, 147, 86, 49, 49, 49, 37, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 14, 24, 24, 24, 24, 24, 24, 24, 24, 24, 12, 12 ]

if len(WEIGHTS) != 364:
    raise RuntimeError(
        f"WEIGHTS must contain exactly 364 values, got {len(WEIGHTS)}."
    )

STAT_KEYS = (
    "Attacking Awareness",
    "Ball Control",
    "Dribbling",
    "Tight Possession",
    "Low Pass",
    "Lofted Pass",
    "Finishing",
    "Heading",
    "Set Piece Taking",
    "Curl",
    "Defensive Awareness",
    "Tackling",
    "Defensive Engagement",
    "Aggression",
    "GK Awareness",
    "GK Catching",
    "GK Parrying",
    "GK Reflexes",
    "GK Reach",
    "Speed",
    "Acceleration",
    "Kicking Power",
    "Jumping",
    "Physical Contact",
    "Balance",
    "Stamina"
)

STAT_OFFSETS = {
    "Attacking Awareness": 13,
    "Ball Control": 26,
    "Dribbling": 39,
    "Tight Possession": 52,
    "Low Pass": 65,
    "Lofted Pass": 78,
    "Finishing": 91,
    "Set Piece Taking": 104,
    "Curl": 117,
    "Heading": 130,
    "Defensive Awareness": 143,
    "Tackling": 156,
    "Aggression": 169,
    "Kicking Power": 182,
    "Speed": 195,
    "Acceleration": 208,
    "Physical Contact": 221,
    "Balance": 234,
    "Jumping": 247,
    "GK Awareness": 260,
    "GK Reach": 273,
    "GK Catching": 286,
    "GK Parrying": 299,
    "GK Reflexes": 312,
    "Stamina": 325,
    "Defensive Engagement": 351
}

STAT_OFFSET_TUPLE = tuple(
    STAT_OFFSETS[stat]
    for stat in STAT_KEYS
)

MANAGER_SKILL_MULTIPLIERS = (
    0.65,
    0.6675,
    0.685,
    0.7025,
    0.72,
    0.7375,
    0.755,
    0.7725,
    0.79,
    0.8075,
    0.825,
    0.8425,
    0.86,
    0.8775,
    0.895,
    0.9125,
    0.93,
    0.9475,
    0.965,
    0.9825,
    1,
    1,
    1.01163,
    1.01389,
    1.015625,
    1.01755,
    1.01925,
    1.02125,
    1.02275,
    1.0244,
    1.026,
    1.02725,
    1.029,
    1.03,
    1.03196,
    1.03275,
    1.03375,
    1.034091,
    1.0355,
    1.036,
    1.0365,
    1.036,
    1.036,
    1.036,
    1.036,
    1.036,
    1.036,
    1.036,
    1.036
)

PROGRESSION_MAX = 25

PROGRESSION_SLIDERS = {
    "Shooting": (
        "Finishing",
        "Set Piece Taking",
        "Curl"
    ),

    "Passing": (
        "Low Pass",
        "Lofted Pass"
    ),

    "Dribbling": (
        "Ball Control",
        "Dribbling",
        "Tight Possession"
    ),

    "Dexterity": (
        "Attacking Awareness",
        "Acceleration",
        "Balance"
    ),

    "Lower Body Strength": (
        "Speed",
        "Kicking Power",
        "Stamina"
    ),

    "Aerial Strength": (
        "Heading",
        "Jumping",
        "Physical Contact"
    ),

    "Defending": (
        "Defensive Awareness",
        "Tackling",
        "Aggression",
        "Defensive Engagement"
    ),

    "GK 1": (
        "GK Awareness",
        "Jumping"
    ),

    "GK 2": (
        "GK Parrying",
        "GK Reach"
    ),

    "GK 3": (
        "GK Catching",
        "GK Reflexes"
    )
}

AUTO_PROGRESSION_GROUPS = (
    ("Shooting",),
    ("Passing",),
    ("Dribbling",),
    ("Dexterity",),
    ("Lower Body Strength",),
    ("Defending",),
    ("Aerial Strength", "GK 1"),
    ("GK 2",),
    ("GK 3",)
)

LEVEL_COSTS = tuple(
    sum(
        math.ceil(current_level / 4)
        for current_level in range(1, level + 1)
    )
    for level in range(PROGRESSION_MAX + 1)
)

ABILITY_MAP = (
    "Attacking Awareness",
    "Ball Control",
    "Tight Possession",
    "Dribbling",
    "Low Pass",
    "Lofted Pass",
    "Finishing",
    "Set Piece Taking",
    "Curl",
    "Heading",
    "Defensive Awareness",
    "Defensive Engagement",
    "Tackling",
    "Aggression",
    "Kicking Power",
    "Speed",
    "Acceleration",
    "Balance",
    "Physical Contact",
    "Jumping",
    "GK Awareness",
    "GK Catching",
    "GK Parrying",
    "GK Reflexes",
    "GK Reach",
    "Stamina"
)

CONDITION_LABELS = {
    0: "E",
    1: "D",
    2: "C",
    3: "B",
    4: "A"
}

CONDITION_AFFECTED_AWARENESS = {
    "Attacking Awareness",
    "Defensive Awareness",
    "Defensive Engagement",
    "GK Awareness"
}

CONDITION_AFFECTED_PHYSICAL = {
    "Kicking Power",
    "Speed",
    "Acceleration",
    "Physical Contact",
    "Balance",
    "Jumping",
    "Stamina"
}


def build_condition_table(*groups):
    table = []

    for modifiers, count in groups:
        table.extend(
            [modifiers] * count
        )

    if len(table) != 61:
        raise RuntimeError(
            "Condition table must contain exactly "
            f"61 entries, got {len(table)}."
        )

    return tuple(table)


CONDITION_MODIFIERS_A = build_condition_table(
    ((14, 10, 5), 23),
    ((13, 10, 5), 1),
    ((13, 9, 5), 2),
    ((12, 9, 5), 2),
    ((12, 8, 5), 1),
    ((11, 8, 4), 3),
    ((10, 7, 4), 3),
    ((9, 7, 4), 1),
    ((9, 6, 4), 2),
    ((8, 6, 3), 2),
    ((8, 5, 3), 1),
    ((7, 5, 3), 3),
    ((6, 4, 3), 3),
    ((5, 4, 2), 1),
    ((5, 3, 2), 2),
    ((4, 3, 2), 3),
    ((4, 2, 2), 1),
    ((3, 2, 2), 7)
)

CONDITION_MODIFIERS_B = build_condition_table(
    ((9, 5, 2), 25),
    ((8, 5, 2), 3),
    ((8, 4, 2), 1),
    ((7, 4, 2), 6),
    ((6, 4, 2), 1),
    ((6, 3, 2), 3),
    ((5, 3, 1), 3),
    ((5, 2, 1), 1),
    ((4, 2, 1), 5),
    ((3, 2, 1), 1),
    ((3, 1, 1), 4),
    ((2, 1, 1), 8)
)

CONDITION_MODIFIERS_D = build_condition_table(
    ((-1, -2, -3), 27),
    ((-1, -2, -4), 5),
    ((-1, -3, -4), 2),
    ((-1, -3, -5), 4),
    ((-2, -3, -5), 3),
    ((-2, -3, -6), 3),
    ((-2, -4, -6), 4),
    ((-2, -4, -7), 13)
)

CONDITION_MODIFIERS_E = build_condition_table(
    ((-2, -3, -5), 25),
    ((-2, -3, -6), 1),
    ((-2, -4, -6), 4),
    ((-2, -4, -7), 2),
    ((-3, -5, -7), 3),
    ((-3, -5, -8), 3),
    ((-3, -6, -8), 2),
    ((-3, -6, -9), 3),
    ((-4, -7, -9), 1),
    ((-4, -7, -10), 4),
    ((-4, -8, -11), 13)
)

CONDITION_MODIFIERS = {
    0: CONDITION_MODIFIERS_E,
    1: CONDITION_MODIFIERS_D,
    3: CONDITION_MODIFIERS_B,
    4: CONDITION_MODIFIERS_A
}


def progression_level_cost(level):
    if 0 <= level <= PROGRESSION_MAX:
        return LEVEL_COSTS[level]

    total = 0

    for current_level in range(1, level + 1):
        total += math.ceil(current_level / 4)

    return total


def available_progression_points(level_cap):
    return max(
        0,
        (level_cap - 1) * 2
    )


def total_progression_points(sliders):
    return sum(
        LEVEL_COSTS[level]
        for level in sliders.values()
    )


def max_affordable_level(
    slider_name,
    sliders,
    total_points
):
    used_without_slider = sum(
        LEVEL_COSTS[level]
        for name, level in sliders.items()
        if name != slider_name
    )

    remaining = (
        total_points -
        used_without_slider
    )

    for level in range(
        PROGRESSION_MAX,
        -1,
        -1
    ):
        if LEVEL_COSTS[level] <= remaining:
            return level

    return 0


def validate_progression(
    sliders,
    level_cap
):
    if level_cap < 1:
        raise ValueError(
            "Level cap must be at least 1."
        )

    for slider_name in PROGRESSION_SLIDERS:

        if slider_name not in sliders:
            raise ValueError(
                f"Missing progression slider "
                f"'{slider_name}'."
            )

    for name, level in sliders.items():

        if name not in PROGRESSION_SLIDERS:
            raise ValueError(
                f"Unknown progression slider "
                f"'{name}'."
            )

        if type(level) is not int:
            raise ValueError(
                f"{name}: progression level must be "
                "an integer."
            )

        if level < 0 or level > PROGRESSION_MAX:
            raise ValueError(
                f"{name}: progression level must be "
                f"between 0 and {PROGRESSION_MAX}."
            )

    available = available_progression_points(
        level_cap
    )

    used = total_progression_points(
        sliders
    )

    if used > available:
        raise ValueError(
            f"Progression points exceeded: "
            f"{used}/{available} used."
        )


def normalize_stats(stats):
    missing = [
        stat
        for stat in STAT_KEYS
        if stat not in stats
    ]

    if missing:
        raise ValueError(
            "Missing stats: " +
            ", ".join(missing)
        )

    unknown = [
        stat
        for stat in stats
        if stat not in STAT_OFFSETS
    ]

    if unknown:
        raise ValueError(
            "Unknown stat(s): " +
            ", ".join(unknown)
        )

    return {
        stat: stats[stat]
        for stat in STAT_KEYS
    }


def apply_progression(
    stats,
    sliders
):
    modified = stats.copy()

    for slider_name, level in sliders.items():

        if level == 0:
            continue

        for stat in PROGRESSION_SLIDERS[
            slider_name
        ]:
            modified[stat] = min(
                99,
                modified[stat] + level
            )

    return modified


def get_manager_skill_multiplier(
    proficiency
):
    if proficiency >= 50:
        index = proficiency - 50
    else:
        index = 0

    return MANAGER_SKILL_MULTIPLIERS[
        min(
            index,
            len(MANAGER_SKILL_MULTIPLIERS) - 1
        )
    ]


def apply_manager_skill(
    stats,
    proficiency
):
    multiplier = get_manager_skill_multiplier(
        proficiency
    )

    if multiplier == 1:
        return stats.copy()

    modified = stats.copy()
    gain = multiplier - 1

    for stat in STAT_KEYS:

        value = stats[stat]

        modified[stat] = min(
            99,
            value +
            math.floor(
                value * gain
            )
        )

    return modified


def get_manager_boost_ids(boosts):
    if not boosts:
        return ()

    result = []

    for boost in boosts:

        if isinstance(boost, int):

            if boost == -1:
                continue

            if 0 <= boost < len(ABILITY_MAP):
                result.append(boost)

            continue

        if isinstance(boost, str):

            try:
                result.append(
                    ABILITY_MAP.index(boost)
                )

            except ValueError:
                raise ValueError(
                    f"Unknown manager boost "
                    f"'{boost}'."
                )

            continue

        raise ValueError(
            f"Unknown manager boost "
            f"'{boost}'."
        )

    return tuple(result)


def get_manager_bonus_stats(manager):
    bonuses = {}

    for boost_id in get_manager_boost_ids(
        manager.get("Boosts", ())
    ):

        stat = ABILITY_MAP[boost_id]

        bonuses[stat] = (
            bonuses.get(stat, 0) + 1
        )

    return bonuses


def apply_manager_boosts(
    stats,
    manager
):
    modified = stats.copy()

    for boost_id in get_manager_boost_ids(
        manager.get("Boosts", ())
    ):

        stat = ABILITY_MAP[boost_id]

        modified[stat] = (
            modified[stat] + 1
        )

    return modified


def apply_condition(
    stats,
    condition,
    condition_ovr
):
    if condition == 2:
        return stats.copy()

    if condition not in CONDITION_MODIFIERS:
        raise ValueError(
            f"Invalid condition {condition}."
        )

    index = max(
        0,
        min(
            60,
            condition_ovr - 40
        )
    )

    awareness, normal, physical = (
        CONDITION_MODIFIERS[
            condition
        ][index]
    )

    modified = stats.copy()

    for stat in STAT_KEYS:

        if stat == "Aggression":
            continue

        if stat in CONDITION_AFFECTED_AWARENESS:
            modifier = awareness

        elif stat in CONDITION_AFFECTED_PHYSICAL:
            modifier = physical

        else:
            modifier = normal

        modified[stat] = max(
            1,
            min(
                99,
                modified[stat] + modifier
            )
        )

    return modified


def boost_magnitude(booster):
    if not booster:
        return 0

    magnitude = booster.get(
        "Magnitude",
        0
    )

    if (
        isinstance(
            magnitude,
            (int, float)
        )
        and math.isfinite(magnitude)
        and magnitude > 0
    ):
        return magnitude

    maximum = 0

    for value in booster.get(
        "Applied Stats",
        {}
    ).values():

        number = float(value)

        if (
            math.isfinite(number)
            and
            number > maximum
        ):
            maximum = number

    return maximum


def js_round(value):
    return math.floor(
        value + 0.5
    )


def scaled_boost(
    booster,
    level
):
    if not booster or level <= 0:
        return None

    magnitude = boost_magnitude(
        booster
    )

    if magnitude <= 0:
        return None

    if level >= magnitude:
        return booster

    scaled = dict(
        booster
    )

    scaled_stats = {}

    for stat, value in booster.get(
        "Applied Stats",
        {}
    ).items():

        numeric_value = float(value)

        if numeric_value == 0:
            scaled_value = 0

        else:
            scaled_value = js_round(
                numeric_value *
                level /
                magnitude
            )

        scaled_stats[stat] = scaled_value

    scaled["Applied Stats"] = scaled_stats

    return scaled


def get_scaled_booster_stats(
    booster
):
    if not booster:
        return {}

    scaled = scaled_boost(
        booster,
        booster.get(
            "Level",
            0
        )
    )

    if not scaled:
        return {}

    result = {}

    for stat, amount in scaled.get(
        "Applied Stats",
        {}
    ).items():

        if stat not in STAT_OFFSETS:
            raise ValueError(
                f"Unknown booster stat "
                f"'{stat}'."
            )

        result[stat] = (
            result.get(stat, 0) +
            amount
        )

    return result


def apply_player_boost(
    stats,
    booster
):
    modified = stats.copy()

    if not booster:
        return modified

    for stat, amount in booster.get(
        "Applied Stats",
        {}
    ).items():

        if stat not in STAT_OFFSETS:
            raise ValueError(
                f"Unknown booster stat "
                f"'{stat}'."
            )

        modified[stat] = (
            modified.get(stat, 0) +
            amount
        )

    return modified


def rating_contribution_value(value):
    if value > 25:
        return value - 25

    return 0


def rating_total(
    position,
    height,
    weak_foot_accuracy,
    stats
):
    position_index = POSITIONS[
        position
    ]

    total = (
        WEIGHTS[position_index]
        *
        rating_contribution_value(
            height - 111
        )
    )

    for stat_index in range(
        len(STAT_KEYS)
    ):

        total += (
            WEIGHTS[
                STAT_OFFSET_TUPLE[stat_index]
                + position_index
            ]
            *
            rating_contribution_value(
                stats[
                    STAT_KEYS[stat_index]
                ]
            )
        )

    weak_foot_value = math.floor(
        59 *
        weak_foot_accuracy /
        3
        +
        40
    )

    total += (
        WEIGHTS[
            338 + position_index
        ]
        *
        rating_contribution_value(
            weak_foot_value
        )
    )

    return total


def compute_overall_ratings(
    position,
    height,
    weak_foot_accuracy,
    stats
):
    total = rating_total(
        position,
        height,
        weak_foot_accuracy,
        stats
    )

    decimal_value = max(
        (total + 500) / 1000,
        40
    )

    decimal_rating = (
        js_round(
            100 * decimal_value
        )
        / 100
    )

    integer_rating = max(
        math.floor(
            (total + 500) / 1000
        ),
        40
    )

    return (
        integer_rating,
        decimal_rating
    )


def compute_overall_rating_decimal(
    position,
    height,
    weak_foot_accuracy,
    stats
):
    return compute_overall_ratings(
        position,
        height,
        weak_foot_accuracy,
        stats
    )[1]


def compute_overall_rating(
    position,
    height,
    weak_foot_accuracy,
    stats
):
    return compute_overall_ratings(
        position,
        height,
        weak_foot_accuracy,
        stats
    )[0]


def get_modified_stats(
    stats,
    manager,
    proficiency,
    progression,
    condition,
    height,
    weak_foot_accuracy,
    position,
    player_booster_1=None,
    player_booster_2=None
):
    base_stats = normalize_stats(
        stats
    )

    progression_stats = apply_progression(
        base_stats,
        progression
    )

    condition_ovr = compute_overall_rating(
        position,
        height,
        weak_foot_accuracy,
        progression_stats
    )

    manager_skill_stats = apply_manager_skill(
        progression_stats,
        proficiency
    )

    condition_stats = apply_condition(
        manager_skill_stats,
        condition,
        condition_ovr
    )

    manager_boosted_stats = apply_manager_boosts(
        condition_stats,
        manager
    )

    booster_1_scaled = (
        scaled_boost(
            player_booster_1,
            player_booster_1.get(
                "Level",
                0
            )
        )
        if player_booster_1
        else None
    )

    player_booster_1_stats = (
        apply_player_boost(
            manager_boosted_stats,
            booster_1_scaled
        )
    )

    booster_2_scaled = (
        scaled_boost(
            player_booster_2,
            player_booster_2.get(
                "Level",
                0
            )
        )
        if player_booster_2
        else None
    )

    final_stats = apply_player_boost(
        player_booster_1_stats,
        booster_2_scaled
    )

    return (
        final_stats,
        condition_ovr
    )


def build_progression_context(
    position,
    base_stats,
    manager,
    proficiency,
    player_booster_1,
    player_booster_2
):
    position_index = POSITIONS[
        position
    ]

    multiplier = get_manager_skill_multiplier(
        proficiency
    )

    multiplier_gain = multiplier - 1

    manager_bonus_stats = (
        get_manager_bonus_stats(
            manager
        )
    )

    booster_1_stats = (
        get_scaled_booster_stats(
            player_booster_1
        )
    )

    booster_2_stats = (
        get_scaled_booster_stats(
            player_booster_2
        )
    )

    weighted_contributions = {}

    for stat in STAT_KEYS:

        base_value = base_stats[
            stat
        ]

        fixed_bonus = (
            manager_bonus_stats.get(
                stat,
                0
            )
            +
            booster_1_stats.get(
                stat,
                0
            )
            +
            booster_2_stats.get(
                stat,
                0
            )
        )

        maximum_progression_amount = (
            PROGRESSION_MAX
        )

        if stat == "Jumping":
            maximum_progression_amount *= 2

        weight = (
            WEIGHTS[
                STAT_OFFSETS[stat]
                + position_index
            ]
        )

        contributions = [
            0
        ] * (
            maximum_progression_amount + 1
        )

        for progression_amount in range(
            maximum_progression_amount + 1
        ):

            value = min(
                99,
                base_value +
                progression_amount
            )

            value = min(
                99,
                value +
                math.floor(
                    value *
                    multiplier_gain
                )
            )

            value += fixed_bonus

            contributions[
                progression_amount
            ] = (
                weight *
                rating_contribution_value(
                    value
                )
            )

        weighted_contributions[
            stat
        ] = contributions

    return weighted_contributions


def calculate_group_delta(
    group,
    levels,
    context
):
    progression_amounts = {}

    for slider_name, level in zip(
        group,
        levels
    ):

        for stat in PROGRESSION_SLIDERS[
            slider_name
        ]:

            progression_amounts[stat] = (
                progression_amounts.get(
                    stat,
                    0
                ) + level
            )

    delta = 0

    for stat, amount in (
        progression_amounts.items()
    ):

        contributions = context[
            stat
        ]

        delta += (
            contributions[amount]
            -
            contributions[0]
        )

    return delta


def get_progression_group_options(
    group,
    available_points,
    context
):
    options = []

    if len(group) == 1:

        slider_name = group[0]

        for level in range(
            PROGRESSION_MAX + 1
        ):

            cost = LEVEL_COSTS[level]

            if cost > available_points:
                break

            options.append({
                "cost": cost,
                "delta": calculate_group_delta(
                    group,
                    (level,),
                    context
                ),
                "levels": {
                    slider_name: level
                }
            })

        return options

    slider_a = group[0]
    slider_b = group[1]

    for level_a in range(
        PROGRESSION_MAX + 1
    ):

        cost_a = LEVEL_COSTS[
            level_a
        ]

        if cost_a > available_points:
            break

        for level_b in range(
            PROGRESSION_MAX + 1
        ):

            total_cost = (
                cost_a +
                LEVEL_COSTS[level_b]
            )

            if total_cost > available_points:
                break

            options.append({
                "cost": total_cost,
                "delta": calculate_group_delta(
                    group,
                    (
                        level_a,
                        level_b
                    ),
                    context
                ),
                "levels": {
                    slider_a: level_a,
                    slider_b: level_b
                }
            })

    return options


def auto_allocate_progression(
    position,
    base_stats,
    manager,
    proficiency,
    level_cap,
    height,
    weak_foot_accuracy,
    player_booster_1,
    player_booster_2
):
    available_points = (
        available_progression_points(
            level_cap
        )
    )

    context = build_progression_context(
        position,
        base_stats,
        manager,
        proficiency,
        player_booster_1,
        player_booster_2
    )

    dp = {
        0: {
            "delta": 0,
            "levels": {}
        }
    }

    for group in AUTO_PROGRESSION_GROUPS:

        options = (
            get_progression_group_options(
                group,
                available_points,
                context
            )
        )

        new_dp = {}

        for used_points, state in dp.items():

            state_delta = state[
                "delta"
            ]

            state_levels = state[
                "levels"
            ]

            for option in options:

                new_used = (
                    used_points +
                    option["cost"]
                )

                if new_used > available_points:
                    continue

                new_delta = (
                    state_delta +
                    option["delta"]
                )

                existing = new_dp.get(
                    new_used
                )

                if (
                    existing is None
                    or
                    new_delta >= existing["delta"]
                ):

                    new_levels = dict(
                        state_levels
                    )

                    new_levels.update(
                        option["levels"]
                    )

                    new_dp[new_used] = {
                        "delta": new_delta,
                        "levels": new_levels
                    }

        dp = new_dp

    if not dp:
        raise RuntimeError(
            f"Could not find a progression "
            f"allocation for {position}."
        )

    best_used_points, best_state = max(
        dp.items(),
        key=lambda item: (
            item[1]["delta"],
            item[0]
        )
    )

    progression = {
        slider_name: best_state[
            "levels"
        ].get(
            slider_name,
            0
        )
        for slider_name in PROGRESSION_SLIDERS
    }

    validate_progression(
        progression,
        level_cap
    )

    final_stats, condition_ovr = (
        get_modified_stats(
            base_stats,
            manager,
            proficiency,
            progression,
            CONDITION,
            height,
            weak_foot_accuracy,
            position,
            player_booster_1,
            player_booster_2
        )
    )

    integer_rating, decimal_rating = (
        compute_overall_ratings(
            position,
            height,
            weak_foot_accuracy,
            final_stats
        )
    )

    return {
        "position": position,
        "progression": progression,
        "used_points": best_used_points,
        "leftover_points": (
            available_points -
            best_used_points
        ),
        "stats": final_stats,
        "condition_ovr": condition_ovr,
        "integer_rating": integer_rating,
        "decimal_rating": decimal_rating
    }


def get_progression_input(
    level_cap
):
    available = available_progression_points(
        level_cap
    )

    print("Progression")
    print("-" * 45)
    print(
        f"Available points: {available}"
    )
    print()

    sliders = {}

    for slider_name in PROGRESSION_SLIDERS:

        while True:

            try:
                value = int(
                    input(
                        f"{slider_name} "
                        f"(0-{PROGRESSION_MAX}): "
                    )
                )

            except ValueError:

                print(
                    "ERROR: progression level must be "
                    "an integer."
                )

                continue

            if (
                value < 0
                or
                value > PROGRESSION_MAX
            ):

                print(
                    f"ERROR: value must be between "
                    f"0 and {PROGRESSION_MAX}."
                )

                continue

            test = dict(sliders)

            test[slider_name] = value

            used = total_progression_points(
                test
            )

            if used > available:

                max_level = (
                    max_affordable_level(
                        slider_name,
                        sliders,
                        available
                    )
                )

                print(
                    "ERROR: too many progression points."
                )

                print(
                    f"Maximum affordable "
                    f"{slider_name} level here: "
                    f"{max_level}"
                )

                continue

            sliders[slider_name] = value
            break

    validate_progression(
        sliders,
        level_cap
    )

    return sliders


def get_progression_mode():
    while True:

        print()
        print(
            "Progression Allocation Mode"
        )
        print("-" * 45)
        print(
            "1. Automatically allocate "
            "for highest OVR"
        )
        print(
            "2. Manually allocate progression"
        )
        print()

        choice = input(
            "Choose mode (1-2): "
        ).strip()

        if choice == "1":
            return "auto"

        if choice == "2":
            return "manual"

        print(
            "ERROR: please enter 1 or 2."
        )


def print_auto_progression_result(
    result
):
    print()
    print(
        f"{result['position']} "
        f"BEST PROGRESSION"
    )
    print("-" * 60)

    print(
        f"Best OVR: "
        f"{result['integer_rating']} "
        f"({result['decimal_rating']:.2f})"
    )

    print(
        f"Condition OVR: "
        f"{result['condition_ovr']}"
    )

    print(
        f"Used Progression Points: "
        f"{result['used_points']}"
    )

    print(
        f"Leftover Progression Points: "
        f"{result['leftover_points']}"
    )

    print()

    for slider_name in PROGRESSION_SLIDERS:

        level = result[
            "progression"
        ][slider_name]

        print(
            f"{slider_name}: "
            f"{level} "
            f"(uses {LEVEL_COSTS[level]} points)"
        )


def print_progression(
    sliders,
    level_cap
):
    available = available_progression_points(
        level_cap
    )

    used = total_progression_points(
        sliders
    )

    leftover = (
        available -
        used
    )

    print("Progression")
    print("-" * 45)

    for name, level in sliders.items():

        print(
            f"{name}: "
            f"{level} "
            f"(uses {LEVEL_COSTS[level]} points)"
        )

    print()

    print(
        f"Level Cap: {level_cap}"
    )

    print(
        f"Available Progression Points: "
        f"{available}"
    )

    print(
        f"Used Progression Points: "
        f"{used}"
    )

    print(
        f"Leftover Progression Points: "
        f"{leftover}"
    )


def print_booster(
    booster
):
    if not booster:
        print("Disabled")
        return

    print(
        f"Name: "
        f"{booster.get('Name', 'Unnamed Booster')}"
    )

    level = booster.get(
        "Level",
        0
    )

    magnitude = boost_magnitude(
        booster
    )

    print(
        f"Level: {level}/{magnitude}"
    )

    print(
        "Applied Stats:"
    )

    scaled = scaled_boost(
        booster,
        level
    )

    if not scaled:

        print(
            "  Inactive"
        )

        return

    for stat, amount in scaled.get(
        "Applied Stats",
        {}
    ).items():

        print(
            f"  {stat}: +{amount}"
        )


def print_modified_stats(
    original,
    modified
):
    print(
        "Final Modified Stats:"
    )

    for stat in STAT_KEYS:

        print(
            f"{stat}: "
            f"{original[stat]} "
            f"-> "
            f"{modified[stat]}"
        )


def print_manager_boosts(
    manager
):
    boost_ids = get_manager_boost_ids(
        manager.get(
            "Boosts",
            ()
        )
    )

    print(
        "Manager Boosts:"
    )

    if not boost_ids:

        print(
            "  None"
        )

        return

    for boost_id in boost_ids:

        print(
            f"  {ABILITY_MAP[boost_id]} +1"
        )


MANAGERS = {
    "didier_deschamps_01": {
        "Name": "Didier Deschamps",

        "Boosts": (
            "Speed",
            "Ball Control"
        ),

        "Proficiency": {
            "Possession Game": 89,
            "Long Ball Counter": 89,
            "Quick Counter": 68,
            "Long Ball": 63,
            "Out Wide": 59,
            "Overload": 59
        }
    }
}


PLAYER = {
    "Height": 182,

    "Weak Foot Accuracy": "High",

    "Stats": {
        "Attacking Awareness": 75,
        "Ball Control": 82,
        "Dribbling": 81,
        "Tight Possession": 83,
        "Low Pass": 76,
        "Lofted Pass": 79,
        "Finishing": 75,
        "Heading": 56,
        "Set Piece Taking": 80,
        "Curl": 81,
        "Defensive Awareness": 42,
        "Defensive Engagement": 42,
        "Tackling": 44,
        "Aggression": 48,
        "GK Awareness": 40,
        "GK Catching": 40,
        "GK Parrying": 40,
        "GK Reflexes": 40,
        "GK Reach": 40,
        "Speed": 75,
        "Acceleration": 79,
        "Kicking Power": 75,
        "Jumping": 62,
        "Physical Contact": 73,
        "Balance": 77,
        "Stamina": 73
    }
}


ACTIVE_MANAGER = "didier_deschamps_01"

ACTIVE_PLAYSTYLE = "Long Ball Counter"

LEVEL_CAP = 32

CONDITION = 2


PLAYER_BOOSTER_1 = {
    "Name": "Fantasista +3",

    "Applied Stats": {
        "Ball Control": 3,
        "Dribbling": 3,
        "Finishing": 3,
        "Balance": 3
    },

    "Magnitude": 3,

    "Level": 3
}


PLAYER_BOOSTER_2 = {
    "Name": "Striker Instinct +1",

    "Applied Stats": {
        "Attacking Awareness": 1,
        "Ball Control": 1,
        "Finishing": 1,
        "Acceleration": 1
    },

    "Magnitude": 1,

    "Level": 1
}


def main():

    if ACTIVE_MANAGER not in MANAGERS:
        raise ValueError(
            f"Unknown manager '{ACTIVE_MANAGER}'."
        )

    manager = MANAGERS[
        ACTIVE_MANAGER
    ]

    if ACTIVE_PLAYSTYLE not in manager[
        "Proficiency"
    ]:
        raise ValueError(
            f"{manager['Name']} does not have "
            f"playstyle '{ACTIVE_PLAYSTYLE}'."
        )

    proficiency = manager[
        "Proficiency"
    ][ACTIVE_PLAYSTYLE]

    weak_foot_accuracy = (
        WEAK_FOOT_ACCURACY[
            PLAYER["Weak Foot Accuracy"]
        ]
    )

    if LEVEL_CAP < 1:
        raise ValueError(
            "LEVEL_CAP must be at least 1."
        )

    if CONDITION not in CONDITION_LABELS:
        raise ValueError(
            "CONDITION must be 0, 1, 2, 3, or 4."
        )

    base_stats = normalize_stats(
        PLAYER["Stats"]
    )

    print()

    print(
        f"Manager: {manager['Name']}"
    )

    print(
        f"Playstyle: {ACTIVE_PLAYSTYLE}"
    )

    print(
        f"Proficiency: {proficiency}"
    )

    print(
        f"Level Cap: {LEVEL_CAP}"
    )

    print(
        f"Condition: "
        f"{CONDITION_LABELS[CONDITION]} "
        f"({CONDITION})"
    )

    mode = get_progression_mode()

    print()

    best_progressions = {}

    if mode == "auto":

        print(
            "Automatically finding the "
            "highest OVR progression for "
            "every position..."
        )

        print()

        for position in POSITIONS:

            result = auto_allocate_progression(
                position,
                base_stats,
                manager,
                proficiency,
                LEVEL_CAP,
                PLAYER["Height"],
                weak_foot_accuracy,
                PLAYER_BOOSTER_1,
                PLAYER_BOOSTER_2
            )

            best_progressions[position] = (
                result
            )

            print_auto_progression_result(
                result
            )

        print()

        print(
            "=" * 70
        )

        print(
            "HIGHEST OVR FOUND FOR EACH POSITION"
        )

        print(
            "=" * 70
        )

        for position in POSITIONS:

            result = best_progressions[
                position
            ]

            print(
                f"{position}: "
                f"{result['integer_rating']} "
                f"({result['decimal_rating']:.2f})"
            )

        print()

    else:

        progression = get_progression_input(
            LEVEL_CAP
        )

        print()

        print_progression(
            progression,
            LEVEL_CAP
        )

        print()

        best_progressions = {
            position: {
                "progression": dict(
                    progression
                )
            }
            for position in POSITIONS
        }

    print_manager_boosts(
        manager
    )

    print()

    print(
        "Player Booster 1"
    )

    print("-" * 45)

    print_booster(
        PLAYER_BOOSTER_1
    )

    print()

    print(
        "Player Booster 2"
    )

    print("-" * 45)

    print_booster(
        PLAYER_BOOSTER_2
    )

    print()

    print(
        "Position OVR"
    )

    print(
        "-" * 70
    )

    if mode == "auto":

        for position in POSITIONS:

            result = best_progressions[
                position
            ]

            print(
                f"{position}: "
                f"{result['integer_rating']} "
                f"({result['decimal_rating']:.2f}) "
            )

    else:

        for position in POSITIONS:

            progression = (
                best_progressions[
                    position
                ]["progression"]
            )

            final_stats, condition_ovr = (
                get_modified_stats(
                    base_stats,
                    manager,
                    proficiency,
                    progression,
                    CONDITION,
                    PLAYER["Height"],
                    weak_foot_accuracy,
                    position,
                    PLAYER_BOOSTER_1,
                    PLAYER_BOOSTER_2
                )
            )

            integer_rating, decimal_rating = (
                compute_overall_ratings(
                    position,
                    PLAYER["Height"],
                    weak_foot_accuracy,
                    final_stats
                )
            )

            print(
                f"{position}: "
                f"{integer_rating} "
                f"({decimal_rating:.2f}) "
            )

    primary_position = "SS"

    primary_progression = (
        best_progressions[
            primary_position
        ]["progression"]
    )

    if mode == "auto":

        result = best_progressions[
            primary_position
        ]

        final_stats = result[
            "stats"
        ]

        final_rating = result[
            "integer_rating"
        ]

        decimal_rating = result[
            "decimal_rating"
        ]

    else:

        final_stats, condition_ovr = (
            get_modified_stats(
                base_stats,
                manager,
                proficiency,
                primary_progression,
                CONDITION,
                PLAYER["Height"],
                weak_foot_accuracy,
                primary_position,
                PLAYER_BOOSTER_1,
                PLAYER_BOOSTER_2
            )
        )

        final_rating, decimal_rating = (
            compute_overall_ratings(
                primary_position,
                PLAYER["Height"],
                weak_foot_accuracy,
                final_stats
            )
        )

    print()

    print(
        f"Final OVR for {primary_position}: "
        f"{final_rating} "
        f"({decimal_rating:.2f})"
    )

    print()

    print(
        f"Progression used for "
        f"{primary_position}:"
    )

    print("-" * 60)

    for slider_name in PROGRESSION_SLIDERS:

        level = primary_progression[
            slider_name
        ]

        print(
            f"{slider_name}: "
            f"{level} "
            f"(uses "
            f"{LEVEL_COSTS[level]} "
            f"points)"
        )

    print()

    print_modified_stats(
        base_stats,
        final_stats
    )


if __name__ == "__main__":

    try:
        main()

    except ValueError as error:

        print()

        print(
            f"ERROR: {error}"
        )
