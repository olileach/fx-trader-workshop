#
#  Copyright 2010-2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
from random import randint
from time import sleep
import argparse
import json
import os
import sys
import time
from datetime import datetime 

os.system('clear')

def color_text(text, rgb):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

class rgb():
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255,255,255)
    # and so on ...

def main(max_trade, max_frequency):

    client = boto3.client('lambda')

    print('\033[1m',"\n Starting FX Trading Platform - Market is Open", '\033[1m')

    total_trades=0
    
    try:
        while True:
            
            trades=randint(2, max_trade)
            total_trades+=trades
            payload={"trade_executions": trades}
            timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(color_text("\nExecuting {} trades on FX trading platform at {}", rgb.GREEN).format(trades, timestamp))

            try:
                response = client.invoke(
                    InvocationType='Event',
                    FunctionName='fx-trade-results',
                    Payload=bytes(json.dumps(payload),encoding='utf8')
                )
                res = response['ResponseMetadata']['HTTPStatusCode']
                if res !=202:
                    raise
            except ClientError as e:
                quit_executor(total_trades, 1)

            sleeptime = randint(1, max_frequency)
            sys.stdout.write("\033[K")
            for i in range(sleeptime):
                print(color_text("\nWaiting for trade activity" + "." * i, rgb.YELLOW))
                sys.stdout.write("\033[F") # Cursor up one line
                sys.stdout.write("\033[F") # Cursor up one line
                time.sleep(1)
            
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F") # Cursor up one line
            
                  
    except KeyboardInterrupt:
        quit_executor(total_trades)

def quit_executor(total_trades, exit=None):
    
    os.system('clear')
    if exit==1:
        print('\033[1m',color_text(" \n WORKSHOP NOTE: Make sure you have disabled your Cloud9 AWS Temporary Credentials.", rgb.WHITE))
    print('\033[1m',color_text(" \n Number of trades executed: {}", rgb.WHITE).format(total_trades),'\033[0m')
    print('\033[1m',color_text("\r\r\n Stopping FX Trading Platform - Market is Closed\n\n", rgb.RED),'\033[0m')
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Valid Arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--max-volume", help="max volume")
    parser.add_argument("-f", "--max-frequency", help="max frequency")
    args = parser.parse_args()
    config = vars(args)
    max_volume = config.get('max_volume') or 100
    max_frequency = config.get('max_frequency') or 15
    
    main(int(max_volume), int(max_frequency))
