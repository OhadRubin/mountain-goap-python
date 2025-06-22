# // <copyright file="Program.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import argparse # Standard Python library for command-line parsing

# Import demo runners
from .ArithmeticHappinessIncrementer import ArithmeticHappinessIncrementer
from .CarDemo import CarDemo
from .ComparativeHappinessIncrementer import ComparativeHappinessIncrementer
from .ConsumerDemo import ConsumerDemo
from .ExtremeHappinessIncrementer import ExtremeHappinessIncrementer
from .HappinessIncrementer import HappinessIncrementer
from .RpgExample.RpgExample import RpgExample

class Program:
    """
    Runs MountainGoap Demos.
    """

    @staticmethod
    def main(args: list[str]) -> int:
        parser = argparse.ArgumentParser(description="Run MountainGoap Demos.")
        subparsers = parser.add_subparsers(dest="command", help="Available demos")

        # Command: happiness
        happiness_parser = subparsers.add_parser("happiness", help="Run the happiness incrementer demo.")
        happiness_parser.set_defaults(func=Program._run_happiness_incrementer)

        # Command: rpg
        rpg_parser = subparsers.add_parser("rpg", help="Run the RPG enemy demo.")
        rpg_parser.set_defaults(func=Program._run_rpg_enemy_demo)

        # Command: arithmeticHappiness
        arithmetic_happiness_parser = subparsers.add_parser("arithmeticHappiness", help="Run the arithmetic happiness incrementer demo.")
        arithmetic_happiness_parser.set_defaults(func=Program._run_arithmetic_happiness_incrementer)

        # Command: extremeHappiness
        extreme_happiness_parser = subparsers.add_parser("extremeHappiness", help="Run the extreme happiness incrementer demo.")
        extreme_happiness_parser.set_defaults(func=Program._run_extreme_happiness_incrementer)

        # Command: comparativeHappiness
        comparative_happiness_parser = subparsers.add_parser("comparativeHappiness", help="Run the comparative happiness incrementer demo.")
        comparative_happiness_parser.set_defaults(func=Program._run_comparative_happiness_incrementer)

        # Command: car
        car_parser = subparsers.add_parser("car", help="Run the car demo.")
        car_parser.set_defaults(func=Program._run_car_demo)

        # Command: consumer
        consumer_parser = subparsers.add_parser("consumer", help="Run the consumer demo.")
        consumer_parser.set_defaults(func=Program._run_consumer_demo)

        if not args:
            parser.print_help()
            return 0

        parsed_args = parser.parse_args(args)

        if hasattr(parsed_args, 'func'):
            parsed_args.func()
            return 0
        else:
            parser.print_help()
            return 1 # Indicate an error or no command selected


    @staticmethod
    def _run_happiness_incrementer() -> None:
        HappinessIncrementer.run()

    @staticmethod
    def _run_rpg_enemy_demo() -> None:
        RpgExample.run()

    @staticmethod
    def _run_arithmetic_happiness_incrementer() -> None:
        ArithmeticHappinessIncrementer.run()

    @staticmethod
    def _run_extreme_happiness_incrementer() -> None:
        ExtremeHappinessIncrementer.run()

    @staticmethod
    def _run_comparative_happiness_incrementer() -> None:
        ComparativeHappinessIncrementer.run()

    @staticmethod
    def _run_car_demo() -> None:
        CarDemo.run()

    @staticmethod
    def _run_consumer_demo() -> None:
        ConsumerDemo.run()

# Standard Python entry point
if __name__ == "__main__":
    exit_code = Program.main(sys.argv[1:])
    sys.exit(exit_code)

