import { CognitoJwtVerifier } from "aws-jwt-verify";

export const lambdaHandler = async (event, context) => {
    try {
        
        
        const { UserPoolId, ClientId } = process.env;
        
        // Verifier that expects valid access tokens:
        const verifier = CognitoJwtVerifier.create({
          userPoolId: UserPoolId,
          tokenUse: "access",
          clientId: ClientId,
        });

        try {
          const payload = await verifier.verify(
            event.token
          );
          console.log("Token is valid. Payload:", payload);
          return {
            'statusCode': 200,
            'body': JSON.stringify({
                decoded_token: payload
            })
          };
        } catch {
         console.log("Token not valid!");
         return {
            'statusCode': 403,
            'body': 'Token s not valid!'
          };
        }
        
    } catch (err) {
        console.log(err);
        return err;
    }
};
