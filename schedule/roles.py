"""Selection only: roles never change readiness, dependencies or queue history."""
ROLES = ('all', 'watch', 'research', 'horizon', 'editor')


def task_role(row):
    if row['study'] == 'horizon':
        return 'horizon'
    if row['kind'] == 'observe' or row['study'] == 'log':
        return 'watch'
    if row['kind'] == 'maintain' and row['study'] == 'site':
        return 'editor'
    return 'research'


def accepts(row, role):
    if role not in ROLES:
        raise ValueError(f'unknown role: {role}')
    return role == 'all' or task_role(row) == role


def selection(report, role):
    """Keep the global readiness report intact, including other roles' waits."""
    ids = {row['id'] for row in report['rows'] if accepts(row, role)}
    return {key: [identity for identity in report[key] if identity in ids]
            for key in ('ready', 'overdue')}
