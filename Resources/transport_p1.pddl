(define (problem transport-city-sequential-40nodes-1000size-4degree-100mindistance-4trucks-16packages-2008seed)
    (:domain transport)

    (:objects
        city-loc-1 city-loc-2 city-loc-3 - location
        truck-1 - vehicle
        package-1 package-2 - package
        capacity-0 capacity-1 capacity-2 - capacity-number
    )

    (:init
        (= (total-cost) 0)
        (capacity-predecessor capacity-0 capacity-1)
        (capacity-predecessor capacity-1 capacity-2)

        (road city-loc-3 city-loc-1)
        (road city-loc-1 city-loc-3)
        (= (road-length city-loc-3 city-loc-1) 15)
        (= (road-length city-loc-1 city-loc-3) 15)

        (road city-loc-3 city-loc-2)
        (road city-loc-2 city-loc-3)
        (= (road-length city-loc-3 city-loc-2) 13)
        (= (road-length city-loc-2 city-loc-3) 13)

        (road city-loc-1 city-loc-2)
        (road city-loc-2 city-loc-1)
        (= (road-length city-loc-1 city-loc-2) 17)
        (= (road-length city-loc-2 city-loc-1) 17)

        (at package-1 city-loc-2)
        (at package-2 city-loc-3)

        (at truck-1 city-loc-2)
        (capacity truck-1 capacity-2)
    )

    (:goal
        (and
        (at package-1 city-loc-3)
        (at package-2 city-loc-1))
    )

    (:metric minimize (total-cost))

)
