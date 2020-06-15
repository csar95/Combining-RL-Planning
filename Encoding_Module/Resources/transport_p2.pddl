(define (problem transport-city-sequential-40nodes-1000size-4degree-100mindistance-4trucks-16packages-2008seed)
    (:domain transport)

    (:objects
        city-loc-1 city-loc-2 city-loc-3 city-loc-4 city-loc-5 - location
        truck-1 truck-2 - vehicle
        package-1 package-2 package-3 package-4 - package
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

        (road city-loc-3 city-loc-4)
        (road city-loc-4 city-loc-3)
        (= (road-length city-loc-3 city-loc-4) 13)
        (= (road-length city-loc-4 city-loc-3) 13)

        (road city-loc-1 city-loc-5)
        (road city-loc-5 city-loc-1)
        (= (road-length city-loc-1 city-loc-5) 17)
        (= (road-length city-loc-5 city-loc-1) 17)

        (road city-loc-2 city-loc-5)
        (road city-loc-5 city-loc-2)
        (= (road-length city-loc-2 city-loc-5) 15)
        (= (road-length city-loc-5 city-loc-2) 15)

        (at package-1 city-loc-2)
        (at package-2 city-loc-3)
        (at package-3 city-loc-1)
        (at package-4 city-loc-5)

        (at truck-1 city-loc-2)
        (capacity truck-1 capacity-2)

        (at truck-2 city-loc-4)
        (capacity truck-2 capacity-2)
    )

    (:goal
        (and
        (at package-1 city-loc-1)
        (at package-2 city-loc-5)
        (at package-3 city-loc-4)
        (at package-4 city-loc-3))
    )

    (:metric minimize (total-cost))

)
