from Planning_Module.Planner import *
from Encoding_Module.environment import *


if __name__ == '__main__':

    env = Environment()

    planner = Planner(env)

    plan_elevators_p2 = ["(board p1 slow0-0 n2 n0 n1)", "(board p0 fast0 n3 n0 n1)", "(move-down-slow slow0-0 n2 n1)",
                         "(board p3 slow0-0 n1 n1 n2)", "(move-down-slow slow0-0 n1 n0)", "(leave p1 slow0-0 n0 n2 n1)",
                         "(move-up-slow slow0-0 n0 n2)", "(leave p3 slow0-0 n2 n1 n0)", "(move-down-fast fast0 n3 n0)",
                         "(board p2 fast0 n0 n1 n2)", "(leave p0 fast0 n0 n2 n1)", "(move-up-fast fast0 n0 n3)", "(leave p2 fast0 n3 n1 n0)"]

    plan_elevators_p5 = ["(board p1 slow1-0 n6 n0 n1)", "(move-down-slow slow0-0 n2 n1)", "(board p0 slow0-0 n1 n0 n1)",
                         "(move-up-slow slow1-0 n6 n8)", "(board p2 slow1-0 n8 n1 n2)", "(move-up-slow slow0-0 n1 n4)",
                         "(move-down-slow slow1-0 n8 n4)", "(leave p1 slow1-0 n4 n2 n1)", "(board p3 slow1-0 n4 n1 n2)",
                         "(leave p2 slow1-0 n4 n2 n1)", "(board p2 slow0-0 n4 n1 n2)", "(leave p0 slow0-0 n4 n2 n1)",
                         "(board p0 slow1-0 n4 n1 n2)", "(move-up-slow slow1-0 n4 n6)", "(leave p0 slow1-0 n6 n2 n1)",
                         "(move-up-slow slow1-0 n6 n8)", "(leave p3 slow1-0 n8 n1 n0)", "(move-down-slow slow0-0 n4 n0)",
                         "(board p4 slow0-0 n0 n1 n2)", "(leave p2 slow0-0 n0 n2 n1)", "(move-up-slow slow0-0 n0 n3)",
                         "(leave p4 slow0-0 n3 n1 n0)"]

    plan_transport_p2 = ["(pick-up truck-1 city-loc-2 package-1 capacity-1 capacity-2)", "(drive truck-1 city-loc-2 city-loc-3)",
                         "(pick-up truck-1 city-loc-3 package-2 capacity-0 capacity-1)", "(drive truck-1 city-loc-3 city-loc-1)",
                         "(drop truck-1 city-loc-1 package-1 capacity-0 capacity-1)", "(pick-up truck-1 city-loc-1 package-3 capacity-0 capacity-1)",
                         "(drive truck-1 city-loc-1 city-loc-5)", "(drop truck-1 city-loc-5 package-2 capacity-0 capacity-1)",
                         "(pick-up truck-1 city-loc-5 package-4 capacity-0 capacity-1)", "(drive truck-1 city-loc-5 city-loc-2)",
                         "(drive truck-1 city-loc-2 city-loc-3)", "(drop truck-1 city-loc-3 package-4 capacity-0 capacity-1)",
                         "(drive truck-1 city-loc-3 city-loc-4)", "(drop truck-1 city-loc-4 package-3 capacity-1 capacity-2)"]

    plan_transport_p3 = ["(pick-up truck-1 city-loc-2 package-6 capacity-2 capacity-3)", "(drive truck-1 city-loc-2 city-loc-3)",
                         "(pick-up truck-3 city-loc-7 package-5 capacity-2 capacity-3)", "(drive truck-3 city-loc-7 city-loc-2)",
                         "(pick-up truck-3 city-loc-2 package-1 capacity-1 capacity-2)", "(drive truck-1 city-loc-3 city-loc-8)",
                         "(drop truck-1 city-loc-8 package-6 capacity-2 capacity-3)", "(drive truck-3 city-loc-2 city-loc-3)",
                         "(pick-up truck-3 city-loc-3 package-2 capacity-0 capacity-1)", "(drive truck-3 city-loc-3 city-loc-1)",
                         "(drop truck-3 city-loc-1 package-1 capacity-0 capacity-1)", "(pick-up truck-3 city-loc-1 package-3 capacity-0 capacity-1)",
                         "(drive truck-3 city-loc-1 city-loc-5)", "(drop truck-3 city-loc-5 package-2 capacity-0 capacity-1)",
                         "(pick-up truck-3 city-loc-5 package-4 capacity-0 capacity-1)", "(drive truck-3 city-loc-5 city-loc-6)",
                         "(drop truck-3 city-loc-6 package-5 capacity-0 capacity-1)", "(drive truck-3 city-loc-6 city-loc-3)",
                         "(drop truck-3 city-loc-3 package-4 capacity-1 capacity-2)", "(drive truck-3 city-loc-3 city-loc-4)",
                         "(drop truck-3 city-loc-4 package-3 capacity-2 capacity-3)"]

    plan_floortile_p1 = ["(right robot2 tile_2-2 tile_2-3)", "(down robot2 tile_2-3 tile_1-3)", "(paint-up robot2 tile_2-3 tile_1-3 black)",
                         "(right robot1 tile_3-1 tile_3-2)", "(paint-up robot1 tile_4-2 tile_3-2 white)", "(down robot1 tile_3-2 tile_2-2)",
                         "(left robot1 tile_2-2 tile_2-1)", "(paint-down robot1 tile_1-1 tile_2-1 white)", "(paint-up robot1 tile_3-1 tile_2-1 white)"]

    plan_floortile_p2 = ["(right robot2 tile_3-2 tile_3-3)", "(right robot2 tile_3-3 tile_3-4)", "(paint-up robot1 tile_3-1 tile_2-1 white)",
                         "(paint-down robot2 tile_2-4 tile_3-4 black)", "(right robot1 tile_2-1 tile_2-2)",
                         "(paint-down robot1 tile_1-2 tile_2-2 white)", "(up robot1 tile_2-2 tile_3-2)", "(paint-down robot1 tile_2-2 tile_3-2 white)",
                         "(right robot1 tile_3-2 tile_3-3)", "(up robot2 tile_3-4 tile_4-4)", "(left robot2 tile_4-4 tile_4-3)",
                         "(left robot2 tile_4-3 tile_4-2)", "(right robot1 tile_3-3 tile_3-4)", "(paint-down robot2 tile_3-2 tile_4-2 black)",
                         "(paint-up robot1 tile_4-4 tile_3-4 white)"]

    print(planner.get_real_score(plan_elevators_p5))

