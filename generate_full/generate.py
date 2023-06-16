import os
from cookiecutter.main import cookiecutter
import shutil

DIR = os.path.dirname(os.path.realpath(__file__))
PARENT = os.path.join(DIR, '..')
FOLDER_NAME = "target"
FOLDER_PATH = os.path.join(DIR, FOLDER_NAME)

# Create the directory
os.makedirs(FOLDER_PATH, exist_ok=True)

contribution_types = ["theorist", "experimentalist", "experiment_runner"]
experimentalist_subtype = ["sampler", "pooler"]
runner_subtypes = ["experimentation_manager", "recruitment_manager", "synthetic"]


def bake_contribution(contrib_type, sub_type=None):
    if sub_type is not None:
        name = f"{contrib_type}-{sub_type}-example"
    else:
        name = f"{contrib_type}-example"
    extra_content = {
        "__contrib_name": name,
        "__autora_contribution_type": contrib_type,
    }
    if sub_type is not None:
        extra_content['__contrib_subtype'] = sub_type
    cookiecutter(
        PARENT,
        no_input=True,
        extra_context=extra_content,
        output_dir=FOLDER_PATH)


def copy_new_files(src, dst):
    """Copy files from src to dst, only if they don't exist in dst."""
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            copy_new_files(s, d)  # Recursive call
    else:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)


def create_readme():
    readme_src = os.path.join(PARENT, '{{ cookiecutter.__project_slug }}/README.md')
    readme_dist = os.path.join(FOLDER_PATH, 'README.md')

    shutil.copy(readme_src, readme_dist)

    # remove lines starting with {%
    output_lines = []
    with open(readme_dist, "r") as file:
        for line in file:
            # Skip lines that start with "{%"
            if line.lstrip().startswith("{%"):
                continue
            output_lines.append(line)

    # Write the output lines back to the README
    with open(readme_dist, "w") as file:
        for line in output_lines:
            file.write(line)


def main():
    # create all contributions
    for t in contribution_types:
        if t == 'experimentalist':
            for s in experimentalist_subtype:
                bake_contribution(t, s)
        elif t == 'experiment_runner':
            for s in runner_subtypes:
                bake_contribution(t, s)
        else:
            bake_contribution(t)

    # get a list of all created folders
    contribution_folders = [name for name in os.listdir(FOLDER_PATH) if os.path.isdir(os.path.join(FOLDER_PATH, name))]

    # copy all folders into the autora folder (if they don't exist)
    for f in contribution_folders:
        src_folder = os.path.join(FOLDER_PATH, f)
        copy_new_files(src_folder, os.path.join(FOLDER_PATH, '.'))
        shutil.rmtree(src_folder)

    create_readme()


if __name__ == '__main__':
    main()
