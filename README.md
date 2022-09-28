# Aggregating Apache HTTP access logs

This is a simple example of how to aggregate Apache HTTP access logs; in this case, we're counting the number of accesses per status code per minute.

The module code is all in [access_logs](access_logs).

## Running the example

The demo is built into the Docker image. To run it, first build the image:

```bash
docker build -t access-logs .
```

Then run the image:
```bash
docker run -it \
    --mount src="$(src_dir)",target=/data/src,type=bind \
    --mount src="$(dest_dir)",target=/data/dest,type=bind \
    access-logs
```

The `src_dir` and `dest_dir` variables should be set to the paths of the directories containing the source and destination files, respectively. The source files should have a `.log` suffix; the destination files will be created with a mirrored directory structure and a `.csv` suffix.

For example, if the source directory looks like:
```
(src_dir)
├── 1
│   └── 2
│       └── first.log
└── a
    └── b
        └── c
            └── second.log
```

Then the destination directory will look like:
```
(dest_dir)
├── 1
│   └── 2
│       └── first
│           ├── 200.csv
│           ├── 303.csv
│           └── 404.csv
└── a
    └── b
        └── c
            └── second
                ├── 200.csv
                ├── 303.csv
                └── 404.csv
```

The actual output files look like
```
timestamp,count
2020-12-19T22:17:00,3
2020-12-19T22:18:00,1
...
```

## Running the tests

The tests are written using [pytest](https://docs.pytest.org/en/stable/). To run them you just need to be in a Poetry shell or run through poetry:
```bash
poetry run pytest
```

