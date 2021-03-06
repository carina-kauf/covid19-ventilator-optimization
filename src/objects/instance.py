from random import randint
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ..helper_functions.update_for_case import get_random_update


@dataclass_json
@dataclass
class Instance:
    hospitals: dict = field(default_factory=dict)
    requests: dict = field(default_factory=dict)
    updates: dict = field(default_factory=dict)

    def generate_updates(self):

        time_frame = [
            min(r.filed_at for r in self.requests.values()),
            max(r.filed_at for r in self.requests.values()),
        ]

        for key in self.hospitals:
            # 10 updates over the time frame
            for ind in range(10):
                time = randint(int(time_frame[0]), int(time_frame[1]))
                update = get_random_update(time, self.hospitals[key])

                self.updates[f"{key}#{ind}"] = update
