from pathlib import Path
import sys

def get_module_name(frame) -> str:
    work_dir = Path.cwd().parts
    file_dir = Path(frame.f_code.co_filename).parts
    i = 0
    while i < len(work_dir) and i < len(file_dir) and work_dir[i] == file_dir[i]:
        i += 1
    
    ret = file_dir[i:]

    return "/".join(ret)

# thread 'main' (5400) panicked at src\main.rs:2:13:
# attempt to divide by zero
# note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
# error: process didn't exit successfully: `target\debug\rust-test.exe` (exit code: 101)
def rust_error_handler(exc_type, exc_value, exc_traceback):
    tb = exc_traceback
    while tb.tb_next:
        tb = tb.tb_next
    
    line = tb.tb_lineno
    frame = tb.tb_frame
    module = get_module_name(frame)

    print(f"process panicked at {module}:{line}:", file=sys.stderr)
    print(f"{str(exc_value)}", file=sys.stderr)
    print(f"\033[1;31merror\033[0m: process didn't exit successfully: `{module}`", file=sys.stderr)

sys.excepthook = rust_error_handler