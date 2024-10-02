from flask import Flask, request, jsonify, send_from_directory
import boto3
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/list-instances', methods=['POST'])
def list_instances():
    data = request.json
    source = data.get('source')
    region = data.get('region')
    
    if source == 'aws':
        aws_access_key = data.get('awsAccessKey')
        aws_secret_key = data.get('awsSecretKey')

        # Create EC2 client
        ec2_client = boto3.client(
            'ec2',
            region_name=region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # List EC2 instances
        instances = ec2_client.describe_instances()
        instance_ids = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

        return jsonify({'instances': instance_ids})

    # Placeholder for Azure and GCP logic
    return jsonify({'instances': []})

@app.route('/migrate-instances', methods=['POST'])
def migrate_instances():
    data = request.json
    instances = data.get('instances', [])
    
    # Logic for migrating instances goes here
    # This is a placeholder for actual migration code
    print(f"Migrating instances: {instances}")

    return jsonify({'message': 'Migration initiated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
