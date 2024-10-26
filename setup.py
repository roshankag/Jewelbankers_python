# from setuptools import setup, find_packages

# setup(
#     name='my_fastapi_app',
#     version='1.0.0',
#     packages=find_packages(),
#     install_requires=[
#         'fastapi',
#         'uvicorn',
#         'pydantic',
#         'google-generativeai',
#         'Pillow',
#         'python-multipart',
#     ],
#     entry_points={
#         'console_scripts': [
#             'run-fastapi=uvicorn:main',  # This points to your FastAPI app's entry point in main.py
#         ],
#     },
# )


from setuptools import setup, find_packages

setup(
    name="main",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "google-generativeai",
        "Pillow",
        "python-multipart",
    "google-ai-generativelanguage",
    "google-api-core",
    "google-api-python-client",
    "google-auth",
    "google-auth-httplib2",
    "google-cloud-aiplatform",
    "google-cloud-bigquery",
    "google-cloud-core",
    "google-cloud-resource-manager",
    "google-cloud-storage",
    "google-cloud-vision",
    "google-crc32c",
    "google-generativeai",
    "google-resumable-media",
    "googleapis-common-protos",
    "grpc-google-iam-v1",
    "grpcio",
    "grpcio-status"


    ],
    entry_points={
        "console_scripts": [
            "run-fastapi=main:app"  # Change to your main entry point
        ]
    },
)
