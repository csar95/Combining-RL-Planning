(define (domain parking)
    (:requirements :strips :typing :action-costs)
    (:types
        car
        curb
    )
    (:predicates
        (at-curb ?car - car)
        (at-curb-num ?car - car ?curb - curb)
        (behind-car ?car ?front-car - car)
        (car-clear ?car - car)
        (curb-clear ?curb - curb)
    )

    (:functions
        (total-cost) - number
    )

    (:action move-curb-to-curb
        :parameters (?car - car ?srccurb ?destcurb - curb)
        :precondition (and (car-clear ?car) (curb-clear ?destcurb) (at-curb-num ?car ?srccurb))
        :effect (and (not (curb-clear ?destcurb)) (curb-clear ?srccurb) (at-curb-num ?car ?destcurb) (not (at-curb-num ?car ?srccurb)) (increase (total-cost) 1))
    )

    (:action move-curb-to-car
        :parameters (?car - car ?srccurb - curb ?destcar - car)
        :precondition (and (car-clear ?car) (car-clear ?destcar) (at-curb-num ?car ?srccurb) (at-curb ?destcar))
        :effect (and (not (car-clear ?destcar)) (curb-clear ?srccurb) (behind-car ?car ?destcar) (not (at-curb-num ?car ?srccurb)) (not (at-curb ?car)) (increase (total-cost) 1))
    )

    (:action move-car-to-curb
        :parameters (?car - car ?srccar - car ?destcurb - curb)
        :precondition (and (car-clear ?car) (curb-clear ?destcurb) (behind-car ?car ?srccar))
        :effect (and (not (curb-clear ?destcurb)) (car-clear ?srccar) (at-curb-num ?car ?destcurb) (not (behind-car ?car ?srccar)) (at-curb ?car) (increase (total-cost) 1))
    )

    (:action move-car-to-car
        :parameters (?car - car ?srccar - car ?destcar - car)
        :precondition (and (car-clear ?car) (car-clear ?destcar) (behind-car ?car ?srccar) (at-curb ?destcar))
        :effect (and (not (car-clear ?destcar)) (car-clear ?srccar) (behind-car ?car ?destcar) (not (behind-car ?car ?srccar)) (increase (total-cost) 1))
    )
)
