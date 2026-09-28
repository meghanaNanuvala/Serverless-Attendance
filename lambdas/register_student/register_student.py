import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name = 'us-east-1')

dynamodbTableName = 'class_student_tf'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
employeeTable = dynamodb.Table(dynamodbTableName)

# cdir = os.getcwd()
# filename = cdir.replace("Lambda_Functions\Function-1", "SES_EMAIL.txt")
# Please add the email di to test
subject = "Student Registered successfully for SWE-315/316."
body_text = "This is automated email body please do not use it for your reference."

def lambda_handler(event, context):
    print('Hi event')
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        response = index_employee_image(bucket, key)
        print('Hi response')
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            name = key.split('.')[0].split('_')
            firstName = name[0]
            lastName = name[1]
            emailId = name[2]

            email = emailId + "@iu.edu"
            receiver = os.environ.get('SENDER_EMAIL')
            body_html = """<html>
    <head></head>
    <body>
    <h2>Dear Professor, </h2>
    <p> {student_name} has been successsfully registered for class SWE-315/316. Have Fun!</a>.</p>
    <h3>Student Details:</h3>
    <p>Name: {student_name}</p>
    <p>Email: {email}</p>
    </body>
    </html>
                """.format(student_name = firstName + " "+ lastName, email = email)
            register_employee(faceId, firstName,lastName, emailId)
            #register_employee(faceId, firstName,lastName)
            send_email(receiver,body_html,body_text,subject)
        return response
    except Exception as e:
        print(e)
        print('Error processing employee image {} from bucket{}.'.format(key, bucket))
        raise e
    
# def extract_email(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     for line in lines:
#         if "SES_EMAIL=" in line:
#             email = line.split("=")[1].strip()
#             return email

#     # If "SES_EMAIL=" is not found, return None
#     return None

def index_employee_image(bucket, key):
    response = rekognition.index_faces(
        Image={
            'S3Object' : 
            {
                'Bucket' : bucket,
                'Name' : key
            }
        },
        CollectionId = "studentsImage_tf"
    )

    return response

# def register_employee(faceId, firstName,lastName,email_id):
def register_employee(faceId, firstName,lastName,email_id):
    employeeTable.put_item(
        Item = {
            'rekognitionId' : faceId,
            'firstName' : firstName,
            'lastName' : lastName,
            'email' : email_id
        }
    )

def send_email(Receiver, body_html, body_text, subject):
    client = boto3.client('ses', region_name='us-east-1')

    try:
        response = client.send_email(
            #Add env file later
            Source = os.environ.get('SENDER_EMAIL'),
            Destination={
                'ToAddresses': [
                    Receiver,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    },
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                },
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", end=" ")
        print(response['MessageId'])


# import boto3

# s3 = boto3.client('s3')
# rekognition = boto3.client('rekognition', region_name = 'us-east-1')

# dynamodbTableName = 'class_student_tf'
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# employeeTable = dynamodb.Table(dynamodbTableName)

# # Please add the email di to test
# sender = "youremail"
# receiver = "youremail"

# subject = "Student Registered successfully."

# body_text = "This is automated email body please do not use it for your reference."
# body_html = """<html>
#     <head></head>
#     <body>
#     <h1>Hey Hi...</h1>
#     <p>Dear Student of class SWE-315/316. Your image is successfully registered into the attendance system. Have Fun!</a>.</p>
#     </body>
#     </html>
#                 """

# def lambda_handler(event, context):
#     print(event)
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     key = event['Records'][0]['s3']['object']['key']

#     try:
#         response = index_employee_image(bucket, key)
#         print(response)
#         if response['ResponseMetadata']['HTTPStatusCode'] == 200:
#             faceId = response['FaceRecords'][0]['Face']['FaceId']
#             name = key.split('.')[0].split('_')
#             firstName = name[0]
#             lastName = name[1]
#             emailId = name[2]
#             register_employee(faceId, firstName,lastName, emailId)
#             send_email(sender,receiver,body_html, body_text,subject)
#         return response
#     except Exception as e:
#         print(e)
#         print('Error processing employee image {} from bucket{}.'.format(key, bucket))
#         raise e
    

# def index_employee_image(bucket, key):
#     response = rekognition.index_faces(
#         Image={
#             'S3Object' : 
#             {
#                 'Bucket' : bucket,
#                 'Name' : key
#             }
#         },
#         CollectionId = "studentsImage_tf"
#     )

#     return response

# def register_employee(faceId, firstName,lastName,email_id):
#     employeeTable.put_item(
#         Item = {
#             'rekognitionId' : faceId,
#             'firstName' : firstName,
#             'lastName' : lastName,
#             'email' : email_id
#         }
#     )