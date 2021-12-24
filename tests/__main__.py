import time
import importlib
from importlib import resources

from rich.console import Console

from . import __initial__

console = Console()
get_time = lambda: int(time.time())


def to_next_sec(prev_timestamp: int) -> int:
    timestamp = get_time()
    while timestamp <= prev_timestamp:
        timestamp = get_time()
    return timestamp


if __name__ == "__main__":
    __initial__.__init__()

    files = resources.contents("tests")
    files = [file[:-3] for file in files if file.endswith(".py") and not file.startswith("_")]

    for file in files:
        module = importlib.import_module(f"tests.{file}")

    from .__loader import tests

    tests = sorted(tests, key=lambda x: (x[0], x[1]))

    print("-" * 50)
    with console.status(f"[bold green]Running tests...", spinner="line") as status:
        fails = 0
        successes = 0
        skipped = 0

        previous_passed = True
        previous_file = None

        for file_order, order, function in tests:
            console.log(f"[Running]: {function.__doc__}")
            log = lambda *args, **kwargs: console.log(*args, **kwargs)
            curr_module = function.__module__.split(".")[-1]

            if order > 1 and previous_file == curr_module and not previous_passed:
                console.log(f"[bold yellow]\[skipped]")
                print("")
                skipped += 1
                continue

            try:
                returned = function(log)

                console.log(f"[bold green]\[passed]")
                if returned is not None:
                    console.log(f"[Returned]: {returned}")

                successes += 1
                previous_passed = True

            except AssertionError as e:
                console.log(f"[bold red]\[failed]")
                fails += 1
                previous_passed = False

            except Exception as e:
                console.log(f"[bold red]\[crashed][reset]: {e}")
                fails += 1
                previous_passed = False

            previous_file = curr_module
            print("")

            # since rich "groups" the output, we need to wait for the next second, so the next isn't grouped with previous one
            now = get_time()
            to_next_sec(now)

        console.log("[cyan][REPORT]", "-" * 50)
        console.log(f"[bold green]\[passed]: {successes}")

        if fails > 0:
            console.log(f"[bold red]\[failed]: {fails}")

        if skipped > 0:
            console.log(f"[bold yellow]\[skipped]: {skipped}")
