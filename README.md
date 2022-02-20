# Try! CDK No. 0009. "Next.js on S3/CF with a custom domain."

## Procedure you replay making the code in this repository.

### Setup the top directory.

```
mkdir try-cdk-0009
cd try-cdk-0009
git init
echo ".venv/" >> .gitignore
python3 -m venv .venv
source .venv/bin/activate
```

### Setup the CDK directory.

```
mkdir cdk
cd cdk
cdk init app --language python --generate-only
cd cdk
python -m pip install -r requirements.txt
```

### Edit CDK code.

Open Visual Studio Code. You should enjoy coding with IntelliSense.

Edit `try-cdk-0009/cdk/cdk/app.py` and update the stack id (`TryCdk0009` in this repo.).

```
CdkStack(app, "TryCdk0009",
```

Edit `try-cdk-0009/cdk/cdk/cdk_stack.py` to configure AWS infra.

### Setup Next.js code.

Locate at the top of `try-cdk-0009` directory.

c.f. https://nextjs.org/learn/basics/create-nextjs-app/setup

```
npx create-next-app nextjs-blog --use-npm --example "https://github.com/vercel/next-learn/tree/master/basics/learn-starter"
```

## Deploy

Needs passing your parameters as Contexts.

```
cdk deploy -c ROOT_DOMAIN_NAME=munepi.com -c HOSTED_ZONE_ID=Z99999999ZZZZZZZZZZZZ -c CERTIFICATE_ARN=arn:aws:acm:us-east-1:999999999999:certificate/ac9564db-15d8-4f37-af06-eaa862488829
```
