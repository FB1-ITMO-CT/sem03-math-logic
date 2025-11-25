import glob
import subprocess
import asyncio as aio
from pathlib import Path
import os
import shutil


async def build_main(base_path: Path, result_path: Path):
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

    os.makedirs(str(result_path), exist_ok=True)

    for target, ret in zip(targets, returns):
        if ret != 0:
            continue

        _ = shutil.copyfile(
            str(Path("./.build") / target.with_suffix(".pdf").name),
            result_path / target.with_suffix(".pdf").name,
        )


async def build_lections():
    base_path = Path("./lections_source")
    result_path = Path("./lections_pdf")

    await build_main(base_path, result_path)


async def build_homework():
    base_path = Path("./homework")
    result_path = Path("./homework")

    await build_main(base_path, result_path)


async def build_colloqs():
    base_path = Path("./colloqs")
    result_path = Path("./colloqs")

    await build_main(base_path, result_path)


async def main():
    _ = await aio.gather(build_lections(), build_homework(), build_colloqs())


if __name__ == "__main__":
    aio.run(main())
