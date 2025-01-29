output domain { value = aws_ses_domain_identity.ses_domain_identity.domain }
output verification_token { value = aws_ses_domain_identity.ses_domain_identity.verification_token }
output arn { value = aws_ses_domain_identity.ses_domain_identity.arn }