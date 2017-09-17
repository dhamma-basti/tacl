#!/usr/bin/env python3

import io
import os
import unittest

import tacl
from .tacl_test_case import TaclTestCase


class ResultsTestCase (TaclTestCase):

    def setUp(self):
        self._tokenizer = tacl.Tokenizer(
            tacl.constants.TOKENIZER_PATTERN_CBETA,
            tacl.constants.TOKENIZER_JOINER_CBETA)

    def test_add_label_count(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit1', '5', 'A'],
            ['AB', '2', 'b', 'base', '3', 'A'],
            ['AB', '2', 'b', 'wit1', '3', 'A'],
            ['AB', '2', 'c', 'base', '2', 'B'],
            ['BC', '2', 'a', 'base', '2', 'A']
        )
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.add_label_count()
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A', '8'),
            ('AB', '2', 'a', 'wit1', '5', 'A', '8'),
            ('AB', '2', 'b', 'base', '3', 'A', '8'),
            ('AB', '2', 'b', 'wit1', '3', 'A', '8'),
            ('AB', '2', 'c', 'base', '2', 'B', '2'),
            ('BC', '2', 'a', 'base', '2', 'A', '2')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_add_label_work_count(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit1', '2', 'A'],
            ['AB', '2', 'b', 'base', '1', 'A'],
            ['AB', '2', 'c', 'base', '2', 'B'],
            ['BC', '2', 'a', 'base', '0', 'A'],
            ['BC', '2', 'a', 'wit1', '0', 'A'],
            ['CD', '2', 'a', 'base', '1', 'A']
        )
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.add_label_work_count()
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A', '2'),
            ('AB', '2', 'a', 'wit1', '2', 'A', '2'),
            ('AB', '2', 'b', 'base', '1', 'A', '2'),
            ('AB', '2', 'c', 'base', '2', 'B', '1'),
            ('BC', '2', 'a', 'base', '0', 'A', '0'),
            ('BC', '2', 'a', 'wit1', '0', 'A', '0'),
            ('CD', '2', 'a', 'base', '1', 'A', '1')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_bifurcated_extend(self):
        self.maxDiff = None
        # This is a test of Results._bifurcated_extend, which does not
        # require any information other than the results themselves.
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A', '7'],
            ['AB', '2', 'a', 'wit1', '5', 'A', '7'],
            ['AB', '2', 'b', 'base', '2', 'A', '7'],
            ['AB', '2', 'c', 'base', '4', 'B', '4'],
            ['ZAB', '3', 'a', 'base', '2', 'A', '3'],
            ['ZAB', '3', 'a', 'wit1', '2', 'A', '3'],
            ['ZAB', '3', 'b', 'base', '1', 'A', '3'],
            ['ABC', '3', 'a', 'base', '4', 'A', '5'],
            ['ABC', '3', 'a', 'wit1', '4', 'A', '5'],
            ['ABC', '3', 'b', 'base', '1', 'A', '5'],
            ['ABC', '3', 'c', 'base', '4', 'B', '4'],
            ['ZAB', '3', 'c', 'base', '2', 'B', '2'],
            ['XAB', '3', 'c', 'base', '2', 'B', '2'],
            ['ZABC', '4', 'a', 'base', '2', 'A', '2'],
            ['ZABC', '4', 'a', 'wit1', '2', 'A', '2'],
            ['ZABCD', '5', 'a', 'base', '1', 'A', '1'],
            ['ZABCD', '5', 'a', 'wit1', '1', 'A', '1'],
            ['ZABCDE', '6', 'a', 'base', '1', 'A', '1'],
        )
        fieldnames = tacl.constants.QUERY_FIELDNAMES + \
            [tacl.constants.LABEL_COUNT_FIELDNAME]
        fh = self._create_csv(input_data, fieldnames=fieldnames)
        results = tacl.Results(fh, self._tokenizer)
        results._bifurcated_extend()
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A', '7'),
            ('AB', '2', 'a', 'wit1', '5', 'A', '7'),
            ('AB', '2', 'b', 'base', '2', 'A', '7'),
            ('ZAB', '3', 'a', 'base', '2', 'A', '3'),
            ('ABC', '3', 'a', 'base', '4', 'A', '5'),
            ('ZAB', '3', 'a', 'wit1', '2', 'A', '3'),
            ('ABC', '3', 'a', 'wit1', '4', 'A', '5'),
            ('ZAB', '3', 'b', 'base', '1', 'A', '3'),
            ('ABC', '3', 'b', 'base', '1', 'A', '5'),
            ('ABC', '3', 'c', 'base', '4', 'B', '4'),
            ('ZAB', '3', 'c', 'base', '2', 'B', '2'),
            ('XAB', '3', 'c', 'base', '2', 'B', '2'),
            ('ZABC', '4', 'a', 'base', '2', 'A', '2'),
            ('ZABC', '4', 'a', 'wit1', '2', 'A', '2'),
            ('ZABCD', '5', 'a', 'base', '1', 'A', '1'),
            ('ZABCD', '5', 'a', 'wit1', '1', 'A', '1'),
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_collapse_witnesses(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit 1', '4', 'A'],
            ['AB', '2', 'a', 'wit 2', '3', 'A'],
            ['AB', '2', 'b', 'base', '4', 'A'],
            ['AB', '2', 'b', 'wit 1', '3', 'A'],
            ['BC', '2', 'a', 'base', '4', 'A'],
            ['BC', '2', 'a', 'wit 1', '3', 'A'],
            ['BC', '2', 'a', 'wit 2', '3', 'A'],
        )
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.collapse_witnesses()
        expected_rows = [
            ('AB', '2', 'a', 'base "wit 1"', '4', 'A'),
            ('AB', '2', 'a', '"wit 2"', '3', 'A'),
            ('AB', '2', 'b', 'base', '4', 'A'),
            ('AB', '2', 'b', '"wit 1"', '3', 'A'),
            ('BC', '2', 'a', 'base', '4', 'A'),
            ('BC', '2', 'a', '"wit 1" "wit 2"', '3', 'A'),
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_is_intersect_results(self):
        # Test that _is_intersect_results correctly identifies diff
        # and intersect results.
        intersect_results = (
            ['AB', '2', 'a', 'base', '7', 'A'],
            ['AB', '2', 'b', 'base', '2', 'B'],
            ['AB', '2', 'c', 'base', '5', 'C'])
        fh = self._create_csv(intersect_results)
        results = tacl.Results(fh, self._tokenizer)
        self.assertTrue(results._is_intersect_results(results._matches))
        diff_results = (
            ['AB', '2', 'a', 'base', '7', 'A'],
            ['AB', '2', 'a', 'other', '1', 'A'],
            ['AB', '2', 'b', 'base', '5', 'A'],
            ['BA', '2', 'c', 'base', '2', 'B'])
        fh = self._create_csv(diff_results)
        results = tacl.Results(fh, self._tokenizer)
        self.assertFalse(results._is_intersect_results(results._matches))

    def test_prune_by_ngram(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'],
            ['ABD', '3', 'a', 'wit', '1', 'A'],
            ['ABCD', '4', 'a', 'base', '2', 'A'],
            ['AB', '2', 'b', 'base', '2', 'A'],
            ['ABC', '3', 'b', 'wit', '2', 'A'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        ngrams = ['AB', 'ABD']
        results.prune_by_ngram(ngrams)
        expected_rows = [
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('ABCD', '4', 'a', 'base', '2', 'A'),
            ('ABC', '3', 'b', 'wit', '2', 'A')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_prune_by_ngram_count(self):
        input_data = (
            ['AB', '2', 'a', 'base', '7', 'A'],
            ['BA', '2', 'a', 'wit', '1', 'A'],
            ['BA', '2', 'b', 'base', '3', 'B'],
            ['BA', '2', 'b', 'wit', '3', 'B'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count(minimum=3)
        expected_rows = [
            ('AB', '2', 'a', 'base', '7', 'A'),
            ('BA', '2', 'a', 'wit', '1', 'A'),
            ('BA', '2', 'b', 'base', '3', 'B'),
            ('BA', '2', 'b', 'wit', '3', 'B')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count(maximum=4)
        expected_rows = [('BA', '2', 'a', 'wit', '1', 'A'),
                         ('BA', '2', 'b', 'base', '3', 'B'),
                         ('BA', '2', 'b', 'wit', '3', 'B')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count(minimum=4, maximum=5)
        expected_rows = [('BA', '2', 'a', 'wit', '1', 'A'),
                         ('BA', '2', 'b', 'base', '3', 'B'),
                         ('BA', '2', 'b', 'wit', '3', 'B')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_prune_by_ngram_count_empty_results(self):
        input_data = ()
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count(minimum=3)
        expected_rows = []
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_prune_by_ngram_count_per_work(self):
        input_data = (
            ['AB', '2', 'a', 'base', '7', 'A'],
            ['AB', '2', 'a', 'wit', '1', 'A'],
            ['AB', '2', 'b', 'base', '1', 'B'],
            ['BA', '2', 'a', 'base', '2', 'A'],
            ['BA', '2', 'a', 'wit', '3', 'A'],
            ['BA', '2', 'b', 'base', '3', 'B'],
            ['BA', '2', 'b', 'wit', '1', 'B'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count_per_work(minimum=3)
        expected_rows = [
            ('AB', '2', 'a', 'base', '7', 'A'),
            ('AB', '2', 'a', 'wit', '1', 'A'),
            ('AB', '2', 'b', 'base', '1', 'B'),
            ('BA', '2', 'a', 'base', '2', 'A'),
            ('BA', '2', 'a', 'wit', '3', 'A'),
            ('BA', '2', 'b', 'base', '3', 'B'),
            ('BA', '2', 'b', 'wit', '1', 'B')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count_per_work(minimum=4)
        expected_rows = [
            ('AB', '2', 'a', 'base', '7', 'A'),
            ('AB', '2', 'a', 'wit', '1', 'A'),
            ('AB', '2', 'b', 'base', '1', 'B')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count_per_work(maximum=3)
        expected_rows = [
            ('AB', '2', 'a', 'base', '7', 'A'),
            ('AB', '2', 'a', 'wit', '1', 'A'),
            ('AB', '2', 'b', 'base', '1', 'B'),
            ('BA', '2', 'a', 'base', '2', 'A'),
            ('BA', '2', 'a', 'wit', '3', 'A'),
            ('BA', '2', 'b', 'base', '3', 'B'),
            ('BA', '2', 'b', 'wit', '1', 'B')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_count_per_work(minimum=3, maximum=4)
        expected_rows = [
            ('BA', '2', 'a', 'base', '2', 'A'),
            ('BA', '2', 'a', 'wit', '3', 'A'),
            ('BA', '2', 'b', 'base', '3', 'B'),
            ('BA', '2', 'b', 'wit', '1', 'B')
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_prune_by_ngram_size(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'],
            ['ABD', '3', 'a', 'wit', '1', 'A'],
            ['ABCD', '4', 'a', 'base', '2', 'A'],
            ['AB', '2', 'b', 'base', '2', 'A'],
            ['ABC', '3', 'b', 'wit', '2', 'A'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_size(minimum=3)
        expected_rows = [
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('ABD', '3', 'a', 'wit', '1', 'A'),
            ('ABCD', '4', 'a', 'base', '2', 'A'),
            ('ABC', '3', 'b', 'wit', '2', 'A')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_size(maximum=3)
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A'),
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('ABD', '3', 'a', 'wit', '1', 'A'),
            ('AB', '2', 'b', 'base', '2', 'A'),
            ('ABC', '3', 'b', 'wit', '2', 'A')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_ngram_size(minimum=3, maximum=3)
        expected_rows = [
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('ABD', '3', 'a', 'wit', '1', 'A'),
            ('ABC', '3', 'b', 'wit', '2', 'A')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_prune_by_work_count(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'b', 'base', '7', 'A'],
            ['AB', '2', 'c', 'base', '1', 'B'],
            ['AB', '2', 'd', 'base', '3', 'B'],
            ['ABC', '3', 'a', 'base', '3', 'A'],
            ['ABC', '3', 'b', 'base', '5', 'A'],
            ['ABC', '3', 'c', 'base', '1', 'B'],
            ['BA', '2', 'a', 'base', '6', 'A'],
            ['B', '1', 'a', 'base', '5', 'A'],
            ['B', '1', 'b', 'base', '3', 'A'],
            ['B', '1', 'b', 'wit', '3', 'A'],
            ['B', '1', 'c', 'base', '0', 'B'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_work_count(minimum=3)
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A'),
            ('AB', '2', 'b', 'base', '7', 'A'),
            ('AB', '2', 'c', 'base', '1', 'B'),
            ('AB', '2', 'd', 'base', '3', 'B'),
            ('ABC', '3', 'a', 'base', '3', 'A'),
            ('ABC', '3', 'b', 'base', '5', 'A'),
            ('ABC', '3', 'c', 'base', '1', 'B')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_work_count(maximum=3)
        expected_rows = [
            ('ABC', '3', 'a', 'base', '3', 'A'),
            ('ABC', '3', 'b', 'base', '5', 'A'),
            ('ABC', '3', 'c', 'base', '1', 'B'),
            ('BA', '2', 'a', 'base', '6', 'A'),
            ('B', '1', 'a', 'base', '5', 'A'),
            ('B', '1', 'b', 'base', '3', 'A'),
            ('B', '1', 'b', 'wit', '3', 'A'),
            ('B', '1', 'c', 'base', '0', 'B'),
        ]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)
        fh.seek(0)
        results = tacl.Results(fh, self._tokenizer)
        results.prune_by_work_count(minimum=2, maximum=3)
        expected_rows = [
            ('ABC', '3', 'a', 'base', '3', 'A'),
            ('ABC', '3', 'b', 'base', '5', 'A'),
            ('ABC', '3', 'c', 'base', '1', 'B'),
            ('B', '1', 'a', 'base', '5', 'A'),
            ('B', '1', 'b', 'base', '3', 'A'),
            ('B', '1', 'b', 'wit', '3', 'A'),
            ('B', '1', 'c', 'base', '0', 'B')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_reciprocal_remove(self):
        input_data = (
            ['AB', '2', 'a', 'base', '5', 'A'],
            ['ABCDEF', '6', 'a', 'base', '7', 'A'],
            ['DEF', '3', 'a', 'base', '2', 'A'],
            ['GHIJ', '4', 'a', 'base', '3', 'A'],
            ['KLM', '3', 'b', 'base', '0', 'A'],
            ['ABCDEF', '6', 'b', 'base', '3', 'B'],
            ['GHIJ', '4', 'b', 'base', '2', 'B'],
            ['KLM', '3', 'b', 'base', '17', 'B'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.reciprocal_remove()
        expected_rows = [
            ('ABCDEF', '6', 'a', 'base', '7', 'A'),
            ('GHIJ', '4', 'a', 'base', '3', 'A'),
            ('ABCDEF', '6', 'b', 'base', '3', 'B'),
            ('GHIJ', '4', 'b', 'base', '2', 'B')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(set(actual_rows), set(expected_rows))
        # More than two labels, and more than one text per label.
        input_data = (
            ['AB', '2', 'a', 'base', '5', 'A'],
            ['ABCDEF', '6', 'a', 'base', '7', 'A'],
            ['DEF', '3', 'a', 'base', '2', 'A'],
            ['AB', '2', 'b', 'base', '6', 'A'],
            ['GHIJ', '4', 'b', 'base', '3', 'A'],
            ['KLM', '3', 'b', 'base', '0', 'A'],
            ['ABCDEF', '6', 'c', 'base', '3', 'B'],
            ['KLM', '3', 'c', 'base', '17', 'B'],
            ['GHIJ', '4', 'd', 'base', '2', 'B'],
            ['KLM', '3', 'e', 'base', '3', 'C'],
            ['GHIJ', '4', 'f', 'base', '11', 'C'],
            ['ABCDEF', '6', 'g', 'base', '8', 'C'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.reciprocal_remove()
        expected_rows = [
            ('ABCDEF', '6', 'a', 'base', '7', 'A'),
            ('GHIJ', '4', 'b', 'base', '3', 'A'),
            ('ABCDEF', '6', 'c', 'base', '3', 'B'),
            ('GHIJ', '4', 'd', 'base', '2', 'B'),
            ('GHIJ', '4', 'f', 'base', '11', 'C'),
            ('ABCDEF', '6', 'g', 'base', '8', 'C')]
        actual_rows = self._get_rows_from_csv(results.csv(
                io.StringIO(newline='')))
        self.assertEqual(set(actual_rows), set(expected_rows))
        # Now with variants.
        input_data = (
            ['AB', '2', 'a', 'base', '5', 'A'],
            ['ABCDEF', '6', 'a', 'wit1', '7', 'A'],
            ['DEF', '3', 'a', 'base', '2', 'A'],
            ['AB', '2', 'b', 'base', '6', 'A'],
            ['GHIJ', '4', 'b', 'base', '3', 'A'],
            ['KLM', '3', 'b', 'base', '0', 'A'],
            ['ABCDEF', '6', 'c', 'base', '3', 'B'],
            ['KLM', '3', 'c', 'base', '17', 'B'],
            ['GHIJ', '4', 'd', 'base', '2', 'B'],
            ['KLM', '3', 'e', 'base', '3', 'C'],
            ['GHIJ', '4', 'f', 'wit2', '11', 'C'],
            ['ABCDEF', '6', 'g', 'base', '8', 'C'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.reciprocal_remove()
        expected_rows = [
            ('ABCDEF', '6', 'a', 'wit1', '7', 'A'),
            ('GHIJ', '4', 'b', 'base', '3', 'A'),
            ('ABCDEF', '6', 'c', 'base', '3', 'B'),
            ('GHIJ', '4', 'd', 'base', '2', 'B'),
            ('GHIJ', '4', 'f', 'wit2', '11', 'C'),
            ('ABCDEF', '6', 'g', 'base', '8', 'C')]
        actual_rows = self._get_rows_from_csv(results.csv(
                io.StringIO(newline='')))
        self.assertEqual(set(actual_rows), set(expected_rows))

    def test_reduce_cbeta(self):
        tokenizer = self._tokenizer
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'],
            ['ABD', '3', 'a', 'base', '1', 'A'],
            ['ABCD', '4', 'a', 'base', '2', 'A'],
            ['AB', '2', 'b', 'base', '2', 'A'],
            ['ABC', '3', 'b', 'base', '2', 'A'],
            ['AB', '2', 'b', 'wit', '3', 'A'],
            ['ABC', '3', 'b', 'wit', '1', 'A'])
        expected_rows = set(
            (('AB', '2', 'a', 'base', '1', 'A'),
             ('ABD', '3', 'a', 'base', '1', 'A'),
             ('ABCD', '4', 'a', 'base', '2', 'A'),
             ('ABC', '3', 'b', 'base', '2', 'A'),
             ('AB', '2', 'b', 'wit', '2', 'A'),
             ('ABC', '3', 'b', 'wit', '1', 'A')))
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), expected_rows)
        # Overlapping n-grams are trickier. Take the intersection of
        # two texts:
        #     ABABABCABDA and ABABABEABFA
        input_data = (
            ['ABABAB', '6', 'text1', 'base', '1', 'C1'],
            ['ABABA', '5', 'text1', 'base', '1', 'C1'],
            ['BABAB', '5', 'text1', 'base', '1', 'C1'],
            ['ABAB', '4', 'text1', 'base', '2', 'C1'],
            ['BABA', '4', 'text1', 'base', '1', 'C1'],
            ['ABA', '3', 'text1', 'base', '2', 'C1'],
            ['BAB', '3', 'text1', 'base', '2', 'C1'],
            ['AB', '2', 'text1', 'base', '4', 'C1'],
            ['BA', '2', 'text1', 'base', '2', 'C1'],
            ['A', '1', 'text1', 'base', '5', 'C1'],
            ['B', '1', 'text1', 'base', '4', 'C1'])
        expected_rows = set(
            (('ABABAB', '6', 'text1', 'base', '1', 'C1'),
             ('AB', '2', 'text1', 'base', '1', 'C1'),
             ('A', '1', 'text1', 'base', '1', 'C1')))
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), expected_rows)
        # An n-gram that consists of a single repeated token is a form
        # of overlapping. Take the intersection of two texts:
        #     AAAAABAAAACAAADAAEA and AAAAAFAAAAGAAAHAAIA
        input_data = (
            ['AAAAA', '5', 'text1', 'base', '1', 'C1'],
            ['AAAA', '4', 'text1', 'base', '3', 'C1'],
            ['AAA', '3', 'text1', 'base', '6', 'C1'],
            ['AA', '2', 'text1', 'base', '10', 'C1'],
            ['A', '1', 'text1', 'base', '15', 'C1'],
            ['AAAAA', '5', 'text2', 'base', '1', 'C2'],
            ['AAAA', '4', 'text2', 'base', '3', 'C2'],
            ['AAA', '3', 'text2', 'base', '6', 'C2'],
            ['AA', '2', 'text2', 'base', '10', 'C2'],
            ['A', '1', 'text2', 'base', '15', 'C2'])
        expected_rows = set(
            (('AAAAA', '5', 'text1', 'base', '1', 'C1'),
             ('AAAA', '4', 'text1', 'base', '1', 'C1'),
             ('AAA', '3', 'text1', 'base', '1', 'C1'),
             ('AA', '2', 'text1', 'base', '1', 'C1'),
             ('A', '1', 'text1', 'base', '1', 'C1'),
             ('AAAAA', '5', 'text2', 'base', '1', 'C2'),
             ('AAAA', '4', 'text2', 'base', '1', 'C2'),
             ('AAA', '3', 'text2', 'base', '1', 'C2'),
             ('AA', '2', 'text2', 'base', '1', 'C2'),
             ('A', '1', 'text2', 'base', '1', 'C2')))
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), expected_rows)
        # If the token is more than a single character, the case is
        # even more pathological. [...] is a single token.
        #     [A][A][A]B[A][A]C[A] and [A][A][A]D[A][A]E[A]
        input_data = (
            ['[A][A][A]', '3', 'text1', 'base', '1', 'C1'],
            ['[A][A]', '2', 'text1', 'base', '3', 'C1'],
            ['[A]', '1', 'text1', 'base', '6', 'C1'])
        expected_rows = set(
            (('[A][A][A]', '3', 'text1', 'base', '1', 'C1'),
             ('[A][A]', '2', 'text1', 'base', '1', 'C1'),
             ('[A]', '1', 'text1', 'base', '1', 'C1')))
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), expected_rows)

    def test_reduce_nan(self):
        # Check that the n-gram "nan" is not interpreted as NaN.
        tokenizer = tacl.Tokenizer(tacl.constants.TOKENIZER_PATTERN_PAGEL,
                                   tacl.constants.TOKENIZER_JOINER_PAGEL)
        input_data = (
            ['nan', '1', 'text1', 'base', '2', 'A'],
            ['nan dus', '2', 'text1', 'base', '1', 'A'],
            ['pa', '1', 'text2', 'base', '1', 'B'])
        expected_rows = (
            ('nan', '1', 'text1', 'base', '1', 'A'),
            ('nan dus', '2', 'text1', 'base', '1', 'A'),
            ('pa', '1', 'text2', 'base', '1', 'B'))
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), set(expected_rows))

    def test_reduce_pagel(self):
        tokenizer = tacl.Tokenizer(tacl.constants.TOKENIZER_PATTERN_PAGEL,
                                   tacl.constants.TOKENIZER_JOINER_PAGEL)
        input_data = (
            ['pa dus', '2', 'text1', 'base', '1', 'B'],
            ['pa dus gcig', '3', 'text1', 'base', '1', 'B'],
            ['pa dus gcig na', '4', 'text1', 'base', '1', 'B'],
            ['pa dus', '2', 'text1', 'wit', '2', 'B'],
            ['pa dus gcig', '3', 'text1', 'wit', '1', 'B'],
        )
        expected_rows = (
            ('pa dus', '2', 'text1', 'wit', '1', 'B'),
            ('pa dus gcig', '3', 'text1', 'wit', '1', 'B'),
            ('pa dus gcig na', '4', 'text1', 'base', '1', 'B'),
        )
        actual_rows = self._perform_reduce(input_data, tokenizer)
        self.assertEqual(set(actual_rows), set(expected_rows))

    def _perform_reduce(self, input_data, tokenizer):
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, tokenizer)
        results.reduce()
        return self._get_rows_from_csv(results.csv(io.StringIO(newline='')))

    def test_remove_label(self):
        """Test removing labelled results."""
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit', '3', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'],
            ['ABD', '3', 'a', 'base', '1', 'B'],
            ['ABCD', '4', 'a', 'base', '2', 'B'],
            ['AB', '2', 'b', 'base', '2', 'AB'],
            ['ABC', '3', 'b', 'base', '2', 'AB'],
            ['AB', '2', 'c', 'wit', '1', 'B'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.remove_label('B')
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A'),
            ('AB', '2', 'a', 'wit', '3', 'A'),
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('AB', '2', 'b', 'base', '2', 'AB'),
            ('ABC', '3', 'b', 'base', '2', 'AB')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_remove_missing_label(self):
        """Test removing a label that doesn't exist in the results."""
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit', '3', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.remove_label('C')
        expected_rows = [
            ('AB', '2', 'a', 'base', '4', 'A'),
            ('AB', '2', 'a', 'wit', '3', 'A'),
            ('ABC', '3', 'a', 'base', '2', 'A')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_sort(self):
        input_data = (
            ['AB', '2', 'a', 'base', '4', 'A'],
            ['AB', '2', 'a', 'wit', '3', 'A'],
            ['ABC', '3', 'a', 'base', '2', 'A'],
            ['ABD', '3', 'a', 'base', '1', 'B'],
            ['ABCD', '4', 'a', 'base', '2', 'B'],
            ['AB', '2', 'b', 'base', '2', 'AB'],
            ['AB', '2', 'b', 'a', '2', 'AB'],
            ['ABC', '3', 'b', 'base', '2', 'AB'],
            ['ABC', '3', 'c', 'base', '3', 'A'])
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, self._tokenizer)
        results.sort()
        expected_rows = [
            ('ABCD', '4', 'a', 'base', '2', 'B'),
            ('ABC', '3', 'c', 'base', '3', 'A'),
            ('ABC', '3', 'a', 'base', '2', 'A'),
            ('ABC', '3', 'b', 'base', '2', 'AB'),
            ('ABD', '3', 'a', 'base', '1', 'B'),
            ('AB', '2', 'a', 'base', '4', 'A'),
            ('AB', '2', 'a', 'wit', '3', 'A'),
            ('AB', '2', 'b', 'a', '2', 'AB'),
            ('AB', '2', 'b', 'base', '2', 'AB')]
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        self.assertEqual(actual_rows, expected_rows)

    def test_zero_fill(self):
        tokenizer = tacl.Tokenizer(tacl.constants.TOKENIZER_PATTERN_CBETA,
                                   tacl.constants.TOKENIZER_JOINER_CBETA)
        input_data = (
            ['AB', '2', 'T1', 'base', '7', 'A'],
            ['AB', '2', 'T2', 'a', '3', 'B'],
            ['ABC', '3', 'T5', 'base', '1', 'A'],
        )
        base_dir = os.path.dirname(__file__)
        stripped_dir = os.path.join(base_dir, 'integration_tests', 'data',
                                    'stripped')
        corpus = tacl.Corpus(stripped_dir, tokenizer)
        fh = self._create_csv(input_data)
        results = tacl.Results(fh, tokenizer)
        results.zero_fill(corpus)
        actual_rows = self._get_rows_from_csv(results.csv(
            io.StringIO(newline='')))
        expected_rows = [
            ('AB', '2', 'T1', 'base', '7', 'A'),
            ('AB', '2', 'T1', 'a', '0', 'A'),
            ('AB', '2', 'T2', 'a', '3', 'B'),
            ('AB', '2', 'T2', 'base', '0', 'B'),
            ('ABC', '3', 'T5', 'base', '1', 'A'),
        ]
        self.assertEqual(set(actual_rows), set(expected_rows))


if __name__ == '__main__':
    unittest.main()
