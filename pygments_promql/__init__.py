# -*- coding: utf-8 -*-
"""
    pygments.lexers.promql
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Prometheus Query Language.

    :copyright: Copyright 2006-2020 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, default, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)

__all__ = ["PromQLLexer"]


class PromQLLexer(RegexLexer):
    """
    For `PromQL <https://prometheus.io/docs/prometheus/latest/querying/basics/>`_ queries.

    For details about the grammar see:
    https://github.com/prometheus/prometheus/tree/master/promql/parser
    """

    name = "PromQL"
    aliases = ["promql"]
    filenames = ["*.promql"]

    base_keywords = (
        words(
            (
                "bool",
                "by",
                "group_left",
                "group_right",
                "ignoring",
                "offset",
                "on",
                "without",
            ),
            suffix=r"\b",
        ),
        Keyword,
    )

    aggregator_keywords = (
        words(
            (
                "sum",
                "min",
                "max",
                "avg",
                "group",
                "stddev",
                "stdvar",
                "count",
                "count_values",
                "bottomk",
                "topk",
                "quantile",
            ),
            suffix=r"\b",
        ),
        Keyword,
    )

    function_keywords = (
        words(
            (
                "abs",
                "absent",
                "absent_over_time",
                "avg_over_time",
                "ceil",
                "changes",
                "clamp_max",
                "clamp_min",
                "count_over_time",
                "day_of_month",
                "day_of_week",
                "days_in_month",
                "delta",
                "deriv",
                "exp",
                "floor",
                "histogram_quantile",
                "holt_winters",
                "hour",
                "idelta",
                "increase",
                "irate",
                "label_join",
                "label_replace",
                "ln",
                "log10",
                "log2",
                "max_over_time",
                "min_over_time",
                "minute",
                "month",
                "predict_linear",
                "quantile_over_time",
                "rate",
                "resets",
                "round",
                "scalar",
                "sort",
                "sort_desc",
                "sqrt",
                "stddev_over_time",
                "stdvar_over_time",
                "sum_over_time",
                "time",
                "timestamp",
                "vector",
                "year",
            ),
            suffix=r"\b",
        ),
        Keyword.Reserved,
    )

    tokens = {
        "root": [
            (r"\n", Whitespace),
            (r"\s+", Whitespace),
            (r"//.*?\n", Comment.Single),
            (r",", Punctuation),
            # Keywords
            base_keywords,
            aggregator_keywords,
            function_keywords,
            # Numbers
            (r"-?[0-9]+\.[0-9]+", Number.Float),
            (r"-?[0-9]+", Number.Integer),
            # Comments
            (r"#.*?$", Comment.Single),
            # Operators
            (r"(\+|\-|\*|\/|\%|\^)", Operator),
            (r"==|!=|>=|<=|<|>", Operator),
            (r"and|or|unless", Operator.Word),
            # Metrics
            (r"[_a-zA-Z][_a-zA-Z0-9]+", Name.Variable),
            # Params
            (r'["\'].*?["\']', String),
            # Other states
            (r"\(", Operator, "function"),
            (r"\)", Operator),
            (r"{", Punctuation, "labels"),
            (r"\[", Punctuation, "range"),
        ],
        "labels": [
            (r"}", Punctuation, "#pop"),
            (r"\n", Whitespace),
            (r"\s+", Whitespace),
            (r",", Punctuation),
            (
                r'([_a-zA-Z][_a-zA-Z0-9]*?)(\s*?)(=|!=|=~|~!)(\s*?)(".*?")',
                bygroups(Name.Label, Whitespace, Operator, Whitespace, String),
            ),
        ],
        "range": [
            (r"\]", Punctuation, "#pop"),
            (r"([1-9][0-9]*?)(s|m|h|d|w|y)", bygroups(String, String)),
        ],
        "function": [
            (r"\)", Operator, "#pop"),
            (r"\(", Operator, "#push"),
            default("#pop"),
        ],
    }
