#!/usr/bin/env python3
"""Summarise retained, disjoint cost components. Missing prices are not zero."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

FIELDS = ['date_utc', 'run_id', 'component', 'amount', 'currency', 'basis', 'note']
BASES = {'provider_reported', 'list_rate_estimate', 'unavailable'}


def canonical_date(value):
    return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)) and date.fromisoformat(value).isoformat() == value


def summarise(path, selected_date=None):
    diagnostics, records = [], []
    try:
        with Path(path).open(newline='', encoding='utf-8') as source:
            reader = csv.reader(source, strict=True)
            if next(reader, None) != FIELDS:
                diagnostics.append('costs.csv: expected columns ' + ','.join(FIELDS))
            for line, cells in enumerate(reader, 2):
                if len(cells) != len(FIELDS):
                    diagnostics.append(f'costs.csv:{line}: expected {len(FIELDS)} cells')
                    continue
                records.append((line, dict(zip(FIELDS, cells))))
    except (OSError, UnicodeError, csv.Error) as error:
        diagnostics.append(f'costs.csv: {error}')
    seen, components, totals, unpriced = set(), {}, {}, []
    for line, row in records:
        where = f'costs.csv:{line}'
        try:
            if not canonical_date(row['date_utc']):
                raise ValueError()
        except ValueError:
            diagnostics.append(f'{where}: date_utc must be YYYY-MM-DD')
        if not row['run_id'].strip() or not row['component'].strip():
            diagnostics.append(f'{where}: run_id and component are required')
        key = (row['run_id'], row['component'])
        if key in seen:
            diagnostics.append(f'{where}: duplicate run/component {key}')
        seen.add(key)
        components.setdefault(row['run_id'], set()).add(row['component'])
        if row['basis'] not in BASES:
            diagnostics.append(f'{where}: unknown basis {row["basis"]!r}')
        amount = None
        if row['basis'] == 'unavailable':
            if row['amount'] or row['currency']:
                diagnostics.append(f'{where}: unavailable costs need blank amount and currency')
        else:
            try:
                amount = Decimal(row['amount'])
                if not amount.is_finite() or amount < 0:
                    raise InvalidOperation()
            except InvalidOperation:
                diagnostics.append(f'{where}: amount must be a finite non-negative decimal')
            if not re.fullmatch(r'[A-Z]{3}', row['currency']):
                diagnostics.append(f'{where}: currency must be a three-letter uppercase code')
        if selected_date and row['date_utc'] != selected_date:
            continue
        if row['basis'] == 'unavailable':
            unpriced.append(row)
        elif amount is not None and amount.is_finite():
            group = (row['date_utc'], row['currency'], row['basis'])
            totals[group] = totals.get(group, Decimal(0)) + amount
    for run_id, names in components.items():
        if 'total' in names and len(names) > 1:
            diagnostics.append(f'{run_id}: a total cannot accompany component costs')
    return {
        'schema_version': 1,
        'valid': not diagnostics,
        'diagnostics': diagnostics,
        'subtotals': [] if diagnostics else [dict(date_utc=day, currency=currency, basis=basis, amount=str(amount))
                                               for (day, currency, basis), amount in sorted(totals.items())],
        'unpriced': unpriced,
        'coverage': 'Recorded components only; missing components and unpriced usage are not included in subtotals.',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--date')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.date:
        try:
            if not canonical_date(args.date):
                raise ValueError()
        except ValueError:
            parser.error('--date must be YYYY-MM-DD')
    result = summarise(args.root / 'schedule/costs.csv', args.date)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print('Recorded cost subtotals' + (f' for {args.date}' if args.date else ''))
        for error in result['diagnostics']:
            print(f'Problem: {error}')
        for row in result['subtotals']:
            print(f'{row["date_utc"]} {row["currency"]} {row["amount"]} ({row["basis"]})')
        print(f'Unpriced components: {len(result["unpriced"])}')
        for row in result['unpriced']:
            print(f'  {row["date_utc"]} {row["run_id"]} / {row["component"]}: {row["note"]}')
        print(result['coverage'])
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
