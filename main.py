from Planning_Module.Planner import *
from Encoding_Module.environment import *


if __name__ == '__main__':

    env = Environment()

    planner = Planner(env)

    plan_elevators_p2 = ["(board p1 slow0-0 n2 n0 n1)", "(board p0 fast0 n3 n0 n1)", "(move-down-slow slow0-0 n2 n1)",
                         "(board p3 slow0-0 n1 n1 n2)", "(move-down-slow slow0-0 n1 n0)", "(leave p1 slow0-0 n0 n2 n1)",
                         "(move-up-slow slow0-0 n0 n2)", "(leave p3 slow0-0 n2 n1 n0)", "(move-down-fast fast0 n3 n0)",
                         "(board p2 fast0 n0 n1 n2)", "(leave p0 fast0 n0 n2 n1)", "(move-up-fast fast0 n0 n3)", "(leave p2 fast0 n3 n1 n0)"]

    plan_transport_p2 = ["(pick-up truck-1 city-loc-2 package-1 capacity-1 capacity-2)", "(drive truck-1 city-loc-2 city-loc-3)",
                         "(pick-up truck-1 city-loc-3 package-2 capacity-0 capacity-1)", "(drive truck-1 city-loc-3 city-loc-1)",
                         "(drop truck-1 city-loc-1 package-1 capacity-0 capacity-1)", "(pick-up truck-1 city-loc-1 package-3 capacity-0 capacity-1)",
                         "(drive truck-1 city-loc-1 city-loc-5)", "(drop truck-1 city-loc-5 package-2 capacity-0 capacity-1)",
                         "(pick-up truck-1 city-loc-5 package-4 capacity-0 capacity-1)", "(drive truck-1 city-loc-5 city-loc-2)",
                         "(drive truck-1 city-loc-2 city-loc-3)", "(drop truck-1 city-loc-3 package-4 capacity-0 capacity-1)",
                         "(drive truck-1 city-loc-3 city-loc-4)", "(drop truck-1 city-loc-4 package-3 capacity-1 capacity-2)"]

    plan_floortile_p1 = ["(right robot2 tile_2-2 tile_2-3)", "(down robot2 tile_2-3 tile_1-3)", "(paint-up robot2 tile_2-3 tile_1-3 black)",
                         "(right robot1 tile_3-1 tile_3-2)", "(paint-up robot1 tile_4-2 tile_3-2 white)", "(down robot1 tile_3-2 tile_2-2)",
                         "(left robot1 tile_2-2 tile_2-1)", "(paint-down robot1 tile_1-1 tile_2-1 white)", "(paint-up robot1 tile_3-1 tile_2-1 white)"]

    print(planner.get_real_score(plan_floortile_p1))

