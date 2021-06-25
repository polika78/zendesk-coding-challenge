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
* RepoBuilder - This builds data structure to make searchable with fields of repo data
* UserRepo - As Users Repository it stores a data structure. And it provides methods to search
* TicketRepo - As Tickets Repository it stores a data structure. And it provides methods to search
* SearchService - This implements search logics for search requests
* CommandHandler - As UI sends a command it parses a command and run it.
* Commands - It calls search service to search results and displays results
* UI - It gets commands and sends commands to command handler

## Data structure for repo
Repo data has two hashmap tables. One table stores raw data as objects with _id key. The other table is indexing table which of key is field name and value is sub hashmap table which of key is field's value and value is a list of _ids.
eg)
{
    "1": {"_id": 1, "name": "james"}
    "2": {"_id": 2, "name": "lee"}
}

{
    "name": {"james": ["1"], "lee": ["2"]}
}
This data structure gives O(n) complexity for search by using hashmap. But it requires more memory and building time and complexity compared with having list of records.


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
