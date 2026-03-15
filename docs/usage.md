# Usage Guide

This guide provides step-by-step instructions for using the Autonomous Retail Forecasting and Inventory Optimization Engine.

## API Endpoints

* **/forecast**: Generates a forecast for sales and demand
* **/optimize**: Optimizes inventory levels based on forecasted demand
* **/api-docs**: Provides API documentation

## API Request Examples

* **Forecast**: `curl -X POST -H 'Content-Type: application/json' -d '{"date": "2023-03-01"}' http://localhost:5000/forecast`
* **Optimize**: `curl -X POST -H 'Content-Type: application/json' -d '{"date": "2023-03-01", "inventory": 100}' http://localhost:5000/optimize`

## Response Formats

* **JSON**: The API responds with JSON data by default
* **CSV**: The API can respond with CSV data by specifying the `Accept` header as `text/csv`

## Error Handling

* **Error codes**: The API returns standard HTTP error codes for errors
* **Error messages**: The API returns descriptive error messages for errors
