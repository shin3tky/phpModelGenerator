# PHP Model Generator

Model class generator for PHP 7.x and MySQL 8.

## Overview

This tool automatically generates PHP model classes from MySQL's XML dump file.

Python 3 is used to convert a XML dump file.

## Required environment

- Python 3
- MySQL 8
- MySQL client tools (mysqldump)

## Usage

1. Dump your database as XML format.

```bash
$ mysqldump -u username -p --xml --no-data dbname >dump.xml
```

2. Convert from a dump file to models.

```bash
$ php gen_model.py dump.xml
```


