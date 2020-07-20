(define (problem elevators-sequencedstrips-p16_14_1_1)
    (:domain elevators-sequencedstrips)

    (:objects
        n2 n1 n0 - count
        p1 p0  - passenger
        slow0-0 - slow-elevator
    )

    (:init
        (next n0 n1) (next n1 n2)

        (above n0 n1) (above n0 n2)
        (above n1 n2)

        (lift-at slow0-0 n2)
        (passengers slow0-0 n0)
        (can-hold slow0-0 n1) (can-hold slow0-0 n2)
        (reachable-floor slow0-0 n0)(reachable-floor slow0-0 n1)(reachable-floor slow0-0 n2)

        (passenger-at p0 n2)
        (passenger-at p1 n1)

        (= (travel-slow n0 n1) 6) (= (travel-slow n0 n2) 7) (= (travel-slow n1 n2) 6)

        (= (total-cost) 0)
    )

    (:goal
        (and
        (passenger-at p0 n1)
        (passenger-at p1 n2))
    )

    (:metric minimize (total-cost))

)
