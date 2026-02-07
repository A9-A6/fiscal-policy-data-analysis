import pandas as pd
import matplotlib.pyplot as plt
def validate_data(file_path):
    required_columns = [
        "Year",
        "Government Revenue (Billion USD)",
        "Government Spending (Billion USD)",
        "Public Debt (% of GDP)"
    ]
    df = pd.read_csv(file_path)
    print("\nChecking the dataset...")
    for column in required_columns:
        empty_count = 0
        for value in df[column]:
            if value == " ":
                empty_count += 1
        if empty_count > 0:
            print(f"{column} has {empty_count} missing values.")
        else:
            print(f"{column} has no missing values.")
    print("\nColumn Types:")
    for column in required_columns:
        print(f"{column} type is: {df[column].dtype}")
    print("\nData check completed.\n")
def analyze_revenue_expenditure(file_path):
    df = pd.read_csv(file_path).sort_values('Year')
    years = df["Year"].tolist()
    revenue = df["Government Revenue (Billion USD)"].tolist()
    spending = df["Government Spending (Billion USD)"].tolist()
    revenue_growth = [0]
    spending_growth = [0]
    for i in range(1, len(years)):
        rev_change = ((revenue[i] - revenue[i - 1]) / revenue[i - 1]) * 100
        spend_change = ((spending[i] - spending[i - 1]) / spending[i - 1]) * 100
        revenue_growth.append(rev_change)
        spending_growth.append(spend_change)
    df["Revenue Growth (%)"] = revenue_growth
    df["Spending Growth (%)"] = spending_growth
    max_rev = revenue_growth[1]
    min_rev = revenue_growth[1]
    max_rev_year = years[1]
    min_rev_year = years[1]
    max_spend = spending_growth[1]
    min_spend = spending_growth[1]
    max_spend_year = years[1]
    min_spend_year = years[1]
    for i in range(2, len(years)):
        if revenue_growth[i] > max_rev:
            max_rev = revenue_growth[i]
            max_rev_year = years[i]
        if revenue_growth[i] < min_rev:
            min_rev = revenue_growth[i]
            min_rev_year = years[i]
        if spending_growth[i] > max_spend:
            max_spend = spending_growth[i]
            max_spend_year = years[i]
        if spending_growth[i] < min_spend:
            min_spend = spending_growth[i]
            min_spend_year = years[i]
    print("\nGrowth Summary:")
    print("Highest Revenue Growth:", max_rev_year, f"({max_rev:.2f}%)")
    print("Lowest Revenue Growth:", min_rev_year, f"({min_rev:.2f}%)")
    print("Highest Spending Growth:", max_spend_year, f"({max_spend:.2f}%)")
    print("Lowest Spending Growth:", min_spend_year, f"({min_spend:.2f}%)")
    plt.figure(figsize=(10, 5))
    plt.plot(years, revenue, label='Revenue', marker='o')
    plt.plot(years, spending, label='Spending', marker='o')
    plt.title('Revenue vs Spending')
    plt.xlabel('Year')
    plt.ylabel('Billion USD')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def adding_budget(file_path):
    df = pd.read_csv(file_path)
    df["Calculated Budget Balance"] = df["Government Revenue (Billion USD)"] - df["Government Spending (Billion USD)"]
    budget_status_list = []
    color_list = []
    for balance in df["Calculated Budget Balance"]:
        if balance >= 0:
            budget_status_list.append("Surplus")
            color_list.append("green")
        else:
            budget_status_list.append("Deficit")
            color_list.append("red")
    df["Budget Status"] = budget_status_list
    df["Color"] = color_list
    deficit_years = budget_status_list.count("Deficit")
    print(f"\nAll {deficit_years} year was budget deficit.")
    plt.figure(figsize=(12, 6))
    plt.bar(df["Year"], df["Calculated Budget Balance"], color=df["Color"])
    plt.axhline(0, color='black')
    plt.title("Yearly budget balance")
    plt.xlabel("Year")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
