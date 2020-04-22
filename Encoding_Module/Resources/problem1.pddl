;
; Problem for domain3
;
(define (problem problem3)
    (:domain domain3)

    (:objects
        truck1 truck2 truck3 -  truck
        city1 city2     city3 - city
        airplane1 - airplane
        airport1 airport2  airport3 - airport
        packet1 packet2 - object
        office1 office2 office3 - office
    )

    (:init
        (loc office1 city1)
        (  loc airport1 city1)
        (loc office2 city2)
        (   loc     airport2 city2)
        (loc office3 city3)
        (loc airport3 city3)

        (object_at packet1 office1)
        (   object_at packet2 office3)
        (vehicle_at truck1 airport1)
        (  vehicle_at truck2  airport2)
        (vehicle_at     truck3 office3)
        (vehicle_at airplane1 airport1)


        (   is_damaged)
    )

    (:goal
        (and
            (object_at packet1 office2)
            (object_at packet2 office2)
        )
    )
)

