# ch1-exercise-challenges Specification

## Purpose

TBD - created by archiving change 'create-ch1-new-challenges'. Update Purpose after archive.

## Requirements

### Requirement: Tier 1 warm-up challenges exist

The system SHALL provide two warm-up challenges at `docs/challenge/`:

- `odd-even.md` (id: 26) — Input: one integer; Output: `Even` or `Odd`; Uses `%` operator for divisibility check
- `sign-check.md` (id: 27) — Input: one integer; Output: `Positive`, `Negative`, or `Zero`; Uses comparison operators with if-elif-else

Each challenge MUST have `layout: challenge`, valid `params` with appropriate integer ranges, a correct `generator` script, and `starter_code` with a Chinese comment hint.

#### Scenario: Tier 1 generators produce correct output

- **WHEN** `odd-even` generator receives input `7`
- **THEN** output SHALL be `Odd`

- **WHEN** `odd-even` generator receives input `4`
- **THEN** output SHALL be `Even`

- **WHEN** `sign-check` generator receives input `0`
- **THEN** output SHALL be `Zero`


<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->

---
### Requirement: Tier 2 application challenges exist

The system SHALL provide two application challenges:

- `bmi-classifier.md` (id: 28) — Input: weight (kg, int), height (cm, int); Output: `Underweight` (BMI < 18.5), `Normal` (18.5-24), `Overweight` (24-27), or `Obese` (>= 27); Uses Taiwan HPA standards; BMI formula: `weight / (height/100) / (height/100)`
- `quadrant-classifier.md` (id: 29) — Input: two integers x, y; Output: one of `Origin`, `X-axis`, `Y-axis`, `Quadrant 1` through `Quadrant 4`; 7 distinct cases covering all combinations of positive, negative, and zero coordinates

Each challenge MUST have valid params, a correct generator, and starter_code.

#### Scenario: Tier 2 generators produce correct output

- **WHEN** `bmi-classifier` generator receives weight `70` and height `170`
- **THEN** output SHALL be `Normal` (BMI approximately 24.2... wait, 70/(1.7*1.7) = 70/2.89 = 24.22, which is >= 24, so `Overweight`)

- **WHEN** `quadrant-classifier` generator receives x `0` and y `0`
- **THEN** output SHALL be `Origin`

- **WHEN** `quadrant-classifier` generator receives x `-3` and y `5`
- **THEN** output SHALL be `Quadrant 2`


<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->

---
### Requirement: Tier 3 mathematical modeling challenges exist

The system SHALL provide four mathematical modeling challenges:

- `triangle-classify.md` (id: 30) — Input: three integers a, b, c; Output: `Not a Triangle`, `Equilateral`, `Isosceles`, or `Scalene`; Checks triangle inequality first, then classifies type
- `quadratic-discriminant.md` (id: 31) — Input: three integers a, b, c (coefficients of ax^2+bx+c=0, a >= 1); Output: `Two Real Roots` (D > 0), `One Repeated Root` (D == 0), or `No Real Roots` (D < 0); D = b*b - 4*a*c
- `taxi-fare.md` (id: 32) — Input: distance in meters (int); Output: fare in TWD (int); Base fare 85 TWD for first 1250m, then 5 TWD per 200m (ceiling division for partial segments)
- `movie-ticket.md` (id: 33) — Input: age (int), hour (int 0-23); Output: ticket price (int); Age-based pricing (child < 12: 150, student 12-25: 250, adult 26-64: 350, senior >= 65: 150) with early show discount (hour < 12: subtract 50)

#### Scenario: Triangle classification is correct

- **WHEN** `triangle-classify` generator receives `3 3 3`
- **THEN** output SHALL be `Equilateral`

- **WHEN** `triangle-classify` generator receives `1 2 10`
- **THEN** output SHALL be `Not a Triangle`

#### Scenario: Quadratic discriminant is correct

- **WHEN** `quadratic-discriminant` generator receives `1 -5 6`
- **THEN** output SHALL be `Two Real Roots` (D = 25-24 = 1 > 0)

- **WHEN** `quadratic-discriminant` generator receives `1 2 1`
- **THEN** output SHALL be `One Repeated Root` (D = 4-4 = 0)

#### Scenario: Taxi fare calculation is correct

- **WHEN** `taxi-fare` generator receives distance `1000`
- **THEN** output SHALL be `85` (within base distance)

- **WHEN** `taxi-fare` generator receives distance `2000`
- **THEN** output SHALL be `105` (85 + ceil(750/200)*5 = 85 + 4*5 = 105)

#### Scenario: Movie ticket pricing is correct

- **WHEN** `movie-ticket` generator receives age `15` and hour `10`
- **THEN** output SHALL be `200` (student 250 - early discount 50)


<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->

---
### Requirement: Tier 4 comprehensive challenge exists

The system SHALL provide one comprehensive challenge:

- `date-validator.md` (id: 34) — Input: year (int), month (int 0-15), day (int 0-35); Output: `Valid` or `Invalid`; Validates month range (1-12), day range per month (31 for months 1,3,5,7,8,10,12; 30 for months 4,6,9,11; 28 or 29 for month 2 depending on leap year)

The params MUST allow out-of-range month and day values to test invalid input cases.

#### Scenario: Date validation handles leap year February

- **WHEN** `date-validator` generator receives year `2024`, month `2`, day `29`
- **THEN** output SHALL be `Valid` (2024 is a leap year)

- **WHEN** `date-validator` generator receives year `1900`, month `2`, day `29`
- **THEN** output SHALL be `Invalid` (1900 is not a leap year)

#### Scenario: Date validation rejects invalid months

- **WHEN** `date-validator` generator receives year `2024`, month `13`, day `1`
- **THEN** output SHALL be `Invalid`


<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->

---
### Requirement: Module 1 comprehensive challenge exists for section 1-4

The system SHALL provide one comprehensive challenge for the Module 1 summary:

- `vending-change.md` (id: 35) — Input: price (int), payment (int); Output: `Insufficient` if payment < price, otherwise four space-separated integers representing coin counts for 50, 10, 5, and 1 TWD denominations using greedy decomposition

#### Scenario: Vending change with sufficient payment

- **WHEN** `vending-change` generator receives price `30` and payment `100`
- **THEN** output SHALL be `1 2 0 0` (change 70 = 1x50 + 2x10)

#### Scenario: Vending change with insufficient payment

- **WHEN** `vending-change` generator receives price `200` and payment `100`
- **THEN** output SHALL be `Insufficient`

#### Scenario: Vending change with exact payment

- **WHEN** `vending-change` generator receives price `100` and payment `100`
- **THEN** output SHALL be `0 0 0 0`


<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->

---
### Requirement: All challenges use only Module 1 Python constructs

All challenge generators and their intended student solutions SHALL use only Python constructs taught in Module 1: `input()`, `int()`, `float()`, `print()`, variables, arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`), comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`), logical operators (`and`, `or`, `not`), and `if-elif-else` statements. Generators MAY use additional Python features (e.g., `in` operator, tuples) since generator code is hidden from students.

#### Scenario: Student-facing constructs are Module 1 only

- **WHEN** a challenge's `starter_code` comment describes the expected approach
- **THEN** the described approach SHALL be achievable using only Module 1 constructs

<!-- @trace
source: create-ch1-new-challenges
updated: 2026-04-10
code:
  - docs/challenge/taxi-fare.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/odd-even.md
  - docs/challenge/sign-check.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/vending-change.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
-->