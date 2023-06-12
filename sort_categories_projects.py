""" Sort categories and projects in projects.yaml by title and name, respectively. """
import ruamel.yaml


def load_yaml_file(filepath):
    """Load YAML data from a file."""
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.preserve_quotes = True
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)
    return yaml, data


def write_yaml_file(yaml, data, filepath):
    """Write YAML data to a file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def validate_data(data):
    """
    Validate that each project uses existing labels and categories.

    :param data: The loaded YAML data.
    :raises ValueError: If invalid labels or categories are found.
    """
    valid_labels = {label['label'] for label in data['labels']}
    valid_categories = {category['category'] for category in data['categories']}
    for project in data['projects']:
        if 'labels' in project:
            if not set(project['labels']).issubset(valid_labels):
                raise ValueError(f"Invalid labels in project {project['name']}")
        if project['category'] not in valid_categories:
            raise ValueError(f"Invalid category in project {project['name']}")


def sort_yaml_data(data):
    """
    Sort categories in YAML data by title.
    Sort projects in YAML data first by category, then by name.
    """
    # Sort categories by title
    data['categories'].sort(key=lambda x: x['title'])

    # Sort projects first by category, then by name
    data['projects'].sort(key=lambda x: (x['category'], x['name']))

    return data


if __name__ == '__main__':
    yaml_obj, yaml_data = load_yaml_file('projects.yaml')
    validate_data(yaml_data)
    sorted_data = sort_yaml_data(yaml_data)
    write_yaml_file(yaml_obj, sorted_data, 'projects.yaml')
