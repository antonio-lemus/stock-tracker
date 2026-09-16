# Automated Market Data & Notification Bot

## Overview
This repository contains an automated stock market tracking script hosted on a continuous integration pipeline. Built with Python, it utilizes the `yfinance` API to extract and parse live financial data (such as QQQM metrics) and pushes real-time custom alerts directly to a mobile device via the Telegram Bot API. The entire process is automated and scheduled using GitHub Actions.

## Tech Stack
* **Language:** Python
* **APIs:** yfinance, Telegram Bot API
* **DevOps / CI:** GitHub Actions

## Features
* Live market data extraction and analysis.
* Automated daily execution via GitHub Actions cron scheduling.
* Real-time mobile notifications and custom alerts sent through Telegram.