def check_debt_status(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values("Year")
    years = df["Year"].tolist()
    debt = df["Public Debt (% of GDP)"].tolist()
    status = []
    high_risk_years = []
    for i in range(len(debt)):
        if debt[i] >= 90:
            status.append("High")
            high_risk_years.append(years[i])
        else:
            status.append("OK")
    df["Debt Status"] = status
    print("\nHigh Risk Years (Debt ≥ 90%):", len(high_risk_years))
    if high_risk_years:
        print("Years:")
        for y in high_risk_years:
            print(y)
    else:
        print("No high risk years.")
    plt.plot(years, debt, marker='o', label="Debt %")
    plt.axhline(90, color="red", linestyle="--", label="Risk Line")
    plt.title("Debt (% of GDP)")
    plt.xlabel("Year")
    plt.ylabel("Debt %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def fiscal_shocks_simple(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values("Year")
    years = df["Year"].tolist()
    revenue = df["Government Revenue (Billion USD)"].tolist()
    spending = df["Government Spending (Billion USD)"].tolist()
    print("Big changes in years:")
    for i in range(1, len(years)):
        rev_change = ((revenue[i] - revenue[i-1]) / revenue[i-1]) * 100
        spend_change = ((spending[i] - spending[i-1]) / spending[i-1]) * 100
        if rev_change < -10 or spend_change > 15:
            print(f"{years[i]} Revenue: {rev_change:.1f}%, Spending: {spend_change:.1f}%")
    plt.plot(years, revenue, label="Revenue", marker="o")
    plt.plot(years, spending, label="Spending", marker="o")
    plt.title("Changes in Revenue and Spending")
    plt.xlabel("Year")
    plt.ylabel("Amount (Billion USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def inflation_adjusted_analysis(file_path):
    df = pd.read_csv(file_path).sort_values("Year")
    if "CPI" not in df.columns:
        print("No CPI data!")
        return
    df["Real Revenue"] = df["Government Revenue (Billion USD)"] / df["CPI"] * 100
    df["Real Spending"] = df["Government Spending (Billion USD)"] / df["CPI"] * 100
    print(df[["Year", "Real Revenue", "Real Spending"]])
    plt.plot(df["Year"], df["Real Revenue"], label="Real Revenue")
    plt.plot(df["Year"], df["Real Spending"], label="Real Spending")
    plt.title("Inflation Adjusted Revenue & Spending")
    plt.legend()
    plt.tight_layout()
    plt.show()
def forecast_simple_easy(file_path, years=5):
    df = pd.read_csv(file_path)
    df = df.sort_values("Year")
    rev = df["Government Revenue (Billion USD)"].tolist()
    spend = df["Government Spending (Billion USD)"].tolist()
    yrs = df["Year"].tolist()
    if len(rev) >= 2:
        rev_avg = (rev[-1] - rev[0]) / (len(rev) - 1)
    else:
        rev_avg = 0
    if len(spend) >= 2:
        spend_avg = (spend[-1] - spend[0]) / (len(spend) - 1)
    else:
     spend_avg = 0
    future_yrs = []
    rev_forecast = []
    spend_forecast = []
    for i in range(1, years + 1):
        next_year = yrs[-1] + i
        future_yrs.append(next_year)
        next_rev = rev[-1] + rev_avg * i
        next_spend = spend[-1] + spend_avg * i
        rev_forecast.append(next_rev)
        spend_forecast.append(next_spend)
    plt.plot(yrs, rev, label="Revenue")
    plt.plot(yrs, spend, label="Spending")
    plt.plot(future_yrs, rev_forecast, "--", label="Future Revenue")
    plt.plot(future_yrs, spend_forecast, "--", label="Future Spending")
    plt.title("Simple Forecast")
    plt.xlabel("Year")
    plt.ylabel("Billion USD")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print("\nForecast (next years):")
    for i in range(years):
        print(f"{future_yrs[i]} → Revenue: {rev_forecast[i]:.1f}, Spending: {spend_forecast[i]:.1f}")
def easy_sector_spending(file_path, year):
    df = pd.read_csv(file_path)
    df = df[df["Year"] == year]
    if df.empty:
        print("That year is not in the file.")
        return
    health = df["Health Spending"].values[0]
    education = df["Education Spending"].values[0]
    defense = df["Defense Spending"].values[0]
    names = ["Health", "Education", "Defense"]
    values = [health, education, defense]
    print(f"\nSpending in {year}:")
    print(f"Health: {health} B")
    print(f"Education: {education} B")
    print(f"Defense: {defense} B")
    plt.pie(values, labels=names, autopct="%1.1f%%")
    plt.title(f"{year} Spending")
    plt.show()
def simple_gdp_check(file_path):
    df = pd.read_csv(file_path)
    years = df["Year"].tolist()
    gdp = df["GDP (Billion USD)"].tolist()
    revenue = df["Government Revenue (Billion USD)"].tolist()
    spending = df["Government Spending (Billion USD)"].tolist()
    print("\nGDP and budget comparison:")
    for i in range(1, len(gdp)):
        print(f"\n{years[i]}:")
        if gdp[i] > gdp[i - 1]:
            print("GDP went up.")
        else:
            print("GDP went down.")
        if revenue[i] > revenue[i - 1]:
            print("Revenue increased.")
        else:
            print("Revenue decreased.")
        if spending[i] > spending[i - 1]:
            print("Spending increased.")
        else:
            print("Spending decreased.")
    plt.figure(figsize=(10, 6))
    plt.plot(years, gdp, label="GDP", marker="o")
    plt.plot(years, revenue, label="Revenue", marker="o")
    plt.plot(years, spending, label="Spending", marker="o")
    plt.title("GDP, Revenue and Spending")
    plt.xlabel("Year")
    plt.ylabel("Billion USD")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
file_path1 = "fiscal_policy_extended_1970_2023.csv"
answer = input(" (yes/no): ").lower()
if answer == "yes":
    print("\nChoose an option:")
    print("1. Validate Dataset")
    print("2. Revenue & Spending Analysis")
    print("3. Budget Balance Analysis")
    print("4. Debt-to-GDP Analysis")
    print("5. Sharp Revenue/Spending Changes")
    print("6. Inflation Adjusted Analysis")
    print("7. Forecast Revenue & Expenditure")
    print("8.Categorize expenditure")
    print("9.Fiscal correlation analysis")
    choice = int(input("Enter choice (1–9): "))
    if choice == 1:
        validate_data(file_path1)
    elif choice == 2:
        analyze_revenue_expenditure(file_path1)
    elif choice == 3:
        adding_budget(file_path1)
    elif choice == 4:
        check_debt_status(file_path1)
    elif choice == 5:
        fiscal_shocks_simple(file_path1)
    elif choice == 6:
        inflation_adjusted_analysis(file_path1)
    elif choice == 7:
        forecast_simple_easy(file_path1, years=5)
    elif choice == 8:
        selected_year = int(input("Enter the year to analyze sector spending: "))
        easy_sector_spending(file_path1, selected_year)
    elif choice == 9:
        simple_gdp_check(file_path1)
    else:
        print("Invalid main menu choice.")
else:
    print("Program exited.")











































































































































































































































































































































































