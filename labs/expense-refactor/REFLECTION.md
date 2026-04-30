# Reflection

Before I changed the code, I noticed a few things that would be hard to change. The CSV reading was inside main(), so adding JSON would be annoying. The categories were also hard-coded, so if someone wanted different categories, they would have to edit the Python file. The last thing was that the math and printing were mixed together, which made it harder to test.

For Part 1, I moved the CSV and JSON reading into parse_csv and parse_json. This made the code better because both functions return the same kind of rows. After that, the rest of the code does not really need to know if the data came from a CSV or JSON file.

For Part 2, I changed the categories so they come from categories.json instead of being typed into the script. The categorize function now takes the categories as an argument. This makes it easier to change later because I can pass in a different category setup.

For Part 3, I moved the totaling logic into build_report. This was probably the most important change because build_report does not read files or print anything. It just takes rows and categories, then returns the totals. Now main() is mostly just reading the files, calling the functions, and printing the report.

The hardest part was Part 3 because the original code had everything mixed together. At first, I thought I could just copy the old totals loop into build_report, but the rows were different after using parse_csv. Once I made the rows dictionaries instead of lists, it made more sense.

If the program had to pull transactions from a remote API later, I would probably add another function that gets the API data and turns it into the same row format. I would not need to change build_report because it already works as long as the rows have date, vendor, amount, and note. I would only need to change main() so it gets the data from the API instead of the CSV file.