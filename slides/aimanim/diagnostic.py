"""diagnostic.py -- a yes/no test (or a classifier at one cutoff) in numbers.

Every slide about a binary outcome -- sick or not, positive or negative --
computes its numbers here, so slides of one film cannot disagree.
Standard library only (decision 0002). The skill `binary-diagnostics`
says what each number means and where the worked examples come from.

    from aimanim.diagnostic import Test
    t = Test.from_rates(n=10_000, sick=20, sensitivity=0.90, specificity=0.95)
    t.tp, t.fn, t.fp, t.tn      # 18, 2, 499, 9481
    t.ppv, t.lr_pos             # 0.0348, 18.0

The 2x2 table, as the slides draw it (columns = truth, rows = result):

                 sick     healthy
    positive      TP        FP        -> PPV = TP / (TP + FP)
    negative      FN        TN        -> NPV = TN / (TN + FN)
                  |         |
       sensitivity    specificity
       TP/(TP+FN)     TN/(TN+FP)
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Test:
    """Counts of one population through one test: whole people."""
    tp: int
    fn: int
    fp: int
    tn: int

    @classmethod
    def from_rates(cls, n: int, sick: int, sensitivity: float,
                   specificity: float) -> "Test":
        """`n` people, `sick` of them with the condition. Counts are
        rounded to whole people (round half to even, Python's round)."""
        healthy = n - sick
        tp = round(sick * sensitivity)
        tn = round(healthy * specificity)
        return cls(tp, sick - tp, healthy - tn, tn)

    # ---- the margins -------------------------------------------------------
    @property
    def sick(self) -> int:
        return self.tp + self.fn

    @property
    def healthy(self) -> int:
        return self.fp + self.tn

    @property
    def positive(self) -> int:
        return self.tp + self.fp

    @property
    def negative(self) -> int:
        return self.fn + self.tn

    @property
    def n(self) -> int:
        return self.sick + self.healthy

    # ---- read down the columns: the test, whoever takes it ------------------
    @property
    def sensitivity(self) -> float:
        """Share of the sick the test flags (detection rate, recall, TPR)."""
        return self.tp / self.sick

    @property
    def specificity(self) -> float:
        """Share of the healthy the test clears (TNR)."""
        return self.tn / self.healthy

    @property
    def fpr(self) -> float:
        """Share of the healthy flagged: 1 - specificity."""
        return self.fp / self.healthy

    @property
    def lr_pos(self) -> float:
        """Positive likelihood ratio: sensitivity / (1 - specificity).
        How many times a positive result multiplies the odds."""
        return self.sensitivity / self.fpr

    @property
    def lr_neg(self) -> float:
        """Negative likelihood ratio: (1 - sensitivity) / specificity."""
        return (1 - self.sensitivity) / self.specificity

    # ---- read along the rows: what a result means, HERE ---------------------
    @property
    def ppv(self) -> float:
        """Of those flagged, the share truly sick (precision)."""
        return self.tp / self.positive

    @property
    def npv(self) -> float:
        """Of those cleared, the share truly healthy."""
        return self.tn / self.negative

    # ---- the whole table ------------------------------------------------------
    @property
    def prevalence(self) -> float:
        return self.sick / self.n

    @property
    def accuracy(self) -> float:
        """Share of all calls right. Rewards a lazy test when the
        condition is rare: see `always_negative`."""
        return (self.tp + self.tn) / self.n

    @property
    def always_negative(self) -> float:
        """Accuracy of a 'test' that calls everyone healthy."""
        return self.healthy / self.n


# ---- Bayes in odds form ---------------------------------------------------------

def post_test_odds(sick: int, healthy: int, lr: float) -> tuple[float, int]:
    """Pre-test odds sick : healthy, times the likelihood ratio, as
    (sick x lr) : healthy. With the counts of a table, lr_pos gives
    TP : FP exactly -- the post-test odds ARE the flagged row."""
    return sick * lr, healthy


def one_in(p: float) -> int:
    """A probability as 'one in N', N rounded: 0.0348 -> 29."""
    return round(1 / p)


def ppv_at(prevalence: float, sensitivity: float, fpr: float) -> float:
    """PPV for any prevalence, with the test's rates held fixed:
    the curve behind 'rarer condition, more false alarms'."""
    tp = prevalence * sensitivity
    return tp / (tp + (1 - prevalence) * fpr)


def prevalence_for_ppv(ppv: float, sensitivity: float, fpr: float) -> float:
    """The prevalence at which a test of these rates has this PPV
    (ppv_at, solved for the prevalence)."""
    # ppv = p s / (p s + (1-p) f)  ->  p = ppv f / (s (1-ppv) + ppv f)
    return ppv * fpr / (sensitivity * (1 - ppv) + ppv * fpr)



def scatter(n: int, k: int, seed: int) -> list[int]:
    """Which `k` of `n` people (0-based places, sorted) are the cases,
    the same every time for one seed: two slides showing one population
    put its cases in the same places."""
    return sorted(random.Random(seed).sample(range(n), k))
