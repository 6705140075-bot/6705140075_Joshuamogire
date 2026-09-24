# Assignment 03 — CHANGES

**Name:** Joshua Mogire Kibwage  
**Student ID:** 6705140075

## 1 · What I changed

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products were stored as bare tuples containing the name, price, and category. | Created a `Product` class with `name`, `price`, and `category` attributes and a `tax_rate()` method. | Classes, encapsulation | Ran the self-test and checked that the output matched the legacy output. |
| 2 | Order items were stored as tuples containing a product index and quantity. | Created an `OrderItem` class that has a `Product` object and a validated quantity. | Composition, encapsulation | Checked line totals and ran the self-test. |
| 3 | Membership discounts and points used repeated `if tier == ...` chains. | Created `Customer`, `SilverCustomer`, `GoldCustomer`, and `PlatinumCustomer` classes with overridden discount and points behaviour. | Inheritance, polymorphism | Checked each tier and ran the self-test until it printed `PASS`. |
| 4 | The original calculation function printed receipts while calculating values and used a global tax variable. | Created pure methods such as `subtotal()`, `discount()`, `tax()`, `total()`, and `points()`. Receipt text is built separately in `receipt()`. | Separation of responsibilities, pure methods | Compared the complete captured output with the original `GOLDEN_OUTPUT`. |
| 5 | Magic numbers and unvalidated data were used throughout the program. | Added named constants and constructor validation for product values, quantities, customers, and orders. | Encapsulation, clean code | Checked invalid constructor values and ran the unchanged-output self-test. |

## 2 · Short reflection

The biggest improvement was replacing the repeated membership-tier `if/elif` chains with a family of customer classes. This makes the discount and points rules easier to understand and allows each tier to provide its own behaviour through polymorphism. Composition also improved the design because an order contains a customer and order items, while each order item contains a product. Keeping the behaviour identical required careful attention to the original tax rules, discount threshold, bulk discount condition, rounding, and receipt formatting. I verified the refactor by comparing the captured refactored output with the original golden output.

## 3 · Prompt log (Level 2 — required)

**Important:** Edit this table so it accurately reflects the prompts you actually used with AI.

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | I provided the Assignment 03 requirements and original Python code and asked for help completing the OOP refactor and written changes explanation. | Suggested classes for products, order items, customers, and orders; tier subclasses; named constants; validation; and separate calculation methods. | Edited and reviewed | Ran the Python self-test and checked the output against the original behaviour. |
| 2 | I asked for help explaining the changes in the `CHANGES.md` file. | Suggested a table describing the original code smell, refactored design, OOP concept, and verification method. | Edited | Read the explanation and compared each row with the submitted code. |
| 3 | I asked for help checking that the refactored code preserved the original output. | Suggested using the existing output-capture and golden-output comparison. | Accepted and reviewed | Ran the program and checked for `PASS`. |

## Ownership statement

By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.
