#!/usr/bin/env python3

import os
import time
import boto3.ec2
from botocore.exceptions import ClientError

VERSION = '1.5.0'
ec2 = boto3.client('ec2', region_name='us-east-2')


class Mem:
    instance_id = ""


def read_credentials():
    """
    Cred file goes in the home directory of bot user
    :return: The EC2 instance id.
    """
    home_dir = os.path.expanduser('~')
    credentials_file_path = os.path.join(home_dir, "instance_id.txt")
    try:
        with open(credentials_file_path, 'r') as f:
            credentials = [line.strip() for line in f]
            return credentials
    except FileNotFoundError as e:
        print("Error Message: {0}".format(e))


def evaluate(args):
    """
    Evaluate the given arguments.
    :param args: The user's input.
    """
    if args == 'startup':
        response = start_ec2()
    elif args == 'shutdown':
        response = stop_ec2()
    else:
        print("Missing argument! Either startup or shutdown.")
        response = 'invalid command'

    return response


def start_ec2():
    """
    Try to start the EC2 instance.
    """
    print("------------------------------")
    print("Try to start the EC2 instance.")
    print("------------------------------")

    try:
        print("Start dry run...")
        ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        print("Start instance without dry run...")
        response = ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        response = 'Server didn\'t start right'
        print(e)
    return response


def stop_ec2():
    """
    Try to stop the EC2 instance.
    """
    print("------------------------------")
    print("Try to stop the EC2 instance.")
    print("------------------------------")

    try:
        ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        response = 'server couldn\'t shutdown correctly'
        print(e)
    return response


def fetch_public_ip():
    credentials = read_credentials()
    Mem.instance_id = credentials[0]
    """
    Fetch the public IP that has been assigned to the EC2 instance.
    :return: Print the public IP to the console.
    """
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    print()
    print("Waiting for public IPv4 address...")
    print()
    time.sleep(5)  # fix this -- ideally should be done only if server status == running, check the code
    # in current_status for what properties to look at for this

    reservations = ec2_client.describe_instances(InstanceIds=[Mem.instance_id]).get("Reservations")
    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))
            ip_address = instance.get("PublicIpAddress")
            print()
            return ip_address


def current_status():
    """Shows the current status of the server, usually running or stopped
    but sometimes it can be in an intermediate state
    :return: the response from the boto3 current_status command
    """
    credentials = read_credentials()
    Mem.instance_id = credentials[0]
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    response = ec2_client.describe_instance_status(InstanceIds=[Mem.instance_id], IncludeAllInstances=True)
    return response['InstanceStatuses'][0]['InstanceState']['Name']


def bash_script_executor(commands):
    """Runs commands on remote linux instances
    ideally, so I don't have to add more to this, just have it call a shell script thats on the EC2
    the shell script goes in the commands param
    :param commands: a list of strings, each one a command to execute on the instances
    :return: the response from the send_command function (check the boto3 docs for ssm client.send_command() )
    """
    credentials = read_credentials()
    Mem.instance_id = credentials[0]
    ids = [Mem.instance_id]
    ssm_client = boto3.client('ssm', region_name="us-east-2")
    resp = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': commands},
        InstanceIds=ids
    )
    return resp


def main(argv):
    credentials = read_credentials()
    Mem.instance_id = credentials[0]
    response = evaluate(argv)
    return response
