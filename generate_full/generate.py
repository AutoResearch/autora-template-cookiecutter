import os
from cookiecutter.main import cookiecutter
import shutil



DIR = os.path.dirname(os.path.realpath(__file__))
PARENT = os.path.join(DIR, '..')
FOLDER_NAME = "target"
FOLDER_PATH = os.path.join(DIR, FOLDER_NAME)

# Create the directory
os.makedirs(FOLDER_PATH, exist_ok=True)

contribution_types = ["theorist", "experimentalist", "experiment_runner", "synthetic_data"]
experimentalist_subtype = ["sampler", "pooler"]
runner_subtypes = ["experimentation_manager", "recruitment_manager"]


def bake_contribution(contrib_type, sub_type=None):
    if sub_type is not None:
        name = f"{contrib_type}-{sub_type}-example"
    else:
        name =  f"{contrib_type}-example"
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


    # make autora
    os.makedirs(os.path.join(FOLDER_PATH, '.'), exist_ok=True)

    # copy all folders into the autora folder (if they don't exist)
    for f in contribution_folders:
        copy_new_files(os.path.join(FOLDER_PATH, f), os.path.join(FOLDER_PATH, '.'))
        shutil.rmtree(os.path.join(FOLDER_PATH, f))

if __name__ == '__main__':
    main()