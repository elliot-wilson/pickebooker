import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        help="Date to book the court (YYYY-MM-DD)",
        required=True,
    )
    parser.add_argument(
        "--start-gte",
        type=int,
        help="Start hour for booking range (0-23)",
        required=True,
    )
    parser.add_argument(
        "--start-lte",
        type=int,
        help="End hour for booking range (0-23)",
        required=True,
    )
    args = parser.parse_args()
    with open("/tmp/ran.txt", "w") as f:
        f.write("Ran at all.\n")
    with open("/Users/elliotwilson/Desktop/test.txt", "w") as f:
        f.write(
            "Booking a court !!dfssttfor date: {}, start hour: {}, end hour: {}".format(
                args.date,
                args.start_gte,
                args.start_lte,
            )
        )
