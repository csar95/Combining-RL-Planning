;
; A version of the logistics domain with typing and type hierarchies
;
(define (domain domain3)
    (:requirements
        :strips :typing
    )

    (:types
        object
        city
        truck  airplane -  vehicle
        office      airport - location
    )

    (:predicates
        (loc ?l - location ?c - city)
        (vehicle_at ?v -    vehicle   ?l  - location)
        ( object_at ?o -  object ?l -  location)
        (in  ?p - object ?v - vehicle)

        (travelling )
        (   is_damaged)
        (   end_missions  )
    )

    (:action load
        :parameters 
            (?o - object ?v - vehicle ?l - location)
        :precondition
            (and
		        (vehicle_at ?v ?l)
                (object_at ?o ?l)
            )
        :effect
            (and
                (in ?o ?v)
                (not (object_at ?o ?l))
            )
    )

    (:action unload
        :parameters
            (?o - object ?v - vehicle ?l - location)
        :precondition
            (and
		        (vehicle_at ?v ?l)
                (in ?o ?v)
            )
        :effect
            (and
                (object_at ?o ?l)
                (not (in ?o ?v))
            )
    )

    (:action drive
        :parameters
            (?t - truck ?c - city ?l1 - location ?l2 - location)
        :precondition
            (and
		        (vehicle_at ?t ?l1)
                (loc ?l1 ?c)
                (loc ?l2 ?c)
            )
        :effect
            (and
                (vehicle_at ?t ?l2)
                (not (vehicle_at ?t ?l1))
            )
    )

    (:action fly
        :parameters
            (?p - airplane ?a1 - airport ?a2 - airport)
        :precondition
            (and
		        (vehicle_at ?p ?a1)
            )
        :effect
            (and 
                (vehicle_at ?p ?a2)
                (not (vehicle_at ?p ?a1))
            )
    )
)
