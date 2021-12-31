import time
import importlib
from importlib import resources
import argparse

from . import __initial__
from .__config import CONSOLE
from .__loader import functions, fixtures

get_time = lambda: int(time.time())


def to_next_sec(prev_timestamp: int) -> int:
    timestamp = get_time()
    while timestamp <= prev_timestamp:
        timestamp = get_time()
    return timestamp


# tests -i --init : initialize data for the tests
# tests -f --function function_name : run a registred function, before running the tests
# tests -h --help : show help
# tests -o --only test_name : run a specific test

# eg: tests -f create_users 10

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SoftDesk API test runner")
    parser.add_argument("-i", "--init", action="store_true", help="initialize data before running the tests")
    parser.add_argument("-f", "--function", type=str, nargs="+", help="run a registred function")
    parser.add_argument("-o", "--only", type=str, nargs="+", help="run a specific test")

    args = parser.parse_args()

    if args.init:
        __initial__.__init__()

    # definitely not confusing
    if args.function:
        fn_name = args.function.pop(0)
        fn_args = args.function

        function = next(filter(lambda x: x["name"] == fn_name, functions), None)

        if function:
            function["function"](*fn_args)
        else:
            CONSOLE.log(f"Function [blue]\[{fn_name}][reset] not found")
            CONSOLE.log("Available functions:")

            for function in functions:
                CONSOLE.log(f"[cyan]\[{function['name']}][reset]: {function['desc']}")
    else:
        files = resources.contents("tests")
        files = [file[:-3] for file in files if file.endswith(".py") and not file.startswith("_")]

        for file in files:
            module = importlib.import_module(f"tests.{file}")

        from .__loader import tests

        tests = sorted(tests, key=lambda x: (x["t_order"], x["f_order"]))

        print("-" * 50)
        with CONSOLE.status(f"[bold green]Running tests...", spinner="line") as status:
            fails = 0
            successes = 0
            skipped = 0

            previous_passed = True
            previous_file = None

            for test in tests:
                file_order, order, function, req_fixture = test.values()

                CONSOLE.log(f"[Running]: {function.__doc__}")
                log = lambda *args, **kwargs: CONSOLE.log(*args, **kwargs)
                curr_module = function.__module__.split(".")[-1]

                if args.only and curr_module not in args.only:
                    CONSOLE.log(f"[bold yellow]\[skipped]")
                    print("")
                    skipped += 1
                    continue

                if order > 1 and previous_file == curr_module and not previous_passed:
                    CONSOLE.log(f"[bold yellow]\[skipped]")
                    print("")
                    skipped += 1
                    continue

                try:
                    fixture = filter(lambda x: x["name"] == req_fixture, fixtures)
                    fixture = next(fixture, {"function": lambda: {}})
                    fixture_result = fixture["function"]()

                    returned = function(**fixture_result)

                    CONSOLE.log(f"[bold green]\[passed]")

                    successes += 1
                    previous_passed = True

                except AssertionError as e:
                    CONSOLE.log(f"[bold red]\[failed][reset]: {e}")
                    fails += 1
                    previous_passed = False

                except Exception as e:
                    CONSOLE.log(f"[bold red]\[crashed][reset]: {e}")
                    fails += 1
                    previous_passed = False

                previous_file = curr_module
                print("")

                # since rich "groups" the output, we need to wait for the next second, so the next isn't grouped with previous one
                now = get_time()
                to_next_sec(now)

            CONSOLE.log("[cyan][REPORT]", "-" * 50)
            CONSOLE.log(f"[bold green]\[passed]: {successes}")

            if fails > 0:
                CONSOLE.log(f"[bold red]\[failed]: {fails}")

            if skipped > 0:
                CONSOLE.log(f"[bold yellow]\[skipped]: {skipped}")
