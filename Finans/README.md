# Ekonomi News Web Scraper

This project is designed to automatically scrape "Ekonomi" (Economy) category news articles from the Anadolu Agency (AA) website using Selenium. The scraped data, including the title, subtitle, and article content, is saved in both a CSV file and a text file.

## Features

- Scrapes articles from the "Ekonomi" category on the AA website.
- Saves the article title, subtitle, and content to a CSV file and a text file.
- Automatically navigates between pages and collects new articles.

## Requirements

To run this project, you need to have the following software and libraries installed:

- Python 3.x
- Selenium
- Pandas
- ChromeDriver (matching your Google Chrome version)

## Installation Guide

To run the code in this project, you'll need to install several Python modules. Below are the step-by-step instructions to get everything set up.

### 1. Install Python 3.x

Ensure that you have Python 3.x installed on your computer. You can download it from the [official Python website](https://www.python.org/downloads/).

- **Note:** During installation, make sure to check the box that says "Add Python to PATH" to ensure that Python and `pip` are accessible from the command line.

### 2. Install Required Python Modules

Once Python is installed, you can install the necessary modules using `pip`, Python's package installer.

#### Step 2.1: Open Command Prompt or Terminal

- **Windows:** Press `Win + R`, type `cmd`, and hit Enter.
- **macOS/Linux:** Open the Terminal application.

#### Step 2.2: Install Modules

The following modules need to be installed:

- **`time`:** This is a built-in Python module, so no installation is required.
- **`pandas`:** A powerful data manipulation and analysis library.
- **`os`:** A built-in Python module for interacting with the operating system, so no installation is required.
- **`selenium`:** A tool for automating web browsers.

Install these modules by running the following command:

```bash
pip install pandas selenium

## Handling Pagination and Maximum Clicks

The script is designed to navigate through multiple pages of search results, where each page contains 20 articles. The variable `max_total_clicks` controls the maximum number of pages the script will click through to load more articles.

### Calculating Maximum Clicks

- **Articles per Page:** Each page on the website contains 20 articles.
- **Total Number of Articles:** To determine how many clicks (pages) are needed, divide the total number of articles you wish to scrape by 20.

### Example Calculation

If you want to scrape 5,000 articles, you would calculate the number of pages as follows:

```python
total_articles = 5000
articles_per_page = 20
required_clicks = total_articles // articles_per_page  # This gives you the number of pages

## PKF Izmir Economic Articles Scraper

This script uses Selenium to scrape economic articles from the PKF Izmir website. It opens the website, navigates through the links to economic articles, and handles downloads and window management.

### Features

- **Automated Browser Control:** Opens and interacts with the PKF Izmir website.
- **Link Handling:** Opens each economic article link in a new tab.
- **Download Preferences:** Configures Chrome to handle downloads automatically.

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- ChromeDriver (matching your Google Chrome version)

### Installation

1. **Install Python Modules**

   Use `pip` to install the required modules. Open Command Prompt or Terminal and run:

   ```bash
   pip install selenium

