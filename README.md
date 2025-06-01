<!-- omit in toc -->
## Languages
[![python](https://img.shields.io/badge/python-3.11-d6123c?color=white&labelColor=d6123c&logo=python&logoColor=white)](https://www.python.org/)

<!-- omit in toc -->
## Frameworks
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.41-d6123c?color=white&labelColor=d6123c&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.115.12-d6123c?color=white&labelColor=d6123c&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![aiokafka](https://img.shields.io/badge/aiokafka-0.12.0-d6123c?color=white&labelColor=d6123c&logo=apachekafka&logoColor=white)](https://aiokafka.readthedocs.io/)
[![rossmann-oltp](https://img.shields.io/badge/rossmann--oltp-d6123c?color=white&labelColor=d6123c)](https://github.com/your-org/rossmann-oltp)
[![rossmann-users-db](https://img.shields.io/badge/rossmann--users--db-d6123c?color=white&labelColor=d6123c)](https://github.com/your-org/rossmann-users-db)

<!-- omit in toc -->
## Services
[![docker](https://img.shields.io/badge/docker-d6123c?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![redis](https://img.shields.io/badge/redis-d6123c?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

<!-- omit in toc -->
## Table of Contents
- [Introduction](#introduction)
- [Project workflow](#project-workflow)
- [Docker Containers](#docker-containers)
- [Redis](#redis)
- [Kafka producer](#kafka-producer)
- [Website (Created by ellie25v)](#website-created-by-ellie25v)
- [Getting Started](#getting-started)
- [Next Section of the Project](#next-section-of-the-project)

## Introduction
🟢 **This is part 5 of 7 Docker sections in the 🔴 [Supermarket Simulation Project](https://github.com/SerhiiDolhopolov/rossmann_services).**

🔵 [**<- Previous part with Users DB.**](https://github.com/SerhiiDolhopolov/rossmann_users_db)

## Project workflow
This section contains an API to work with General OLTP DB and Users DB and Redis for cache and working with approximate users count.
Also this section contains a link to website with frontend.

## Docker Containers
**This Docker section includes:**
  - **Redis**
    - Connection URL for Redis insight
      - [redis://default@redis:6379](redis://default@redis:6379)
  - **Redis insight** to view Redis databases. 
    - 🌐 Web interface: 
      - [localhost:1501](http://localhost:1501)
  - **API**
    - 🌐 Web interface:
      - [localhost:1300](http://localhost:1300)
  - **Website** [(Created by ellie25v)](https://github.com/ellie25v/rossmann-web)
    - 🌐 Web interface:
      - [https://ellie25v.github.io/rossmann-web/](https://ellie25v.github.io/rossmann-web/)

## Redis
Thanks to the HyperLogLog Redis data type, you can count the number of users by IP with a small amount of memory usage and cache product pages.

## Kafka producer
The Kafka producer is also implemented via aiokafka. The Kafka producer sends messages with updated product data to local shops.

## Website [(Created by ellie25v)](https://github.com/ellie25v/rossmann-web)
See more details about the website [here](https://github.com/ellie25v/rossmann-web).

## Getting Started
**To start:**
1. Complete all steps in the [first part](https://github.com/SerhiiDolhopolov/rossmann_services).
2. Run the services:
```bash
docker compose up --build
```

## Next Section of the Project

[Rossmann Airflow](https://github.com/SerhiiDolhopolov/rossmann_airflow.git)