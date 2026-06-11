#!/bin/bash

PROFILE="${1:-superset}"

COMPOSE_PROFILES=$PROFILE docker compose up --build
