# Model selection

## The question

The model predicts whether a customer is likely to churn (leave the service).
A false negative may cause the company to miss a customer who needs retention
support, while a false positive may lead to unnecessary retention efforts.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | Simple, interpretable baseline | 0.7982 | 0.4948 | 0.2500 (one-year, two-year) | 2.3177 | 3.5479 | 59becb96ed1a49c0b0250a2169369c71 |
| Random Forest | Captures nonlinear patterns and feature interactions | 0.7589 | 0.4536 | 0.2222 (one-year) | 8.3304 | 3160.1270 | d99600a71be04a2aa997084054899d94 |
| Gradient Boosting | Tests a boosting-based tree ensemble | 0.7476 | 0.4167 | 0.2222 (two-year) | 2.2177 | 141.6758 | 39a2df9ba2a54de98fef177ba62f123e |

## The champion

I selected Logistic Regression as the champion because it achieved the highest
AUC (0.7982) and F1 (0.4948). It was also the smallest model (3.55 KB) and
had low p95 latency (2.32 ms).

I accepted lower F1 on the one-year and two-year contract slices (0.25 each).
Random Forest performed better on the two-year slice (0.3636), while Gradient
Boosting performed better on the one-year slice (0.4444). These differences
need further investigation before production use.

## My promotion rules

- Latency budget (p95): 25 ms, because the prediction API should remain responsive
  and the budget leaves room for deployment overhead and future growth.
- Minimum gain to replace the champion (F1 points): 0.01, because a candidate
  must improve F1 by at least one absolute percentage point to justify replacing
  the current champion and avoid promotions based on tiny metric fluctuations.

## What I would check next

I would investigate the number of customers in each contract slice and evaluate
the model on newer data. Small slices or changes in customer behavior may make
the current results unreliable in production.
