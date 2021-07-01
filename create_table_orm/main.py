#!/bin/bash
# Copyright 2021 Yoshi Yamaguchi
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

from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

RFC3339 = "%Y-%m-%dT%H:%M:%SZ"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(), nullable=False)
    age = Column(Integer(), nullable=False)
    birthday = Column(DateTime(), nullable=False)
    created = Column(DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, id: int, name: str, birthday: str):
        self.id = id
        self.name = name
        self.birthday = datetime.strptime(birthday, RFC3339)
        now = datetime.utcnow()
        self.created = now
        self.age = now.year - self.birthday.year

    def __repr__(self):
        return "User(id={}, name={}, age={}, birthday={}, created={})".format(
            self.id, self.name, self.age, self.birthday, self.created
        )


def main() -> None:
    # See "Engine Configuration" for database dialects
    # https://docs.sqlalchemy.org/en/14/core/engines.html
    engine = sqlalchemy.create_engine("sqlite:///sample.db", echo=True)

    # Create all Base inherited tables
    Base.metadata.create_all(bind=engine)

    sm = sessionmaker(bind=engine)
    session = sm()

    # Insert records
    session.add(User(0, "John Doe", "1990-01-01T12:34:56Z"))
    session.add(User(1, "Taro Yamada", "1983-12-31T23:45:01Z"))
    session.commit()

    # Select all users
    result = session.query(User)
    for user in result:
        print(user)

    # Delete all records
    session.query(User).delete()
    session.commit()


if __name__ == "__main__":
    main()
