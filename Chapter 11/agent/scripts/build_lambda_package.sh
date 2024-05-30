#!/usr/bin/env bash 

# Declare variable to reuse directory validations
PACKAGE="package"

# Create directory and install dependencies of lambda function
if [ -d $PACKAGE ]
then
	echo ""$PACKAGE" folder already exists."
else
	echo "============================================="
	echo "Creating folder "$PACKAGE"..."
	mkdir $PACKAGE
	echo ""$PACKAGE" folder created."
	echo "============================================="
fi

# Declare variable that locates the requirements file with project dependencies
FILE_REQUIREMENTS=../function/lambda_requirements.txt

# Check if file lambda_requirements exists
if [ -f $FILE_REQUIREMENTS ]
then
	echo "============================================="
	echo "Installing dependencies in "$FILE_REQUIREMENTS""
	pip install --target ./package -r $FILE_REQUIREMENTS
	echo "Dependencies installed."
	echo "============================================="	
fi


cd $PACKAGE

# Declare variable that locates the handler function
LAMBDA_FUNCTION=../../function/lambda_function.py

# Check if file lambda_function.py exists
if [ -f $LAMBDA_FUNCTION ]
then
	echo "============================================="
	echo "Copying Handler function..."
	cp $LAMBDA_FUNCTION .
    echo "Copying custom modules..."
    mkdir worksheet
    cp -r ../../function/worksheet/__init__.py ./worksheet
    cp -r ../../function/worksheet/template.py ./worksheet
	echo ""
	echo "Creating file: lambda_function_payload.zip"
	zip -r9 ../lambda_function_payload.zip .
	echo "Zip file created."
	echo "============================================="
fi
