"Performance measure wrapper module"

from typing import Optional, Callable, Any
import time

from src.logging_config import logger


def measure_performance(title: Optional[str] = None) -> Callable[..., Any]:
    "Function to test performance"

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        "Decorator to add a custom title to this function"

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            "Main wrapper to run perf"

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            if title:
                logger.info("%s: Function '%s' took %f seconds to execute.", title, func.__name__, execution_time)
            else:
                logger.info("Function '%s' took %f seconds to execute.", func.__name__, execution_time)

            return result

        return wrapper

    return decorator
