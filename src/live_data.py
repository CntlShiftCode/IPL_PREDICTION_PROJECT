import random
import time


def simulate_live_match():

    score = 0
    wickets = 0
    over = 0
    ball = 0

    while over < 20:

        ball += 1

        run = random.choice(
            [0, 1, 2, 4, 6]
        )

        if random.random() < 0.05:
            wickets += 1

        score += run

        yield {

            "score": score,

            "wickets": wickets,

            "over": f"{over}.{ball}"

        }

        time.sleep(1)

        if ball == 6:
            over += 1
            ball = 0