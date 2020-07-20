(define (problem transport-large)
    (:domain transport)

    (:objects
        city-loc-1 city-loc-2 city-loc-3 city-loc-4 city-loc-5 city-loc-6 city-loc-7 city-loc-8 - location
        truck-1 truck-2 truck-3 - vehicle
        package-1 package-2 package-3 package-4 package-5 package-6 - package
        capacity-0 capacity-1 capacity-2 capacity-3 - capacity-number
    )

    (:init
        (= (total-cost) 0)
        (capacity-predecessor capacity-0 capacity-1)
        (capacity-predecessor capacity-1 capacity-2)
        (capacity-predecessor capacity-2 capacity-3)

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

        (road city-loc-5 city-loc-6)
        (road city-loc-6 city-loc-5)
        (= (road-length city-loc-6 city-loc-5) 13)
        (= (road-length city-loc-5 city-loc-6) 13)

        (road city-loc-3 city-loc-6)
        (road city-loc-6 city-loc-3)
        (= (road-length city-loc-6 city-loc-3) 17)
        (= (road-length city-loc-3 city-loc-6) 17)

        (road city-loc-2 city-loc-7)
        (road city-loc-7 city-loc-2)
        (= (road-length city-loc-7 city-loc-2) 15)
        (= (road-length city-loc-2 city-loc-7) 15)

        (road city-loc-4 city-loc-7)
        (road city-loc-7 city-loc-4)
        (= (road-length city-loc-7 city-loc-4) 19)
        (= (road-length city-loc-4 city-loc-7) 19)

        (road city-loc-3 city-loc-8)
        (road city-loc-8 city-loc-3)
        (= (road-length city-loc-8 city-loc-3) 13)
        (= (road-length city-loc-3 city-loc-8) 13)

        (road city-loc-6 city-loc-8)
        (road city-loc-8 city-loc-6)
        (= (road-length city-loc-8 city-loc-6) 17)
        (= (road-length city-loc-6 city-loc-8) 17)

        (at package-1 city-loc-2)
        (at package-2 city-loc-3)
        (at package-3 city-loc-1)
        (at package-4 city-loc-5)
        (at package-5 city-loc-7)
        (at package-6 city-loc-2)

        (at truck-1 city-loc-2)
        (capacity truck-1 capacity-3)

        (at truck-2 city-loc-4)
        (capacity truck-2 capacity-3)

        (at truck-3 city-loc-7)
        (capacity truck-3 capacity-3)
    )

    (:goal
        (and
        (at package-1 city-loc-1)
        (at package-2 city-loc-5)
        (at package-3 city-loc-4)
        (at package-4 city-loc-3)
        (at package-5 city-loc-6)
        (at package-6 city-loc-8))
    )

    (:metric minimize (total-cost))

)
