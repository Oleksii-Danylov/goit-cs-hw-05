'''
Напишіть Python-скрипт, який буде читати всі файли у вказаній користувачем вихідній папці (source folder) і розподіляти їх по підпапках у директорії призначення (output folder) на основі розширення файлів. Скрипт повинен виконувати сортування асинхронно для більш ефективної обробки великої кількості файлів.'''

import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile


async def read_folder(path: AsyncPath) -> None:
    async for file in path.rglob('*'):
        if file.is_file():
            await copy_file(file)


async def copy_file(file: AsyncPath) -> None:
    extension_name = file.suffix[1:]
    extension_folder = output / extension_name
    try:
        await extension_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, extension_folder / file.name)
        logging.info(f"Copied {file} to {extension_folder / file.name}")
    except Exception as e:
        logging.error(f"Failed to copy {file}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    parser = argparse.ArgumentParser(description="Sort files by extensions asynchronously.")
    parser.add_argument("source", type=str, help="Source folder")
    parser.add_argument("output", type=str, help="Output folder")
    args = parser.parse_args()
    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    asyncio.run(read_folder(source))