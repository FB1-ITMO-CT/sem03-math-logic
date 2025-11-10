import glob
import subprocess
import asyncio as aio
from pathlib import Path
import os
import shutil


async def build_lections():
    base_path = Path("./lections_source")
    result_path = Path("./lections_pdf")

    targets = [Path(f) for f in glob.glob(str(base_path / "*.tex"))]
    print(f"Building {len(targets)} files:\n{'\n'.join(map(str, targets))}")

    procs = await aio.gather(
        *[
            aio.subprocess.create_subprocess_shell(
                f"lualatex.exe -synctex=1 --output-directory=.build --aux-directory=.build/.aux {file}",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            for file in targets
        ]
    )

    returns = await aio.gather(*[proc.wait() for proc in procs])

    print(f"Return codes: {' '.join(map(str, returns))}")

    shutil.rmtree(result_path)
    os.makedirs(str(result_path), exist_ok=True)

    for target, ret in zip(targets, returns):
        if ret != 0:
            continue

        _ = shutil.copyfile(
            str(Path("./.build") / target.with_suffix(".pdf").name),
            result_path / target.with_suffix(".pdf").name,
        )


def build_homework():
    pass


def build_colloqs():
    pass


async def main():
    await build_lections()


if __name__ == "__main__":
    aio.run(main())
