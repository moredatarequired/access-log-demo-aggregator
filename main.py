import asyncio

from access_logs.group_and_count import aggregate_from_dir

if __name__ == "__main__":
    asyncio.run(aggregate_from_dir("/data/src", "/data/dest"))
