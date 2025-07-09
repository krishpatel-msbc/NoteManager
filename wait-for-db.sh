#!/bin/sh
set -e

echo "Using host: $1"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "POSTGRES_DB: $POSTGRES_DB"

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -U "$POSTGRES_USER"; do
  >&2 echo "⏳ PostgreSQL is unavailable - waiting..."
  sleep 1
done

>&2 echo "✅ PostgreSQL is up - executing command"
exec $cmd