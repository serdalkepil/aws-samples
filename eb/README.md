AWS Elastic Beanstalk CLI Commands and their description for the super busy developer.

eb init

    Used to configure a local repository for your Elastic Beanstalk environment and source code. This will prompt you for your aws-access-id & aws-secret-key to connect to your aws account.

eb list

    Lists down all environments that are present for your application

eb open

    Opens the public url of the application

eb health

    To check the status of the application and various instances

eb events

    Prints the latest events for the specific environment

eb appversion

    Shows all app versions which are available in an interactive mode. User can delete a version of the application or create the application version lifecycle policy

eb config

    Gets all config of the environment. Saves the environment configuration settings as well as uploads, downloads, or lists saved configurations

eb terminate

    Terminates the environment

eb restore

    Rebuilds a terminated environment, creating a new environment with the same name, ID, and configuration

eb upgrade

    Upgrades the platform of your environment to the most recent version available for the platform

eb clone

    Clones the environment

eb create

    Creates a new environment and deploys an application version to it

eb abort

    Cancels an upgrade when environment configuration changes to instances are still in progress

eb scale

    Scales the environment to always run on a specified number of instances, setting both the minimum and maximum number of instances to the specified number

eb swap

    Helps you swap the environment's CNAME with the CNAME of another environment to avoid any down time

eb logs

    Retrieves the tail logs of your environment

eb logs --all

    Retrieves all logs of your environment

eb setenv

    Set an environment property

eb printenv

    Prints the environment properties

eb deploy

    Deploys the application source bundle from the initialized project directory to the running application

eb codesource

    Configures the EB CLI to deploy from a CodeCommit repository, or disables CodeCommit integration and uploads the source bundle from your local machine

eb ssh

    Allows you to ssh into a non windows server/instance

eb tags

    Add, delete, update, and list tags of an Elastic Beanstalk resource

Elastic Beanstalk CLI install with automated scripts

    https://github.com/aws/aws-elastic-beanstalk-cli-setup#macoslinux
    Linux --> python ./aws-elastic-beanstalk-cli-setup/scripts/ebcli_installer.py
