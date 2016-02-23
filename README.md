#Environment Variables

##GitHub
GIT_USERNAME = '??'

GIT_PASSWORD = '??'

GIT_REPOSITORY = 'bitbucket.org/felipehaack/chaordic-restapi.git'

##DATABASE
DATABASE_NAME = 'chaordic_shorturl'

DATABASE_USERNAME = 'chaordic'

DATABASE_PASSWORD = 'chaordic'

DATABASE_HOST = 'http://172.101.1.2'

[Instance: i-f1baf82b] Command failed on instance. Return code: 1 Output: (TRUNCATED)...n-zero code: 128 Failed to build Docker image aws_beanstalk/staging-app: [0mThe command '/bin/sh -c git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@${GIT_REPOSITORY} --progress --verbose' returned a non-zero code: 128. Check snapshot logs for details. Hook /opt/elasticbeanstalk/hooks/appdeploy/pre/03build.sh failed. For more detail, check /var/log/eb-activity.log using console or EB CLI.