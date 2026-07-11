#!/usr/bin/env bash

set -euo pipefail

# -----------------------------------------------------------------------------
# Bitestream Kafka topic bootstrap
# Creates required Kafka topics after the broker becomes available.
# Safe to run multiple times: existing topics are detected and skipped.
# -----------------------------------------------------------------------------

readonly SCRIPT_NAME="$(basename "$0")"
readonly BOOTSTRAP_SERVER="${KAFKA_BOOTSTRAP_SERVER:-bitestream-kafka:29092}"
readonly TOPIC_NAME="${FOOD_DELIVERY_EVENTS_TOPIC:-food_delivery_events}"
readonly TOPIC_PARTITIONS="${FOOD_DELIVERY_EVENTS_PARTITIONS:-3}"
readonly TOPIC_REPLICATION_FACTOR="${FOOD_DELIVERY_EVENTS_REPLICATION_FACTOR:-1}"
readonly READY_BROKER_COUNT="${KAFKA_READY_BROKER_COUNT:-1}"
readonly READY_TIMEOUT_SECONDS="${KAFKA_READY_TIMEOUT_SECONDS:-60}"

# Enable ANSI colors only when stdout is a terminal.
if [[ -t 1 ]]; then
  readonly COLOR_RESET=$'\033[0m'
  readonly COLOR_RED=$'\033[0;31m'
  readonly COLOR_GREEN=$'\033[0;32m'
  readonly COLOR_YELLOW=$'\033[1;33m'
  readonly COLOR_BLUE=$'\033[0;34m'
else
  readonly COLOR_RESET=""
  readonly COLOR_RED=""
  readonly COLOR_GREEN=""
  readonly COLOR_YELLOW=""
  readonly COLOR_BLUE=""
fi

log_info() {
  printf "%s[INFO]%s %s\n" "${COLOR_BLUE}" "${COLOR_RESET}" "$*"
}

log_success() {
  printf "%s[SUCCESS]%s %s\n" "${COLOR_GREEN}" "${COLOR_RESET}" "$*"
}

log_warning() {
  printf "%s[WARNING]%s %s\n" "${COLOR_YELLOW}" "${COLOR_RESET}" "$*"
}

log_error() {
  printf "%s[ERROR]%s %s\n" "${COLOR_RED}" "${COLOR_RESET}" "$*" >&2
}

# ERR trap handler: report failing line and exit non-zero.
on_error() {
  local exit_code=$1
  local line_number=$2
  log_error "${SCRIPT_NAME} failed on line ${line_number} with exit code ${exit_code}."
  exit "${exit_code}"
}

trap 'on_error $? $LINENO' ERR

# Block until the Kafka broker accepts protocol requests.
wait_for_kafka() {
  log_info "Waiting for Kafka broker at ${BOOTSTRAP_SERVER} to become ready..."

  cub kafka-ready \
    -b "${BOOTSTRAP_SERVER}" \
    "${READY_BROKER_COUNT}" \
    "${READY_TIMEOUT_SECONDS}" >/dev/null

  log_success "Kafka broker is ready."
}

# Return 0 if the topic already exists; non-zero otherwise.
topic_exists() {
  local topic_name=$1

  kafka-topics \
    --bootstrap-server "${BOOTSTRAP_SERVER}" \
    --topic "${topic_name}" \
    --describe >/dev/null 2>&1
}

# Create a topic when missing; skip when it already exists (idempotent).
create_topic() {
  local topic_name=$1
  local partitions=$2
  local replication_factor=$3

  if topic_exists "${topic_name}"; then
    log_warning "Topic '${topic_name}' already exists. Skipping creation."
    return 0
  fi

  log_info "Creating topic '${topic_name}' with ${partitions} partitions and replication factor ${replication_factor}..."

  kafka-topics \
    --bootstrap-server "${BOOTSTRAP_SERVER}" \
    --create \
    --if-not-exists \
    --topic "${topic_name}" \
    --partitions "${partitions}" \
    --replication-factor "${replication_factor}" >/dev/null

  if ! topic_exists "${topic_name}"; then
    log_error "Topic '${topic_name}' was not found after creation."
    exit 1
  fi

  log_success "Topic '${topic_name}' created successfully."
}

# Print all topics for post-init verification.
list_topics() {
  log_info "Listing Kafka topics for verification:"

  kafka-topics \
    --bootstrap-server "${BOOTSTRAP_SERVER}" \
    --list
}

main() {
  wait_for_kafka
  create_topic "${TOPIC_NAME}" "${TOPIC_PARTITIONS}" "${TOPIC_REPLICATION_FACTOR}"
  list_topics
  log_success "Kafka topic initialization completed successfully."
}

main "$@"
