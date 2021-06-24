# Search Application
This is an application which enables for user to search users and tickets with term and value.


## Environment
* Python
* Recommended python version - 3.9
* test framework - pytest
* type checking - mypy
* typing

## How to install packages

```bash
$ pip install -r requirements-dev.txt
```

## How to run test

```bash
$ pytest
```

## How to run type checking

```bash
$ mypy .
```

## Design models
* UserRepo
* TicketRepo
* SearchService
* CommandHandler


## Assumptions
* _id of users and tickets are unique as primary key
* Optional fields:
    * User: verified
    * Ticket: type, assignee_id
* Empty string will be used to search missing values
* Full value matching and case-insensitive searching


## Design decisions



## Trade offs
| what | cons | pros |
|---|---|---|
||||


## Limitations
