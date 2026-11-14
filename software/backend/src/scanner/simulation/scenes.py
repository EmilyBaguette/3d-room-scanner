from scanner.geometry.primitives import Direction, Plane, Point, Surface


def make_rectangle(lower: Point, upper: Point, normal: Direction) -> Surface:
    return Surface(
        plane=Plane(point=lower, normal=normal),
        lower=lower,
        upper=upper,
    )


def create_alcove() -> list[Surface]:
    """Create a wall with a 1000 mm wide, 2000 mm high, 300 mm deep alcove."""

    return [
        # Main wall: left of the opening
        make_rectangle(
            lower=Point(2000, -2000, 0),
            upper=Point(2000, -500, 2500),
            normal=Direction(1, 0, 0),
        ),
        # Main wall: right of the opening
        make_rectangle(
            lower=Point(2000, 500, 0),
            upper=Point(2000, 2000, 2500),
            normal=Direction(1, 0, 0),
        ),
        # Main wall: above the opening
        make_rectangle(
            lower=Point(2000, -500, 2000),
            upper=Point(2000, 500, 2500),
            normal=Direction(1, 0, 0),
        ),
        # Alcove: back
        make_rectangle(
            lower=Point(2300, -500, 0),
            upper=Point(2300, 500, 2000),
            normal=Direction(1, 0, 0),
        ),
        # Alcove: left side
        make_rectangle(
            lower=Point(2000, -500, 0),
            upper=Point(2300, -500, 2000),
            normal=Direction(0, 1, 0),
        ),
        # Alcove: right side
        make_rectangle(
            lower=Point(2000, 500, 0),
            upper=Point(2300, 500, 2000),
            normal=Direction(0, 1, 0),
        ),
        # Alcove: top
        make_rectangle(
            lower=Point(2000, -500, 2000),
            upper=Point(2300, 500, 2000),
            normal=Direction(0, 0, 1),
        ),
        # Alcove: bottom
        make_rectangle(
            lower=Point(2000, -500, 0),
            upper=Point(2300, 500, 0),
            normal=Direction(0, 0, 1),
        ),
    ]
