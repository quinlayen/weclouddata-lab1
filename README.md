# weclouddata-lab1
Lab 1 for We Cloud Data data engineering bootcamp
First practice with hands-on ETL process
In this lab we use an EC2 instance to access an API at https://www.themuse.com/api/public/jobs, extracting the data.
The data is than transformed using a python script and then saved/loaded into an S3 bucket.

# usage
Set up necessary EC2 and S3 buckets, giving S3 Full Access permissions to EC2
Install all files to EC2
Make sure python script subprocess function S3 information matches what you are using.
Run ./init.sh
Run ./run.sh
