#!/bin/bash

set -e

APP_NAME="${{ values.appName }}"
CHART_PATH="${{ values.chartPath }}"
NAMESPACE="${{ values.appName }}"

helm upgrade --install "$APP_NAME" "$CHART_PATH" \
  --namespace "$NAMESPACE" \
  --create-namespace \
  -f helm/values.yaml