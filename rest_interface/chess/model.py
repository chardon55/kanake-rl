from pathlib import Path
import shutil
import re
from datetime import datetime


MODEL_ROOT = Path('models')


def get_latest_model():
    global MODEL_ROOT

    dates = []

    for item in MODEL_ROOT.iterdir():
        item_str = str(item)

        if re.match(r"^models/ddqn-target-.+$", item_str):
            continue

        dates.append(datetime.strptime(item_str.lstrip(
            'models/ddqn-').rstrip('.pt'), r'%Y-%m-%d_%H-%M-%S'))

    return Path('models/ddqn-{0}.pt'.format(max(dates).strftime(r'%Y-%m-%d_%H-%M-%S')))


# def cp_models():
#     global MODEL_ROOT

#     for item in MODEL_ROOT.iterdir():
#         item_str = str(item)

#         if re.match(r"^models/ddqn-target-.+$", item_str):
#             continue

#         parts = item_str.lstrip(
#             'models/ddqn-').rstrip('-.pt').rsplit('-', maxsplit=1)

#         shutil.copyfile(item_str,
#         'models/ddqn-{0}.pt'.format(datetime.strptime(
#             parts[0], r'%Y-%m-%d_%H-%M').strftime(r'%Y-%m-%d_%H-%M-%S')))


# if __name__ == '__main__':
#     print(get_latest_model())
