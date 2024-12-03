#!/bin/bash

# Exit on any error
set -e

# Configuration variables
STACK_NAME="${1:-my-stack}"
TEMPLATE_FILE="${2:-template.yml}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PARAMETERS_FILE="${3:-parameters.json}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_message $RED "Error: $1 is required but not installed."
        exit 1
    fi
}

# Function to validate prerequisites
validate_prerequisites() {
    check_command aws
    
    if [ ! -f "$TEMPLATE_FILE" ]; then
        print_message $RED "Error: Template file $TEMPLATE_FILE not found"
        exit 1
    fi
}

# Function to validate CloudFormation template
validate_template() {
    print_message $YELLOW "Validating CloudFormation template..."
    aws cloudformation validate-template \
        --template-body file://$TEMPLATE_FILE \
        --region $REGION
}

# Function to check stack status
check_stack_status() {
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].StackStatus' \
        --output text 2>/dev/null || echo "STACK_NOT_FOUND"
}

# Function to wait for stack operation to complete
wait_for_stack_operation() {
    local stack_operation=$1
    local counter=0
    local status
    
    print_message $YELLOW "Waiting for stack operation to complete..."
    
    while [ $counter -lt 60 ]; do
        status=$(check_stack_status)
        
        case $status in
            *_COMPLETE)
                print_message $GREEN "Stack operation completed successfully with status: $status"
                return 0
                ;;
            *_FAILED|ROLLBACK_*)
                print_message $RED "Stack operation failed with status: $status"
                aws cloudformation describe-stack-events \
                    --stack-name $STACK_NAME \
                    --region $REGION \
                    --query 'StackEvents[?ResourceStatus==`CREATE_FAILED` || ResourceStatus==`UPDATE_FAILED`].[LogicalResourceId,ResourceStatusReason]' \
                    --output text
                return 1
                ;;
            STACK_NOT_FOUND)
                if [ "$stack_operation" = "delete" ]; then
                    print_message $GREEN "Stack has been deleted successfully"
                    return 0
                fi
                ;;
        esac
        
        sleep 10
        ((counter++))
    done
    
    print_message $RED "Timeout waiting for stack operation to complete"
    return 1
}

# Function to deploy stack
deploy_stack() {
    local status=$(check_stack_status)
    local params_arg=""
    
    if [ -f "$PARAMETERS_FILE" ]; then
        params_arg="--parameters file://$PARAMETERS_FILE"
    fi
    
    if [ "$status" = "STACK_NOT_FOUND" ]; then
        print_message $YELLOW "Creating new stack: $STACK_NAME"
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --region $REGION \
            --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
            $params_arg
    else
        print_message $YELLOW "Updating existing stack: $STACK_NAME"
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --region $REGION \
            --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
            $params_arg
    fi
    
    wait_for_stack_operation "deploy"
}

# Main execution
main() {
    print_message $YELLOW "Starting CloudFormation deployment script..."
    print_message $YELLOW "Stack Name: $STACK_NAME"
    print_message $YELLOW "Template File: $TEMPLATE_FILE"
    print_message $YELLOW "Region: $REGION"
    
    validate_prerequisites
    validate_template
    deploy_stack
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "Stack deployment completed successfully"
        
        # Output stack outputs
        print_message $YELLOW "Stack Outputs:"
        aws cloudformation describe-stacks \
            --stack-name $STACK_NAME \
            --region $REGION \
            --query 'Stacks[0].Outputs' \
            --output table
    else
        print_message $RED "Stack deployment failed"
        exit 1
    fi
}

# Execute main function
main
