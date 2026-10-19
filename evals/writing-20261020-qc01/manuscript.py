"""Extract an evaluation body without changing the writer's delivered artifact.

Both an initial attribution/title heading and a separate final Attribution
section are valid task deliveries. Reject other body headings: these evaluation
requests require connected prose without internal subheadings.
"""


def body_text(text):
    lines = text.lstrip('\ufeff').splitlines()
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    attribution = [i for i, line in enumerate(lines)
                   if line == '## Attribution'
                   or (line.startswith('## Attribution (') and line.endswith(')'))]
    if len(attribution) > 1:
        raise ValueError('Multiple attribution sections')
    if attribution:
        index = attribution[0]
        if index == 0 or not any(line.strip() for line in lines[index + 1:]):
            raise ValueError('Empty manuscript or attribution section')
        lines = lines[:index]
    body = '\n'.join(lines).strip()
    if not body or any(line.lstrip().startswith('#') for line in body.splitlines()):
        raise ValueError('Expected a manuscript body without internal headings')
    return body + '\n'
