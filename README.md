# Bank Transaction Analyzer

An application for analyzing bank transactions from an Excel file. Generates JSON data for web pages, provides search services, and produces reports.

## Features

### Web Pages

- **Main page** — time-of-day greeting, card information, top 5 transactions, currency rates, and stock prices

### Services

- **Cashback categories** — top 3 categories with the highest cashback
- **Search by description** — find transactions by text (case-insensitive)
- **Search by phone number** — find transactions containing phone numbers in the description

### Reports

- **Spending by weekday** — expense distribution by day of the week
- **Working day vs. weekend spending** — comparison of weekday and weekend expenses

### Notes

Data is filtered from the beginning of the month to the specified date
Cashback is calculated as 1 ruble per 100 rubles spent
Search by description is case-insensitive
Supports various phone number formats: +7 (900) 000-00-00, 89000000000, etc.
