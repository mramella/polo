# polo
Retrieves your balance in Poloniex.

The AWS Lambda needs to be created with the Python 3.6 runtime.

In the AWS Lambda console, you need to add your Polo secret and key as environment variables named 'SECRET' and 'KEY'.

You also need to create a DynamoDB table called 'polo', with a key named 'datetime' of type string.
