import argparse
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from faker import Faker
import time
from datetime import datetime

# function to parse SILENT parameter output  
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Instantiate Faker class  
faker = Faker()

# MAIN function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate fake data...')

    parser.add_argument('--interval', type=float, default=0.5,
                        help='interval of generating fake data in seconds')
    parser.add_argument('-n', type=int, default=1,
                        help='sample size')
    parser.add_argument('--host', dest="host", 
                        type=str, default='postgresql',
                        help='Host for the database')
    parser.add_argument('--password', '-p', dest="password", 
                        type=str, default='postgresql',
                        help='Password in plain text for the database')
    parser.add_argument('--silent', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="print fake data")

    args = parser.parse_args()

    print(f"Args parsed:")
    print(f"Interval: {args.interval}")
    print(f"Sample size; {args.n}")
    print(f"Host: {args.host}", end='\n\n')

    #-----------------------------------------------------------------

    CONNECTION_STRING = f"postgresql://postgres:{args.password}@{args.host}:5432/postgres"
    engine = create_engine(CONNECTION_STRING)

    print("Starting simulation...", end="\n\n")

    # Generate fake data and ingest
    while True:
        name          = [faker.name() for i in range(args.n)]
        gender        = [np.random.choice(["M", "F"], p=[0.5, 0.5]) for i in range(args.n)]
        address       = [faker.address() for i in range(args.n)]
        phone         = [faker.phone_number() for i in range(args.n)]
        email         = [faker.safe_email() for i in range(args.n)]
        photo         = [faker.image_url() for i in range(args.n)]
        birthdate     = [faker.date_of_birth().strftime("%Y-%m-%d") for i in range(args.n)]
        profession    = [faker.job() for i in range(args.n)]
        dt_update     = [datetime.now() for i in range(args.n)]

        df = pd.DataFrame({
            "name": name,
            "gender": gender,
            "address": address,
            "phone": phone,
            "email": email,
            "photo": photo,
            "birthdate": birthdate,
            "profession": profession, 
            "dt_update": dt_update
        })

        df.to_sql("customers", con=engine, if_exists="append", index=False)

        if not args.silent:
            print(df, end="\n\n")

        time.sleep(args.interval)