# -*- coding: utf-8 -*-
# Copyright 2015, 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import platform

from ._base import BaseDatabaseEngine, IncorrectDatabaseSetup


def create_engine(database_config) -> BaseDatabaseEngine:
    name = database_config["name"]

    if name == "sqlite3":
        import sqlite3
        from .sqlite import Sqlite3Engine

        return Sqlite3Engine(sqlite3, database_config)

    if name == "psycopg2":
        # pypy requires psycopg2cffi rather than psycopg2
        if platform.python_implementation() == "PyPy":
            import psycopg2cffi as psycopg2  # type: ignore
        else:
            import psycopg2  # type: ignore

        from .postgres import PostgresEngine

        return PostgresEngine(psycopg2, database_config)

    raise RuntimeError("Unsupported database engine '%s'" % (name,))


__all__ = ["create_engine", "BaseDatabaseEngine", "IncorrectDatabaseSetup"]
