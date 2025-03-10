import asyncio
import shutil
import logging
from pathlib import Path
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(file_path: Path, output_path: Path):
    try:
        ext = file_path.suffix[1:] or "unknown"
        target_dir = output_path / ext
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, target_path)
        logging.info(f"Copied: {file_path} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

async def read_folder(source_path: Path, output_path: Path):
    tasks = []

    for file_path in source_path.rglob("*"):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_path))

    await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("source_path", type=Path, help="Path to the source folder")
    parser.add_argument("output_path", type=Path, help="Path to the output folder")

    args = parser.parse_args()

    source_folder = Path(args.source_path).resolve()
    output_folder = Path(args.output_path).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Source folder does not exist or is not a directory: {source_folder}")
        return


    output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)
    logging.info(f"Finished copying files from {source_folder} to {output_folder}")

if __name__ == "__main__":
    asyncio.run(main())
