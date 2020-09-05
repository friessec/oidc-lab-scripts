



if __name__ == "__main__":
    command(ClearCommand())

    jwks = JWKSSpoof()
    jwks.uri = "https://attack-idp.professos/modauthopenidc/jwks"
    jwks.keys[0]["another"] = "abbbaa"

    keys = jwks.keys

    #print({ "keys": keys})

    command(jwks)
    #data = json.dumps(jwks.__dict__)
    #print(data)

    #cmd = ReplaceCommand()
    #cmd.uri = "mitreid-server/oidc-server/authorize"
    #cmd.replaceKeyVal("redirect_uri", '<script>"42"</script>')

    #command(cmd)
    #sleep(4)
    #command(ClearCommand())
