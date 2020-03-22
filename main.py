import argparse

from src.simulate import simulate
from src.visualize import visualize
from src.evaluate import simple_evaluation
from src.compare import compare
from src.globals import (
    Scenario,
    NUMBER_FREE_BEDS,
    NUMBER_CORONA_BEDS,
    NUMBER_FREE_CORONA_BEDS,
    NUMBER_CORONA_PAT_IN_NORMAL_BED,
)
from src.write_out import write_output
from src.helper_functions.build_instance import build_instance

from src.schedulers.capacity_coefficient_scheduler import CapacityScheduler


# this main reads data, solves the scheduling problem, writes json output, and visualize the results
def main(args):

    if args.scenario not in [s.value for s in Scenario]:
        raise ValueError

    project_instance = build_instance(args)

    # THIS IS ONLY A DUMMY AND SHOULD REMOVED ONCE WE GENERATE REASONABLE BED DATA
    for h in project_instance.hospitals.values():
        h.nbr_free_beds = NUMBER_FREE_BEDS
        h.nbr_free_corona_beds = NUMBER_FREE_CORONA_BEDS
        h.nbr_corona_pat_in_normal_bed = NUMBER_CORONA_PAT_IN_NORMAL_BED
        h.nbr_corona_beds = NUMBER_CORONA_BEDS

    if args.compare:
        print("Start simulation of both schedulers")
        snapshots_simple, score_simple, snapshots, score = compare(project_instance)
        print("Lower score means better capacity distribution")
        print(f"standard score {score_simple} > our score {score}")
    else:
        print("Start simulation capacity scheduler")
        snapshots = simulate(project_instance, CapacityScheduler())
        score = simple_evaluation(project_instance)

    if args.visualize:
        print("Start visualizing")
        visualize(project_instance, snapshots)

    if args.output:
        write_output(project_instance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input parameters for the algorithm")
    parser.add_argument("scenario")
    parser.add_argument("-compare", default=False)
    parser.add_argument("-visualize", default=False)
    parser.add_argument("-output", default=True)

    args = parser.parse_args()

    main(args)
